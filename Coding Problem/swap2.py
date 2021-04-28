n = int(input())
arr = list(map(int, input().split()))
for i in range(n):
    if arr[i] == 1:
        init = i
        break
for j in range(n):
    if arr[n-j-1] == 1:
        endi = n-j-1
        break

finalarr = arr[init:endi]
swaps = 0
for elem in finalarr:
    if elem == 0:
        swaps += 1

print("Swaps Required:",swaps)