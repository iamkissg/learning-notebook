import sys
UP = {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'}

for s in sys.stdin:
    s = s.rstrip('\n')
    length = len(s)
    sum = 0
    for i in range(length):
        if s[i] in UP:
            sum += 1
    for j in range(sum):
        for i in range(length):
            if s[i] in UP:
                s = s[:i] + s[i+1:] + s[i:i+1]
                break
    print s
