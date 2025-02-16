import threading, time

def task(name):
    print(f"Задача {name} началась\n")
    time.sleep(2)
    print(f"\nЗадача {name} завершена")

for i in range(5):
    t = threading.Thread(target=task, args=(f"Поток {i+1}",))
    t.start()
