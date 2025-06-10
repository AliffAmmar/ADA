import csv
import pandas as pd
import numpy as np
import heapq as hq

file_path=(r'C:\Users\22002\OneDrive\Desktop\UM\Sem 4\Algorithm &\Assignment\Moira_Market_Items.csv')
df=pd.read_csv(file_path)
filtered_df = df[(df["Price"] <= 800) & (df["Durability"] >= 85)]

array = filtered_df.to_numpy()
array = array.tolist()
for i in range(0,len(array),1):
    array[i][4]= int(array[i][4]*100)


def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left][-1] < arr[largest][-1]:
        largest = left

    if right < n and arr[right][-1] < arr[largest][-1]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def buildHeap(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)


def heapSort(arr):
    n = len(arr)
    buildHeap(arr)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0] 
        heapify(arr, i, 0)

if __name__ == '__main__':
    heapSort(array)
    print("[Stall ID, Item Name, Price, Durability, Compatibility]")
    for i in range(0,len(array),1):
        array[i][4]=float(array[i][4]/100)

    for row in array:
        print(row)