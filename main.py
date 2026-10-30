import random
import sys
import time


sys.setrecursionlimit(200000)


def partition(arr: list[float], low: int, high: int, ascending: bool = True) -> int:
    """
    Функція партиціонування (розбиття масиву відносно півоти).
    За опорний елемент (pivot) обирається останній елемент підмасиву.
    """
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        # Якщо сортування за зростанням — шукаємо елементи <= pivot
        # Якщо сортування за спаданням — шукаємо елементи >= pivot
        condition = (arr[j] <= pivot) if ascending else (arr[j] >= pivot)

        if condition:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    # Ставимо півоту на її правильну позицію
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort_helper(arr: list[float], low: int, high: int, ascending: bool = True):
    """
    Рекурсивна допоміжна функція QuickSort.
    """
    if low < high:
        pi = partition(arr, low, high, ascending)
        quick_sort_helper(arr, low, pi - 1, ascending)
        quick_sort_helper(arr, pi + 1, high, ascending)


def quick_sort(arr: list[float], ascending: bool = True) -> list[float]:
    """
    Основний метод сортування QuickSort.
    Приймає масив дробових чисел та прапорець ascending:
    True  — сортування за зростанням;
    False — сортування за спаданням.
    """
    quick_sort_helper(arr, 0, len(arr) - 1, ascending)
    return arr


def is_sorted(arr: list[float], ascending: bool = True) -> bool:
    """
    Перевіряє, чи впорядкований масив за вказаним напрямком.
    Повертає True, якщо масив відсортований правильно, і False у протилежному випадку.
    """
    for i in range(len(arr) - 1):
        if ascending:
            if arr[i] > arr[i + 1]:
                return False
        else:
            if arr[i] < arr[i + 1]:
                return False
    return True


# --- Для порівняння з ПР №3 (Bubble Sort) ---
def bubble_sort(arr: list[float], ascending: bool = True) -> list[float]:
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            condition = (arr[j] > arr[j + 1]) if ascending else (arr[j] < arr[j + 1])
            if condition:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


# --- Тестування та порівняння продуктивності ---
if __name__ == "__main__":
    sizes = [1_000, 10_000, 100_000]

    print("=== ПЕРЕВІРКА КОРЕКТНОСТІ РОБОТИ QUICKSORT ===")
    test_arr = [3.14, -2.5, 7.8, 0.0, 1.2, -6.4, 9.9]
    print(f"Початковий масив: {test_arr}")

    # Тест за зростанням
    arr_asc = test_arr.copy()
    quick_sort(arr_asc, ascending=True)
    print(f"Відсортовано за зростанням: {arr_asc}")
    print(f"Перевірка is_sorted(ascending=True): {is_sorted(arr_asc, True)}\n")

    # Тест за спаданням
    arr_desc = test_arr.copy()
    quick_sort(arr_desc, ascending=False)
    print(f"Відсортовано за спаданням: {arr_desc}")
    print(f"Перевірка is_sorted(ascending=False): {is_sorted(arr_desc, False)}\n")

    print("=== БЕНЧМАРК ТА ПОРІВНЯННЯ ПРОДУКТИВНОСТІ ===")
    for size in sizes:
        # Генеруємо випадковий масив дробових чисел
        data = [random.uniform(-10000.0, 10000.0) for _ in range(size)]

        # --- Вимірювання QuickSort ---
        qs_data = data.copy()
        start = time.perf_counter()
        quick_sort(qs_data, ascending=True)
        end = time.perf_counter()
        qs_time = end - start
        sorted_ok = is_sorted(qs_data, ascending=True)

        print(f"Розмір масиву: {size:7,d} елементів")
        print(f"   QuickSort: {qs_time:.6f} сек | Правильно впорядковано: {sorted_ok}")

        # --- Вимірювання Bubble Sort (з ПР №3) ---
        # Для 100 000 елементів O(N^2) працюватиме надто довго (~кілька хвилин), тому обмежуємо
        if size <= 10_000:
            bs_data = data.copy()
            start = time.perf_counter()
            bubble_sort(bs_data, ascending=True)
            end = time.perf_counter()
            bs_time = end - start
            print(f"   BubbleSort: {bs_time:.6f} сек")
            print(f"   -> QuickSort швидший у {bs_time / qs_time:.1f} разів!")
        else:
            print("   BubbleSort: пропущено (O(N^2) надто повільне для 100,000 елементів)")

        print("-" * 50)