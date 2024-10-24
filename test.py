import time
import numpy as np

start_time = time.time()
list_a = np.zeros(70000000)

i = 0
while i < 70000:
    list_a[i] = 5.139258
    i += 1
end_time = time.time()
print(end_time - start_time, '\n', list_a, list_a.size)

i = 0
start_time = time.time()
list_a = np.array([])
while i < 70000:
    list_a = np.append(list_a, 5.139258)
    i += 1
end_time = time.time()
print(end_time - start_time, '\n', list_a, list_a.size)
