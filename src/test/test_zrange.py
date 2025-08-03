from sortedcontainers import SortedSet
hash_table = {'myzset': SortedSet([(2, 'abc'), (2, 'two'), (3, 'three'), (3, 'xyz'), (4, 'four'), (5, 'five'), (5, 'pqr'), (10, 'Ten'), (11, 'Eleven')]), 'mykey': SortedSet([(2, 'two'), (3, 'three'), (4, 'four'), (5, 'five'), (6, 'Six'), (8, 'Eight'), (9, 'Nine')])}

def ZRANGE(hash_key, start_index, end_index, *args):
    if hash_key in hash_table:
        ss = hash_table[hash_key]
        if type(ss) == SortedSet:
            if int(start_index) < 0:
                temp = abs(int(start_index))
                start_index = len(ss) - temp
            if int(end_index) < 0:
                temp = abs(int(end_index))
                end_index = len(ss) - temp
            print(ss)
            if int(start_index) <= int(end_index) <= len(ss) - 1:
                ans = []
                if len(args) == 1 and args[0].lower() == 'withscores':
                    for i in range(int(start_index), int(end_index) + 1):
                        ans.append(ss[i])
                elif len(args) == 0:
                    for i in range(int(start_index), int(end_index) + 1):
                        ans.append(ss[i][1])
                else:
                    raise Exception('Syntax Error')
                return ans
            else:
                raise Exception('WrongFormat')
        else:
            raise Exception('ZRangeOnlyPossibleWithZset')
    else:
        return None

query1 = 'myzset2 1 4 withscores'

print(ZRANGE(*query1.split(' ')))
