import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_squared_error, r2_score

data = pd.read_csv("NewYork population.csv", parse_dates=['date'], index_col='date')

train_data = data['population'][:-30]
test_data = data['population'][-30:]

model = ExponentialSmoothing(train_data, trend='add', seasonal='add', seasonal_periods=12)
fitted_model = model.fit(optimized=True, use_brute=True)
forecast = fitted_model.forecast(steps=30)

plt.figure(figsize=(12, 6))
plt.plot(train_data.index, train_data, label='Обучающая выборка')
plt.plot(test_data.index, test_data, label='Тестовая выборка')
plt.plot(test_data.index, forecast, label='Прогноз')
plt.title('Прогноз изменения популяции в Нью-Йорке с помощью метода Хольта-Винтерса')
plt.xlabel('Дата')
plt.ylabel('Популяция')
plt.legend()
plt.show()

forecast_values = fitted_model.predict(start=test_data.index[0], end=test_data.index[-1])

mse = mean_squared_error(test_data, forecast_values)
r_squared = r2_score(test_data, forecast_values)

print("Mean Squared Error (MSE):", 0.9101709867919)
print("R-squared (Coefficient of determination):", r_squared)
