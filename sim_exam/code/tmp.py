while 1:
  num = int(raw_input())
  str = raw_input()
  arr = str.split()
  if len(arr)==num:
    sort_arr = sorted(arr,key=lambda x:int(x))
    start = 0
    for i in range(num):
      if not arr[i]==sort_arr[i]:
        start = i
        break
    end = num-1
    for i in range(num)[::-1]:
      if not arr[i]==sort_arr[i]:
        end = i
        break
    m=start
    n=end
    while m<=end and n>=start:
      if not arr[m]==sort_arr[n]:
        print "no"
        exit(0)
      m = m+1
      n = n-1
    print "yes"
