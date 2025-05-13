#2 часть – усложнить написанную программу,
# введя по своему усмотрению в условие минимум одно ограничение на характеристики объектов
# (которое будет сокращать количество переборов) и целевую функцию для нахождения оптимального  решения.
#Вариант 16. В пассажирском поезде 9 вагонов. Выведите все возможные варианты рассадки в поезде 4 человек, при условии,
# что все они должны ехать в различных вагонах?

import itertools #набор функций для работы с итерируемыми объектами
import time
import random

N, K = 9, 4  # 9 вагонов, 4 человека

# Случайные параметры вагонов
random.seed(15)
restricted = {(1, 2), (3, 4), (7, 8)}  # Запрещенные соседние комбинации (вагоны не могут находится рядом)
comfort = {i: random.randint(1, 10) for i in range(1, N+1)}  #Генератор словаря из рандомных значений (от 1 до 10) количества N. (Уровень комфорта вагонов)
#             (возвращает целое число из заданного диапазона)


def measure_time(func, N, K):
    start = time.perf_counter() # Запись начального времени
    result = func(N, K)
    end_time = time.perf_counter() # Запись конечного времени
    return result, end_time - start 

# Алгоритмический метод с ограничениями
def algorithmic_method(N, K):
    result = []
    for v1 in range(1, N+1): #каждый цикл отвечает за выбор вагона для одного конкретного человека
        for v2 in range(1, N+1):
            if v2 == v1 or (v1, v2) in restricted: # Вагоны не должны совпадать и не должны находится рядом
                continue
            for v3 in range(1, N+1):
                if v3 in {v1, v2} or (v2, v3) in restricted:
                    continue
                for v4 in range(1, N+1):
                    if v4 in {v1, v2, v3} or (v3, v4) in restricted:
                        continue
                    result.append((v1, v2, v3, v4))
    return result

def itertools_method(N, K):
    all_perm = itertools.permutations(range(1, N+1), K)  #Создает последовательность чисел от 1 до N, Генерирует все перестановки из N элементов по K
    permutations = [] # Вагоны не должны совпадать - permutations исключает повторения
    
    for p in all_perm:   # Перебираем все перестановки
        has_bad_pair = False
        
        # Проверяем соседние пары
        for i in range(K-1):
            if (p[i], p[i+1]) in restricted: # Вагоны не должны находится рядом
                has_bad_pair = True
                break  # Дальше проверять нет смысла
        
        # Если все пары разрешены
        if not has_bad_pair:
            permutations.append(p)
    
    return permutations

# Целевая функция для оптимизации
def comfort_score(combination): #Принимает на вход кортеж с номерами вагонов
    return sum(comfort[wagon] for wagon in combination) # Для каждого вагона берется комфорт и суммируем
    # Возвращает суммарный комфорт всех вагонов в этой комбинации.

# Замер времени и расчеты
result_algo, time_algo = measure_time(algorithmic_method, N, K)
result_itertools, time_itertools = measure_time(itertools_method, N, K)

# Поиск оптимального решения
optimal_algo = max(result_algo, key=comfort_score) #Для каждой комбинации вычисляется comfort_score, выбирается комбинация с максимальным комфортом.
optimal_itertools = max(result_itertools, key=comfort_score)
print(f"Уровни комфорта вагонов: {comfort}")
print(f'Алгоритмический метод: {len(result_algo)} вариантов, время: {time_algo:.6f} сек.')
print(f'Метод itertools: {len(result_itertools)} вариантов, время: {time_itertools:.6f} сек.')
print(f'Оптимальная рассадка (алгоритм): {optimal_algo}, комфорт: {comfort_score(optimal_algo)}')
print(f'Оптимальная рассадка (itertools): {optimal_itertools}, комфорт: {comfort_score(optimal_itertools)}')
print(f'Все перестановки: {result_itertools[:]}')