import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

n = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
X = np.array([156, 165, 415, 894, 465, 163, 496, 131, 566, 561, 562, 354])
Y = np.array([526, 414, 561, 561, 456, 321, 648, 654, 321, 456, 464, 456])

mean_X = np.mean(X)
mean_Y = np.mean(Y)
numerator = np.sum((X - mean_X) * (Y - mean_Y))
denominator = np.sum((X - mean_X) ** 2)
b1 = numerator / denominator
b0 = mean_Y - b1 * mean_X

print("Коэффициенты уравнения регрессии:")
print("b0 =", b0)
print("b1 =", b1)

plt.scatter(X, Y, label='Данные')
plt.plot(X, b0 + b1*X, color='red', label='Линия тренда')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Корреляционное поле и линия тренда')
plt.legend()
plt.show()

n = len(X)
SSR = np.sum((b0 + b1 * X - Y) ** 2)
SE_b0 = np.sqrt(SSR / (n - 2) / np.sum((X - mean_X) ** 2))
SE_b1 = np.sqrt(SSR / (n - 2) / np.sum((X - mean_X) ** 2))

t_b0 = b0 / SE_b0
t_b1 = b1 / SE_b1

alpha = 0.05
t_critical = stats.t.ppf(1 - alpha / 2, n - 2)

print("t-статистика для b0:", t_b0)
print("t-статистика для b1:", t_b1)
print("Критическое значение t-статистики для alpha =", alpha, "и степеней свободы", n - 2, ":", t_critical)

if abs(t_b0) > t_critical:
    print("b0 является значимым коэффициентом")
else:
    print("b0 не является значимым коэффициентом")

if abs(t_b1) > t_critical:
    print("b1 является значимым коэффициентом")
else:
    print("b1 не является значимым коэффициентом")