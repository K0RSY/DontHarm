import time

start_time = time.time()

while 1:
    time.sleep(1)

    end_time = time.time()

    print(end_time - start_time)

    if end_time - start_time >= 10:
        break

print("Конец")
