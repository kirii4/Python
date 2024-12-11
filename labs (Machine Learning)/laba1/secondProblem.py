import numpy as np
import matplotlib.pyplot as plt

def f(x, c):
    return np.power(np.power(np.abs(2*x - c), 2), 1/5) + 0.567


def main():
    c_values = np.arange(-10, -1, 0.25)
    x = 3.67

    f_values = f(x, c_values)

    for c, f_value in zip(c_values, f_values):
        print(f"c = {c}, f(x) = {f_value}")

    max_value = np.max(f_values)
    min_value = np.min(f_values)
    mean_value = np.mean(f_values)
    array_length = len(f_values)

    if array_length % 2 == 0:
        sorted_indices = np.argsort(f_values)[::-1]
    else:
        sorted_indices = np.argsort(f_values)

    sorted_f_values = f_values[sorted_indices]

    plt.plot(c_values, f_values, marker='', label='f(x)')
    plt.axhline(y=mean_value, color='r', linestyle='--', label='Среднее значение')
    plt.xlabel('c')
    plt.ylabel('f(x)')
    plt.title('Изменение значений функции f(x)')
    plt.legend()
    plt.grid(True)
    plt.show()

    print(f"Наибольшее значение: {max_value}")
    print(f"Наименьшее значение: {min_value}")
    print(f"Среднее значение: {mean_value}")
    print(f"Количество элементов массива: {array_length}")
    print("Отсортированный массив значений функции:")
    for c, f_value in zip(c_values[sorted_indices], sorted_f_values):
        print(f"c = {c}, f(x) = {f_value}")


if __name__ == "__main__":
    main()