from sortedcontainers import SortedSet
s = SortedSet()
s.add((1981, 'Brad'))
s.add((1975, 'John'))
s.add((1990, 'Mike'))
s.add((1990, 'Kate'))
s.add((1990, 'ABC'))

print(s)
s = s[::-1]
print(s)
