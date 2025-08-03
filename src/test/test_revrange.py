from sortedcontainers import SortedSet
s = SortedSet()
s.add((1, 'Brad'))
s.add((2, 'John'))
s.add((3, 'Mike'))
s.add((4, 'Kate'))
s.add((5, 'ABC'))
s.add((6, 'XYZ'))
s.add((7, 'PQR'))
hash_table = {'mykey': s}

def ZREVRANGE(hash_key, start_index, end_index, *args):
    if hash_key in hash_table:
        ss = hash_table[hash_key]
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
        return str(None)

print(ZREVRANGE('mykey', '-1', '6', 'withscores'))
