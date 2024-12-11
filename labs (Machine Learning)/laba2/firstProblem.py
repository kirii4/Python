import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

electric_activity = np.array([0, 38.5, 59, 97.4, 119.2, 129.5, 198.7, 248.7, 318, 438.5])
vascular_permeability = np.array([19.5, 15, 13.5, 23.3, 6.3, 2.5, 13, 1.8, 6.5, 1.8])

correlation_coefficient, p_value = stats.pearsonr(electric_activity, vascular_permeability)
print("Коэффициент корреляции:", correlation_coefficient)
print("p-value:", p_value)

slope, intercept, r_value, p_value, std_err = stats.linregress(electric_activity, vascular_permeability)
print("Уравнение регрессии: y =", slope, "x +", intercept)

plt.scatter(electric_activity, vascular_permeability, label='Данные')
plt.plot(electric_activity, slope * electric_activity + intercept, color='red', label='Линия регрессии')
plt.xlabel('Электрическая активность сетчатки')
plt.ylabel('Проницаемость сосудов сетчатки')
plt.title('Зависимость проницаемости сосудов сетчатки от электрической активности')
plt.legend()
plt.show()