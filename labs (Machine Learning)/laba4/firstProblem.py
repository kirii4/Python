import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

# Загрузка данных из CSV файла
data = pd.read_csv("sitka_weather_2014.csv")

# Выбор признаков (фичей) для обучения модели
features = ['Max TemperatureF', 'Mean TemperatureF', 'Min TemperatureF', 'Max Dew PointF', 'MeanDew PointF',
            'Min DewpointF', 'Max Humidity', 'Mean Humidity', 'Min Humidity', 'Max Sea Level PressureIn',
            'Mean Sea Level PressureIn', 'Min Sea Level PressureIn', 'Max VisibilityMiles', 'Mean VisibilityMiles',
            'Min VisibilityMiles', 'Max Wind SpeedMPH', 'Mean Wind SpeedMPH', 'Max Gust SpeedMPH', 'CloudCover',
            'WindDirDegrees']

# Определение целевой переменной
target = 'Events'  # Здесь предполагается, что 'Events' является целевой переменной

# Извлечение фичей и целевой переменной
X = data[features]
y = data[target]

# Разделение данных на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание и обучение модели дерева решений
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Предсказание на тестовом наборе
y_pred = model.predict(X_test)

# Оценка точности модели
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Построение матрицы сходства
conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(conf_matrix)

# Интерпретация построенной модели
# Вывод важности признаков
importance = model.feature_importances_
feature_importance = pd.DataFrame({'Feature': features, 'Importance': importance})
print("Feature Importance:")
print(feature_importance)

# Вывод знаний, полученных из набора данных
# Здесь можно проанализировать важность различных факторов (фичей) влияющих на события погоды
