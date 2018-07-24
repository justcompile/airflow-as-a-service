import time
import random
import threading

from reprint import output


def some_op(index=0):
    LENGTH = 2
    global output_list
    now = 0
    while now < LENGTH:
        if now == 1:
            message = 'done'
        else:
            message = ''
        output_list[index] = "My Service {}...{}".format(
            index,
            message
        )
        now += 1
        time.sleep(random.randint(2, 10))

with output(output_type="list", initial_len=5, interval=0) as output_list:
    pool = []
    for i in range(5):
        t = threading.Thread(target=some_op, args=(i,))
        t.start()
        pool.append(t)
    [t.join() for t in pool]
