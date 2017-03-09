import sys

l = []

for n in range(100000):
    tmp = int(n*(n+1)/2)
    l.append((tmp,tmp - 2*(n-1)))

for line in sys.stdin:
    line = int(line.strip())
    for i in range(len(l)):
        if l[i][0] == line:
            print l[i][1]
            break
        if l[i][0] < line:
            continue
        print l[i-1][1] + line - l[i-1][0]
        break
