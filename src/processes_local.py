from encryption.file_encryptor import FileEncryptor
import multiprocessing as mp
import time
import queue

def encrypt_blocks(blocks, results_queue, fe):
    while True:
        try:
            block = blocks.get(block=True, timeout=1)  # Add timeout of 1 second
        except queue.Empty:
            break
        print(f"Encrypting block")
        encrypted_block = fe.encrypt_block(block)
        print(f"Finished encrypting block")
        results_queue.put(encrypted_block)
        print(f"Added encrypted block to results queue")

def encrypt_blocks_multiprocessed(blocks_list, num_processes, fe):
    manager = mp.Manager()
    input_queue = manager.Queue()
    results_queue = manager.Queue()

    for block in blocks_list:
        input_queue.put(block)

    processes = []
    for _ in range(num_processes):
        process = mp.Process(target=encrypt_blocks, args=(input_queue, results_queue, fe))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    return results_queue

if __name__ == '__main__':
    fe = FileEncryptor()
    input_file_path = 'data/crime-and-punishment.txt'
    blocks_list = fe.split_file_to_list(input_file_path)

    num_processes = 3
    start_time = time.time()
    encrypted_blocks = encrypt_blocks_multiprocessed(blocks_list, num_processes, fe)
    end_time = time.time()
    execution_time = end_time - start_time

    print("Execution time:", execution_time, "seconds")
    print("Blocks:", len(blocks_list))
    print("Encrypted blocks:", encrypted_blocks.qsize())

    decrypted_blocks = []
    while not encrypted_blocks.empty():
        block = encrypted_blocks.get()
        decrypted_block = fe.decrypt_block(block)
        decrypted_blocks.append(decrypted_block)

    sorted_list = sorted(decrypted_blocks, key=lambda x: x[0])

    print(sorted_list)
