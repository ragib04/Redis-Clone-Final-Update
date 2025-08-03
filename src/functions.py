import time
from sortedcontainers import SortedSet
from .exception import *
import traceback
import random

class Redis:
    def __init__(self):
        self.hash_table = {}
        self.expire = {}
        self.exp_queue = SortedSet()
        self.changed = {}
        self.z_map = {}

    def __repr__(self):
        return f'curr_time : {time.time()}\n\n' \
               f'hash_table :\n{self.hash_table}\n\n' \
               f'expire :\n{self.expire}\n\n' \
               f'changed :\n{self.changed}\n\n' \
               f'z_map :\n{self.z_map}'

    def log(self, curr_time, func, *args):
        command = [str(curr_time), func]
        for i in args:
            command.append(i)
        command = ' '.join(command)
        command = command.strip(' ')
        command += '\n'
        with open("log.txt", "a") as logfile:
            logfile.write(command)

    def search_util(self, item):
        low, high = 0, len(self.exp_queue)
        while low <= high:
            mid = (low + high) // 2
            if self.exp_queue[mid][0] == item:
                self.exp_queue.pop(mid)
                return True
            elif self.exp_queue[mid][0] < item[0]:
                low = mid + 1
            else:
                high = mid - 1
        return False

    def search_index_util(self, sorted_set, item):
        low, high = 0, len(sorted_set)-1
        while low <= high:
            mid = (low + high) // 2
            if sorted_set[mid][0] == item:
                return mid
            elif sorted_set[mid][0] < item:
                low = mid + 1
            else:
                high = mid - 1
        # return str(None)
        return 'Index Not Found'

    def destroy_util(self, curr_time, hash_key):
        """
        :param param:
        :return:
        """
        if hash_key in self.hash_table and self.expire[hash_key] is not None and self.expire[hash_key] <= round(time.time(), 4):
            self.DELETE(curr_time, hash_key)
            return True
        else:
            return False

    def auto_clean_util(self, curr_time):
        count = 0
        while count < 10 and len(self.hash_table) > 100:
            sample = random.sample(self.hash_table.keys(), 10)
            for key in sample:
                self.destroy_util(curr_time, key)
            count += 1


    def START(self):
        pass

    def GET(self, curr_time, hash_key):
        """
        :param param:
        :return:
        """
        self.destroy_util(curr_time, hash_key)
        if hash_key in self.hash_table:
            if isinstance(self.hash_table[hash_key], str):
                # Element Found
                return self.hash_table[hash_key]
            else:
                # Throw Error -> Element found but not string
                raise NoStringValueError('NoStringValueError')
        else:
            # Element not found
            return str(None)

    def EXPIRE(self, curr_time, hash_key, seconds):
        """
        :param hash_key:
        :param seconds:
        :return:
        """
        if hash_key in self.hash_table:
            exp_time = round(curr_time, 4) + float(seconds)
            self.expire[hash_key] = exp_time
            if self.expire[hash_key] is None:
                self.exp_queue.add((exp_time, hash_key))
            else:
                # old_exp = self.expire[hash_key]
                # self.search_util((old_exp, hash_key))
                self.exp_queue.add((exp_time, hash_key))
            self.log(curr_time, "EXPIRE", hash_key, seconds)
            return '1'
        else:
            return '0'

    def TTL(self, curr_time, hash_key):
        self.destroy_util(curr_time, hash_key)
        if hash_key in self.hash_table and self.expire[hash_key] is not None:
            return str(time.time() - self.expire[hash_key])
        else:
            return str(None)

    def ping(self):
        return 'PONG'

    def DELETE(self, curr_time, hash_key):
        """
        :param param:
        :return:
        """

        if hash_key in self.hash_table:
            del self.hash_table[hash_key]
            del self.expire[hash_key]
            if hash_key in self.changed:
                del self.changed[hash_key]
            if hash_key in self.z_map:
                del self.z_map[hash_key]
            self.log(curr_time, "DELETE", hash_key)

            return '1'
        else:
            return '0'


    def SET(self, curr_time, hash_key, hash_val, *args):
        self.destroy_util(curr_time, hash_key)
        x = hash_key in self.hash_table
        ex, px, xx, nx, keepttl = [False] * 5
        kwargs = {}
        for i in range(len(args)):
            if args[i].lower() == 'ex':
                ex = True
                try:
                    kwargs['EX'] = int(args[i + 1])
                except:
                    raise InvalidRequest('InvalidRequest')
            elif args[i].lower() == 'px':
                px = True
                try:
                    kwargs['PX'] = int(args[i + 1])
                except:
                    raise InvalidRequest('InvalidRequest')
            elif args[i].lower() == 'xx':
                xx = True
            elif args[i].lower() == 'nx':
                nx = True
            elif args[i].lower() == 'keepttl':
                keepttl = True

        if (x is False and xx) or (x is True and nx):
            return str(None)
        # Make entry in both expiry table and hash table
        if (ex and px) or (nx and xx):
            raise InvalidRequest('InvalidRequest')
        if keepttl:
            if ex or nx:
                raise InvalidRequest('InvalidRequest')
            else:
                if hash_key in self.hash_table and self.expire[hash_key] is not None:
                    self.hash_table[hash_key] = str(hash_val)
                else:
                    self.hash_table[hash_key] = str(hash_val)
                    self.expire[hash_key] = None
                self.log(curr_time, 'SET', hash_key, hash_val, *args)
                return 'OK'
        else:
            self.hash_table[hash_key] = str(hash_val)
            old_exp = None
            if hash_key in self.expire:
                old_exp = self.expire[hash_key]
            self.expire[hash_key] = None
            if old_exp is not None:
                self.search_util((old_exp, hash_key))
            if ex:
                exp_time = round(curr_time, 4) + kwargs['EX']
                self.expire[hash_key] = exp_time
                # Remove then Add in Queue
                self.exp_queue.add((exp_time, hash_key))
            elif px:
                seconds = round((kwargs['PX'] / 1000), 4)
                exp_time = round(curr_time, 4) + seconds
                self.expire[hash_key] = exp_time
                # Remove and Add in Queue
                self.exp_queue.add((exp_time, hash_key))
            self.log(curr_time, 'SET', hash_key, hash_val, *args)
            return 'OK'

    def ZINCRBY(self, hash_key, score, key):
        # if hash_key in self.hash_table and type(self.hash_table[hash_key]) == SortedSet:
        pass



    def ZADD(self, curr_time, hash_key, score, key, *args):
        self.destroy_util(curr_time, hash_key)
        nx, xx, ch, incr, index = False, False, False, False, len(args)
        ind = 0
        for arg in args:
            if arg.lower() == 'nx':
                nx = True
                index = min(ind, index)
            elif arg.lower() == 'xx':
                xx = True
                index = min(ind, index)
            elif arg.lower() == 'ch':
                ch = True
                index = min(ind, index)
            elif arg.lower() == 'incr':
                incr = True
                index = min(ind, index)
            ind += 1
        keyword = ['NX', 'XX', 'CH', 'INCR']
        if index % 2 != 0 or (nx and xx):
            raise SyntaxError('SyntaxError')
        pairs = [(int(score), key)]
        # self.z_map[hash_key] = {key: int(score)}
        for i in range(0, index, 2):
            score1 = args[i]
            key1 = args[i + 1]
            pairs.append((int(score1), key1))
        if incr and len(pairs) > 0:
            raise SyntaxError('SyntaxError')

        # handle INCR Case
        # if incr:

        x = hash_key in self.hash_table
        if (x is False and xx) or (x is True and nx):
            if ch:
                if x:
                    return str(self.changed[hash_key])
                else:
                    return '0'
            else:
                if x:
                    return str(len(self.hash_table[hash_key]))
                else:
                    return '0'

        if hash_key not in self.hash_table:
            self.hash_table[hash_key] = SortedSet()
            self.changed[hash_key] = 0
            self.expire[hash_key] = None
            self.z_map[hash_key] = {}
        elif hash_key in self.hash_table and type(self.hash_table[hash_key]) != SortedSet:
            raise InvalidDataType('InvalidDataType')
        for score1, key1 in pairs:
            self.hash_table[hash_key].add((score1, key1))
            self.changed[hash_key] += 1
            self.z_map[hash_key][key1] = score1

        if ch:
            self.log(curr_time, 'ZADD', hash_key, str(score), key, *args)
            return str(self.changed[hash_key])
        else:
            self.log(curr_time, 'ZADD', hash_key, str(score), key, *args)
            return str(len(self.hash_table[hash_key]))

    def ZRANK(self, curr_time, hash_key, value):
        self.destroy_util(curr_time, hash_key)
        if hash_key in self.hash_table and value in self.z_map[hash_key]:
            x = self.hash_table[hash_key]
            if type(x) == SortedSet:
                index = self.search_index_util(x, self.z_map[hash_key][value])
                return str(index)
            else:
                raise InvalidDataType('WrongDataType')
        else:
            return str(None)

    def ZREVRANK(self, curr_time, hash_key, value):
        rank = self.ZRANK(curr_time, hash_key, value)
        if rank == 'None':
            return str(None)
        else:
            rank = int(rank)
            rev_rank = len(hash_key[value]) - rank - 1
            return str(rev_rank)


    def ZRANGE(self, curr_time, hash_key, start_index, end_index, *args):
        self.destroy_util(curr_time, hash_key)
        if hash_key in self.hash_table:
            ss = self.hash_table[hash_key]
            if type(ss) == SortedSet:
                if int(start_index) < 0:
                    temp = abs(int(start_index))
                    start_index = len(ss) - temp
                if int(end_index) < 0:
                    temp = abs(int(end_index))
                    end_index = len(ss) - temp
                if int(start_index) <= int(end_index) <= len(ss) - 1:
                    ans = []
                    s = ''
                    if len(args) == 1 and args[0].lower() == 'withscores':
                        for i in range(int(start_index), int(end_index) + 1):
                            ans.append(' '.join(map(str, ss[i])))
                            # for a, b in ans:
                            #     s += str(a) + " " + str(b) + ", "
                        s = ', '.join(ans)
                    elif len(args) == 0:
                        for i in range(int(start_index), int(end_index) + 1):
                            ans.append(ss[i][1])
                            # for a in ans:
                            #     s += str(a) + ", "
                        s = ', '.join(ans)
                    else:
                        raise SyntaxError('SyntaxError')
                    return s
                else:
                    raise InvalidFormat('WrongFormat')
            else:
                raise InvalidDataType('WrongDataType')
        else:
            return str(None)

    def ZREVRANGE(self, curr_time, hash_key, start_index, end_index, *args):
        self.destroy_util(curr_time, hash_key)
        if hash_key in self.hash_table:
            ss = self.hash_table[hash_key]
            if type(ss) == SortedSet:
                if int(start_index) < 0:
                    temp = abs(int(start_index))
                    start_index = len(ss) - temp
                if int(end_index) < 0:
                    temp = abs(int(end_index))
                    end_index = len(ss) - temp
                if int(start_index) <= int(end_index) <= len(ss) - 1:
                    ans = []
                    s = ''
                    n = len(ss)
                    start, stop = n - int(start_index) - 1, n - int(end_index) - 1
                    if len(args) == 1 and args[0].lower() == 'withscores':

                        for i in range(start, stop - 1, -1):
                            ans.append(' '.join(map(str, ss[i])))
                            # for a, b in ans:
                            #     s += str(a) + " " + str(b) + ", "
                        s = ', '.join(ans)
                    elif len(args) == 0:
                        for i in range(start, stop - 1, -1):
                            ans.append(ss[i][1])
                            # for a in ans:
                            #     s += str(a) + ", "
                        s = ', '.join(ans)
                    else:
                        raise SyntaxError('SyntaxError')
                    return s
                else:
                    raise InvalidFormat('WrongFormat')
            else:
                raise InvalidDataType('WrongDataType')
        else:
            return str(None)
