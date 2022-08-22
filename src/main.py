import multiprocessing as mp
import handTracking
import sandbox
import time

# initialize multiprocessing
if __name__ == '__main__':
    q = mp.Manager().Queue()

    producer = mp.Process(target=handTracking.trackHands, args=(q,))
    consumer = mp.Process(target=sandbox.game_loop, args=(q,))

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()
