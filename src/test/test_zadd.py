# def check(*args):
#     print(args)
#     print(len(args))
#     for key, val in enumerate(args):
#         print(key, val)
#
# s = 'A B C'
# check(*s.split(' '))

from sortedcontainers import SortedSet
hash_table = {}
expire = {}
exp_queue = SortedSet()
changed = {}
def ZADD(hash_key, score, key, *args):
    global hash_table, changed, expire
    # Log

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
        raise Exception('Syntax Error')
    pairs = [(score, key)]
    for i in range(0, index, 2):
        score = args[i]
        key = args[i + 1]
        pairs.append((score, key))
    if incr and len(pairs) > 0:
        raise Exception('Syntax Error')

    # handle INCR Case
    # if incr:

    x = hash_key in hash_table
    if (x is False and xx) or (x is True and nx):
        if ch:
            if x:
                return changed[hash_key]
            else:
                return 0
        else:
            if x:
                return len(hash_table[hash_key])
            else:
                return 0
    if hash_key not in hash_table:
        hash_table[hash_key] = SortedSet()
        changed[hash_key] = 0
        expire[hash_key] = None
    for score, key in pairs:
        hash_table[hash_key].add((int(score), key))
        changed[hash_key] += 1

    print(hash_table)

    if ch:
        print('In changed')
        return changed[hash_key]
    else:
        print('Not in changed')
        return len(hash_table[hash_key])


query1 = "myzset 2 two 3 three 4 four 5 five CH"
query2 = "mykey 2 two 3 three 4 four 5 five 6 Six 9 Nine 8 Eight CH"
query3 = "myzset 10 Ten 11 Eleven NX"
query4 = "myzset 2 abc 3 xyz 4 four 5 pqr"
query5 = "mykey 2 two 3 three 4 four 5 five 6 Six 9 Nine 8 Eight"
query6 = "myzset 10 Ten 11 Eleven"
print(ZADD(*query1.split(' ')))
print(ZADD(*query2.split(' ')))
print(ZADD(*query3.split(' ')))
print(ZADD(*query4.split(' ')))
print(ZADD(*query5.split(' ')))
print(ZADD(*query6.split(' ')))

