import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt

# Загрузка данных из файла
df = pd.read_csv("sitka_weather_2014.csv")

# Удаление столбца 'Date', так как он не несет информации для обучения модели
df.drop('AKST', axis=1, inplace=True)

df.columns = df.columns.str.lower().str.replace(' ', '')

# Замена пустых значений на 0
df.fillna(0, inplace=True)

# Преобразование целевой переменной в числовой формат
df['events'] = df['events'].astype(str)

# Преобразование целевой переменной в числовой формат
label_encoder = LabelEncoder()
df['events'] = label_encoder.fit_transform(df['events'])

# Разделение данных на признаки (X) и целевую переменную (y)
X = df.drop('events', axis=1)
y = df['events']

# Разделение данных на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание и обучение модели дерева решений
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Оценка точности модели на тестовом наборе
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Построение матрицы сходства
conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(conf_matrix)

# Важность признаков
feature_importances = pd.DataFrame(model.feature_importances_, index=X.columns, columns=['Importance'])
print("Feature Importances:")
print(feature_importances)

corr_matrix = df.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", annot_kws={"size": 10})
plt.title("Correlation Matrix")
plt.show()

# Построение матрицы сходства
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, cmap='Blues', fmt="d", annot_kws={"size": 10})
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()