import pandas as pd
from collections import Counter
import numpy as np
import re
import os


def get_all_skills(df: pd.DataFrame, year=None) -> list:
    if year is not None:
        df = df[df['year'] == year]

    skills = df['key_skills']
    skills = [str(skill).split("\n") for skill in skills.tolist()]
    return [skill for sublist_skills in skills for skill in sublist_skills if skill != 'nan']


def get_top_skills(all_skills: list) -> list:
    counter = Counter(all_skills)
    skills_with_count = [(skill, count) for skill, count in counter.items()]
    sorted_skills_with_count = sorted(skills_with_count, key=lambda x: x[1], reverse=True)
    return sorted_skills_with_count[:20]


def filter_prof(df: pd.DataFrame, prof: str) -> pd.DataFrame:
    prof_escaped = re.escape(prof)
    return df[df['name'].str.lower().str.contains(prof_escaped.lower())]


def export_to_csv(year: int, data: list, filename: str):
    df = pd.DataFrame(data, columns=['skill_name', 'count'])
    df['year'] = year
    print(df.head())
    df.to_csv(filename, index=False, mode='a', header=not os.path.exists(filename))


def main():
    vacancies_path = 'data/vacancies.csv'

    df = pd.read_csv(vacancies_path)
    df['published_at'] = pd.to_datetime(df['published_at'], utc=True)
    df['year'] = pd.to_datetime(df['published_at']).dt.year
    print(df.head())

    prof = "C++"
    df_for_prof = filter_prof(df, prof)

    unique_years = list(range(2017, 2024))

    for year in unique_years:
        skills_all = get_all_skills(df, year)
        skills_prof = get_all_skills(df_for_prof, year)

        skills_all_top = get_top_skills(skills_all)
        skills_prof_top = get_top_skills(skills_prof)

        export_to_csv(year, skills_all_top, 'data/top_skills_all.csv')
        export_to_csv(year, skills_prof_top, 'data/top_skills_prof.csv')

    print("Data exported to CSV files successfully.")


if __name__ == "__main__":
    main()