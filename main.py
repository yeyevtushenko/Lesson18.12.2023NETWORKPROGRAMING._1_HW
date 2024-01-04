import threading
import random
import math
import os

def fill_file_thread(file_path, size, fill_event):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write('\n'.join(str(random.randint(1, 10)) for _ in range(size)))
        fill_event.set()
    else:
        print(f"Файл {file_path} вже існує. Введіть 'Y' для використання існуючого файлу або 'N' для створення нового.")
        choice = input().strip().lower()
        if choice == 'y':
            fill_event.set()
        elif choice == 'n':
            with open(file_path, 'w') as file:
                file.write('\n'.join(str(random.randint(1, 10)) for _ in range(size)))
            fill_event.set()
        else:
            print("Невірний вибір. Використовується існуючий файл.")
            fill_event.set()

def find_primes_thread(file_path, primes_result, fill_event, primes_event):
    fill_event.wait()
    primes = []
    with open(file_path, 'r') as file:
        numbers = [int(line) for line in file.readlines()]
        for num in numbers:
            if is_prime(num):
                primes.append(num)
    primes_result.extend(primes)
    primes_event.set()

    # Збереження результатів пошуку у файл
    with open("primes_result.txt", 'w') as primes_file:
        primes_file.write('\n'.join(map(str, primes)))

def find_factorials_thread(file_path, factorials_result, fill_event, factorials_event):
    fill_event.wait()
    numbers = [int(line.strip()) for line in open(file_path, 'r')]
    for num in numbers:
        factorial_result = math.factorial(num)
        factorials_result.append((num, factorial_result))
        print(f"Факторіал числа {num}: {factorial_result}")

    factorials_event.set()

    # Збереження результатів пошуку у файл
    with open("factorials_result.txt", 'w') as factorials_file:
        factorials_file.write('\n'.join(f"{num}: {factorial}" for num, factorial in factorials_result))

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    file_path = input("Введіть шлях до файлу: ")

    primes_result = []
    factorials_result = []

    fill_event = threading.Event()
    primes_event = threading.Event()
    factorials_event = threading.Event()

    if not os.path.exists(file_path):
        print(f"Файл {file_path} не існує. Він буде створений.")
        with open(file_path, 'w') as file:
            pass

    fill_thread = threading.Thread(target=fill_file_thread, args=(file_path, 10, fill_event))
    primes_thread = threading.Thread(target=find_primes_thread, args=(file_path, primes_result, fill_event, primes_event))
    factorials_thread = threading.Thread(target=find_factorials_thread,
                                         args=(file_path, factorials_result, fill_event, factorials_event))

    fill_thread.start()
    primes_thread.start()
    factorials_thread.start()

    fill_thread.join()
    primes_thread.join()
    factorials_thread.join()

    print(f"Прості числа: {primes_result}")
    print(f"Факторіали: {factorials_result}")

    print(f"Статистика:")
    print(f"Кількість простих чисел: {len(primes_result)}")
    print(f"Кількість обчислених факторіалів: {len(factorials_result)}")
