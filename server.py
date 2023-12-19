import os
import subprocess
import time
import threading
import sys
from queue import Queue, Empty

def read_output(queue, process):
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
            queue.put(output.strip())

def start_minecraft_server():
    server_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(server_directory)
    command = 'java -Xmx16G -Xms16G -jar "server.jar" nogui'

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    output_queue = Queue()

    output_thread = threading.Thread(target=read_output, args=(output_queue, process))
    output_thread.start()
    while True:
        try:
            # Non-blocking check for new output in the queue
            output = output_queue.get_nowait()
            # print(output)
        except Empty:
            time.sleep(0.1)
        