import sys

UP = {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'}

for s in sys.stdin:
    s = s.rstrip()
    print repr(s)
    for c in s:
        if c not in UP:
            sys.stdout.write(c)
    for c in s:
        if c in UP:
            sys.stdout.write(c)
