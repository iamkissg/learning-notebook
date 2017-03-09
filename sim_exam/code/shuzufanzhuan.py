
def isASC(l):
    for i in range(1, len(l)):
        if l[i] < l[i-1]:
            return False
    return True

def findTurningPoint(l):
    a1, a2 = 0, len(l)
    asc =  True
    for i in range(1, len(l)):
        if asc:
            if l[i] < l[i-1]:
                a1 = i - 1
                asc = False
        else:
            if l[i] > l[i-1]:
                a2 = i
                break
    return (a1, a2)

while True:
    n = int(raw_input())
    l = raw_input().split()
    if isASC(l):
        print("yes")
    else:
        a1, a2 = findTurningPoint(l)
        l1 = l[:a1]
        l2 = list(reversed(l[a1:a2]))
        l3 = l[a2:]
        print(l1)
        print(l2)
        print(l3)
        print("yes" if isASC(l1 + l2 + l3) else "no")

