import threading

def test():
    i = 0
    while i < 10000000000:
        print(i)
        i += 1

def test2():
    i = 0
    while True:
        print(i)
        i += 1

def test3():
    i = 0
    while True:
        print(i)
        i += 1

if __name__ == "__main__":
    t = threading.Thread(target=test)
    t2 = threading.Thread(target=test2)
    t3 = threading.Thread(target=test3)
    t4 = threading.Thread(target=test)
    t.start()
    t2.start()
    t3.start()
    t4.start()
    print("Done")