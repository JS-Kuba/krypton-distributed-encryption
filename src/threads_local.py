from encryption.file_encryptor import FileEncryptor
import threading
import queue

def encrypt_blocks(blocks, results_queue):
    while True:
        # Get the next string to reverse from the queue
        try:
            block = blocks.get(block=False)
        except queue.Empty:
            # If the queue is empty, the worker thread is done
            break

        # Reverse the string and add it to the results queue
        results_queue.put(fe.encrypt_block(block['data']))

def encrypt_blocks_multithreaded(blocks_list, num_threads):
    # Create a queue to hold the input strings and a queue to hold the reversed strings
    input_queue = queue.Queue()
    results_queue = queue.Queue()

    # Add the input strings to the queue
    for block in blocks_list:
        input_queue.put(block)

    # Create the worker threads
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=encrypt_blocks, args=(input_queue, results_queue))
        threads.append(thread)
        thread.start()

    # Wait for the worker threads to finish
    for thread in threads:
        thread.join()

    # Collect the reversed strings from the results queue
    reversed_strings = []
    while not results_queue.empty():
        reversed_strings.append(results_queue.get())

    return reversed_strings

if __name__ == '__main__':
    fe = FileEncryptor()
    input_file_path = 'data/crime-and-punishment.txt'
    blocks_list = fe.split_file_to_list(input_file_path)

    num_threads = 3
    encrypted_blocks = encrypt_blocks_multithreaded(blocks_list, num_threads)
    print("Blocks: " + str(len(blocks_list)))
    print("Encrypted blocks: " + str(len(encrypted_blocks)))
