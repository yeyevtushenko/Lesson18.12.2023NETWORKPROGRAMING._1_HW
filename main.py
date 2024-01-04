import threading
import random
import queue

def fill_list_thread(lst, size, fill_event):
    lst.extend(random.randint(1, 100) for _ in range(size))
    fill_event.set()

def calculate_sum_thread(lst, sum_result, fill_event, sum_event):
    fill_event.wait()
    result = sum(lst)
    sum_result.append(result)
    sum_event.set()

def calculate_average_thread(lst, avg_result, fill_event, avg_event):
    fill_event.wait()
    result = sum(lst) / len(lst) if len(lst) > 0 else 0
    avg_result.append(result)
    avg_event.set()

if __name__ == "__main__":
    random_list = []
    sum_result = []
    avg_result = []

    fill_event = threading.Event()
    sum_event = threading.Event()
    avg_event = threading.Event()

    fill_thread = threading.Thread(target=fill_list_thread, args=(random_list, 30, fill_event))
    sum_thread = threading.Thread(target=calculate_sum_thread, args=(random_list, sum_result, fill_event, sum_event))
    avg_thread = threading.Thread(target=calculate_average_thread, args=(random_list, avg_result, fill_event, avg_event))

    fill_thread.start()
    sum_thread.start()
    avg_thread.start()

    sum_event.wait()
    avg_event.wait()

    print(f"Випадковий список: {random_list}")
    print(f"Cума: {sum_result[0]}")
    print(f"Середнє: {avg_result[0]}")
