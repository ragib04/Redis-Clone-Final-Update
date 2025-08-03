import time
from sortedcontainers import SortedSet
hash_table = {}
expire = {}
exp_queue = SortedSet()
changed = {}

print(CustomError.__repr__())

def SET(hash_key, hash_val, *args):
    # LOG

    # self.destroy_util(hash_key)
    x = hash_key in hash_table
    ex, px, xx, nx, keepttl = [False] * 5
    ind = 0
    index = len(args)
    kwargs = {}
    for i in range(len(args)):
        if args[i].lower() == 'ex':
            ex = True
            kwargs['EX'] = int(args[i + 1])
        elif args[i].lower() == 'px':
            px = True
            kwargs['NX'] = int(args[i + 1])
        elif args[i].lower() == 'xx':
            xx = True
        elif args[i].lower() == 'nx':
            nx = True
        elif args[i].lower() == 'keepttl':
            keepttl = True
    if (x is False and xx) or (x is True and nx):
        return None
    # Make entry in both expiry table and hash table
    if (ex and px) or (nx and xx):
        raise CustomError('Invalid Request')
    if keepttl:
        if ex or nx:
            raise CustomError('InvalidRequest')
        else:
            if hash_key in hash_table and expire[hash_key] is not None:
                hash_table[hash_key] = str(hash_val)
            else:
                hash_table[hash_key] = str(hash_val)
                expire[hash_key] = None
            print(hash_table)
            print(exp_queue)
            print(expire)
            return 'OK'
    else:
        hash_table[hash_key] = str(hash_val)
        old_exp = None
        if hash_key in expire:
            old_exp = expire[hash_key]
        expire[hash_key] = None
        if old_exp is not None:
            # Since no KEEPTTL and old expiration time is not None so we remove it from exp_queue
            # search_util((old_exp, hash_key))
            pass
        if ex:
            exp_time = round(time.perf_counter(), 4) + kwargs['EX']
            expire[hash_key] = exp_time
            # Remove then Add in Queue
            exp_queue.add((exp_time, hash_key))
        elif px:
            seconds = round((kwargs['PX'] / 1000), 4)
            exp_time = round(time.perf_counter(), 4) + seconds
            expire[hash_key] = exp_time
            # Remove and Add in Queue
            exp_queue.add((exp_time, hash_key))
        print(hash_table)
        print(exp_queue)
        print(expire)
        return 'OK'


query1 = 'mykey "hellow"'
query2 = 'anotherkey "will expire in a minute" ex 60'

print(SET(*query1.split(' ')))
print(SET(*query2.split(' ')))
