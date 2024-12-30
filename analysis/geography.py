import pandas as pd
import numpy as np
import math
import re

currency_path = 'data/currency.csv'
currency_df = pd.read_csv(currency_path)


def filter_prof(df: pd.DataFrame, prof: str) -> pd.DataFrame:
    prof_escaped = re.escape(prof)
    return df[df['name'].str.lower().str.contains(prof_escaped.lower())]


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


def get_area_salary(df: pd.DataFrame) -> dict:
    df = df.copy()

    total_vacancies = len(df)
    qualified_cities = df['area_name'].value_counts()[
        df['area_name'].value_counts() >= total_vacancies * 0.01].index
    df_filtered = df[df['area_name'].isin(qualified_cities)]

    salary_levels = df_filtered.groupby('area_name')['salary'].mean().nlargest(10).astype(int).reset_index()
    sorted_salary_levels = salary_levels.sort_values(by=['salary', 'area_name'], ascending=[False, True])
    result_df = sorted_salary_levels.set_index('area_name')['salary']

    return result_df.to_dict()


def get_area_count(df: pd.DataFrame) -> dict:
    df = df.copy()

    total_vacancies = len(df)
    threshold = math.floor(total_vacancies * 0.01)
    qualified_cities = df['area_name'].value_counts()[
        df['area_name'].value_counts() >= threshold].index
    df_filtered = df[df['area_name'].isin(qualified_cities)]

    share_level = (df_filtered['area_name'].value_counts() / total_vacancies).reset_index()

    sorted_share_level = share_level.sort_values(by=['count', 'area_name'], ascending=[False, True])
    sorted_share_level['count'] = sorted_share_level['count'].round(4)

    result_df = sorted_share_level.set_index('area_name')['count'].nlargest(10)

    return result_df.to_dict()


def main():
    vacancies_path = 'data/vacancies.csv'

    df = pd.read_csv(vacancies_path)
    df['published_at'] = pd.to_datetime(df['published_at'], utc=True)
    print(df.head())

    df['salary'] = np.nanmean(df[['salary_from', 'salary_to']], axis=1)
    df['salary'] = df.apply(convert_salary, axis=1)
    df = df[df['salary'] < 10000000]

    prof_keywords = ['c++', 'с++']
    df_for_prof = df[df['name'].str.lower().str.contains('|'.join(prof_keywords))]
    print(df_for_prof.head())

    area_salary_all = get_area_salary(df)
    area_count_all = get_area_count(df)

    area_salary_prof = get_area_salary(df_for_prof)
    area_count_prof = get_area_count(df_for_prof)

    area_salary_all_df = pd.DataFrame(list(area_salary_all.items()), columns=['area_name', 'average_salary'])
    area_salary_all_df.to_csv('data/area_salary_all.csv', index=False)

    area_share_all_df = pd.DataFrame(list(area_count_all.items()), columns=['area_name', 'vacancy_count'])
    area_share_all_df.to_csv('data/area_count_all.csv', index=False)

    area_salary_prof_df = pd.DataFrame(list(area_salary_prof.items()), columns=['area_name', 'average_salary'])
    area_salary_prof_df.to_csv('data/area_salary_prof.csv', index=False)

    area_share_prof_df = pd.DataFrame(list(area_count_prof.items()), columns=['area_name', 'vacancy_count'])
    area_share_prof_df.to_csv('data/area_count_prof.csv', index=False)

    print("Data exported to CSV files successfully.")


if __name__ == "__main__":
    main()
