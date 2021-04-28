n = int(input())
arr = list(map(int, input().split()))

arr1_len = 0
arr1_i = 0
arr1_e = 0

for i in range(n):
    if arr[i]==1:
        arr1_i = i
        break

for i in range(n):
    if arr[i]==1:
        arr1_len += 1

a  = 0
for i in range(n):
    if arr[i] == 1:
        a += 1

    if a == arr1_len:
        arr1_e = i
        break

arr1 = arr[arr1_i:arr1_e+1]
swaps = 0

for i in arr1:
    if i==0:
        swaps +=1

#print(arr1_i, arr1_e)
#print(arr1)
print(swaps)