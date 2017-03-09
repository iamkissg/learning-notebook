import sys
from collections import Counter

nob = [bin(i).count("1") for i in range(2000001)]

while True:
    line = raw_input().split()
    l, r, m = int(line[0]), int(line[1]), int(line[2])
    non = Counter(nob[l:r+1])
    print(non[m] if m in non else -1)
