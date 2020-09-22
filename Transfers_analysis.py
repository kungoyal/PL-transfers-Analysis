import pandas as pd
import pandasql as ps
# import blaze
import glob
import os
import matplotlib.pyplot as plt
import numpy as np


def get_team(team_name):
    path = "" #fill in local path to folder containing data files
    all_files = glob.glob(os.path.join(path, "*.csv"))
    df_from_each_file = (pd.read_csv(f) for f in all_files)
    concatenated_df = pd.concat(df_from_each_file, ignore_index=True)
    # data = pd.read_csv("english_premier_league_2010.csv")
    filter1 = concatenated_df['club_name'] == team_name
    filter2 = concatenated_df['transfer_movement'] == 'in'
    concatenated_df.where(filter1 & filter2, inplace=True)
    concatenated_df = concatenated_df.dropna(how='all')
    print(concatenated_df.head())
    return concatenated_df


def get_all():
    path = r'C:\Users\goyal\Documents\PL transfers'
    all_files = glob.glob(os.path.join(path, "*.csv"))
    df_from_each_file = (pd.read_csv(f) for f in all_files)
    concatenated_df = pd.concat(df_from_each_file, ignore_index=True)
    # data = pd.read_csv("english_premier_league_2010.csv")
    filter1 = concatenated_df['transfer_movement'] == 'in'
    concatenated_df.where(filter1, inplace=True)
    concatenated_df = concatenated_df.dropna(how='all')
    print(concatenated_df.head())
    return concatenated_df


def clean_data(df):
    clean_df = df[['position', 'fee_cleaned', 'age']]
    clean_df = clean_df.dropna(how='any')
    clean_df = clean_df[clean_df.fee_cleaned != 0]
    print(clean_df.head())
    return clean_df


def draw_bar(df, team_name, filt):
    if filt == 'pos':
        query = """select position, sum(fee_cleaned) as "total" from df group by position"""
        plot_df = ps.sqldf(query, locals())
        plot_df.sort_values(by='total', ascending=True, inplace=True)
        print(plot_df)
        ax = plot_df.plot.barh(rot=0, x='position', y='total')
        plt.title(f'{team_name} Total spending by position 2010-2020')
        plt.xlabel('Total amount spent in millions')
        # plt.xlim((int(min(plot_df['total'])), int(max(plot_df['total']) + 1)))
        plt.show()
    elif filt == 'age':
        query = """select position, avg(age) as "average" from df group by position"""
        plot_df = ps.sqldf(query, locals())
        plot_df.sort_values(by='average', ascending=True, inplace=True)
        print(plot_df)
        ax = plot_df.plot.barh(rot=0, x='position', y='average', title=f'{team_name} Average age by position 2010-2020')
        # plt.xticks(range(int(min(plot_df['average'])), int(max(plot_df['average']) + 1)))
        plt.xlim((int(min(plot_df['average'])), int(max(plot_df['average']) + 1)))
        plt.show()


def age_percentage(df):
    query = """select age, (count(age)*100.0 / (select count(*) from df)) as "percentage" from df group by age"""
    age_df = ps.sqldf(query, locals())
    age_df.sort_values(by='percentage', ascending=False, inplace=True)
    age_df['percentage'] = age_df['percentage'].round(2)
    print(age_df)


def pos_percentage(df):
    query = """select position, (count(position)*100.0 / (select count(*) from df)) as "percentage" from df group by 
    position """
    pos_df = ps.sqldf(query, locals())
    pos_df.sort_values(by='percentage', ascending=False, inplace=True)
    pos_df['percentage'] = pos_df['percentage'].round(2)
    print(pos_df)


if __name__ == '__main__':
    team = "Arsenal FC"
    data = get_team(team)
    # data = get_all()
    cleaned = clean_data(data)
    # draw_bar(cleaned, 'Premier League', 'pos')
    age_percentage(cleaned)
    pos_percentage(cleaned)
