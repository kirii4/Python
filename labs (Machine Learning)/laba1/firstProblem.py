import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats


def load_data(file_path):
    return pd.read_csv(file_path)


def check_missing_values(data):
    print("Пропуски в данных:")
    print(data.isnull().sum())


def check_distribution_outliers(data):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='price', data=data)
    plt.yscale('log')
    plt.title('Boxplot для цен')
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.histplot(data['price'], bins=30, kde=True)
    plt.title('Гистограмма цен')
    plt.xlabel('Цена')
    plt.ylabel('Частота')
    plt.show()


def fill_missing_values(data):
    data['avg_rating'] = data['avg_rating'].fillna(data['avg_rating'].mean())
    data['review_count'] = data['review_count'].fillna(data['review_count'].mean())


def handle_outliers(data):
    median_price = data['price'].median()
    data.loc[data['price'] > 1000, 'price'] = median_price


def create_pivot_table(data):
    pivot_table = pd.pivot_table(data, index=['brand', 'model'], values=['price', 'avg_rating', 'review_count'],
                                 aggfunc={'price': 'mean', 'avg_rating': 'mean', 'review_count': 'sum'})
    return pivot_table


def main():
    file_path = 'D:/study/6 term/МО/laba1/nike.csv'

    data = load_data(file_path)

    check_missing_values(data)

    check_distribution_outliers(data)

    fill_missing_values(data)

    handle_outliers(data)
    pivot_table = create_pivot_table(data)
    print(pivot_table)


if __name__ == "__main__":
    main()
