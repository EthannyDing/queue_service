import concurrent.futures
import threading
from queue import Queue
import random, time, logging, json
import socket


"""This script builds a prototype of creating a queue mechanism between Server - Client environment,
   In particular, main thread will be responsible for receiving requests from clients and 4 other threads
   will be used to do cleaning job."""


def request_receiver(queue, name):

    while True:
        conn, addr = s.accept()
        data = conn.recv(409600)
        data = json.loads(data.decode())
        queue.put(data)
        logging.info("New Request Received by %d", name)

def job_description(queue, name):
    """Pretend we're saving a number in the database."""

    logging.info("Worker %d activated for request.", name)
    while True:

        request = queue.get()
        if request:
            job_time = random.randint(5, 10)
            logging.info(
                "Worker %d received tm request: \n\t%s \n\trequests in queue: %d\n\tTime Cost: %d",
                name, request.get('Credential'), queue.qsize(), job_time
            )

            time.sleep(job_time)
            logging.info("Worker %d finishes job.", name)

        else:
            break

    logging.info("None signal received: Worker %d exiting", name)


def main():

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 6666))
    s.listen(20)

    queue = Queue()

    # with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    #     executor.submit(request_receiver, queue, 0)
    #     executor.submit(job_description, queue, 1)
    #     executor.submit(job_description, queue, 2)
    #     executor.submit(job_description, queue, 3)
    #     executor.submit(job_description, queue, 4)

    for index in range(1, 5):
        worker = threading.Thread(target=job_description, args=(queue, index))
        worker.start()

    SERVICE_ON = True
    logging.info("Main Thread: Service Ready.")

    while SERVICE_ON:

        conn, addr = s.accept()
        data = conn.recv(409600)
        data = json.loads(data.decode())
        queue.put(data)
        logging.info("Main: server received a request, %d requests in queue", queue.qsize())


if __name__ == "__main__":

    main()