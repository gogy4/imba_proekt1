import pandas as pd
from collections import Counter
import numpy as np
import math
import re

currency_path = 'data/currency.csv'
currency_df = pd.read_csv(currency_path)


def filter_prof(df: pd.DataFrame, prof_list: list) -> pd.DataFrame:
    pattern = '|'.join(re.escape(prof) for prof in prof_list)
    return df[df['name'].str.lower().str.contains(pattern.lower())]


def convert_salary(row):
    currency = row['salary_currency']
    if pd.isna(currency) or currency not in currency_df.columns:
        return row['salary']

    vacancy_date = row['published_at'].strftime('%Y-%m')
    rate_rows = currency_df[currency_df['date'] == vacancy_date]

    if rate_rows.empty:
        return row['salary']

    rate_row = rate_rows.iloc[0]
    rate_column = currency.upper()

    if rate_column not in rate_row.index:
        return row['salary']

    rate = rate_row[rate_column]
    return row['salary'] * rate


def get_dynamic_salary(df: pd.DataFrame) -> dict:
    df = df.copy()

    df['year'] = df['published_at'].dt.year

    city_avg_salary = df.groupby('year')['salary'].mean().reset_index()

    full_range_years = pd.Series(range(2017, 2024), name='year')

    city_avg_salary = pd.merge(full_range_years, city_avg_salary, how='left', on='year').fillna(0)

    city_avg_salary['salary'] = city_avg_salary['salary'].astype(int)

    result_df = city_avg_salary.set_index('year')['salary'].to_dict()

    return result_df


def get_dynamic_count(df: pd.DataFrame) -> dict:
    df = df.copy()

    df['year'] = df['published_at'].dt.year

    df = df.groupby('year').size()

    full_range_years = pd.Series(range(2017, 2024), name='year')
    df = df.reindex(full_range_years, fill_value=0)

    return df.to_dict()


def main():
    vacancies_path = 'data/vacancies.csv'

    df = pd.read_csv(vacancies_path)
    df['published_at'] = pd.to_datetime(df['published_at'], utc=True)
    print(df.head())

    df['salary'] = np.nanmean(df[['salary_from', 'salary_to']], axis=1)
    df['salary'] = df.apply(convert_salary, axis=1)
    df = df[df['salary'] < 10000000]

    prof_list = ["C++", "с++", "c/c++", "cpp"]
    df_for_prof = filter_prof(df, prof_list)
    print(df_for_prof.head())

    dynamic_salary_all = get_dynamic_salary(df)
    dynamic_count_all = get_dynamic_count(df)

    dynamic_salary_prof = get_dynamic_salary(df_for_prof)
    dynamic_count_prof = get_dynamic_count(df_for_prof)

    dynamic_salary_all_df = pd.DataFrame(list(dynamic_salary_all.items()), columns=['year', 'average_salary'])
    dynamic_salary_all_df.to_csv('data/dynamic_salary_all.csv', index=False)

    dynamic_count_all_df = pd.DataFrame(list(dynamic_count_all.items()), columns=['year', 'vacancy_count'])
    dynamic_count_all_df.to_csv('data/dynamic_count_all.csv', index=False)

    dynamic_salary_prof_df = pd.DataFrame(list(dynamic_salary_prof.items()), columns=['year', 'average_salary'])
    dynamic_salary_prof_df.to_csv('data/dynamic_salary_prof.csv', index=False)

    dynamic_count_prof_df = pd.DataFrame(list(dynamic_count_prof.items()), columns=['year', 'vacancy_count'])
    dynamic_count_prof_df.to_csv('data/dynamic_count_prof.csv', index=False)

    print("Data exported to CSV files successfully.")


if __name__ == "__main__":
    main()
