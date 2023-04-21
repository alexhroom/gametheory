"""Utilities for data analysis."""
import re
import ast
import itertools
import statistics as stats

import pandas as pd

def read_pop_per_turn(filename: str) -> pd.DataFrame:
    """
    Reads a pop_per_turn.csv file.
    Due to containing a list as one entry, the pop_per_turn.csv
    is not a valid CSV file. This function reads the file correctly.
    """
    file_dict = {
        'date': [],
        'type': [],
        'player_name': [],
        'pop_per_turn': []
    }
    with open(filename) as file:
        p = re.compile(r"(.*),(.*),(.*),(\[.*\])")

        for line in file:
            match = p.match(line)
            if match is None:
                continue
            for i, header in enumerate(['date', 'type', 'player_name'], start=1):
                file_dict[header].append(match.group(i))
            file_dict['pop_per_turn'].append(ast.literal_eval(match.group(4)))

    return pd.DataFrame(file_dict)

def mean_pop_per_turn(filename, player_type):
    """Reads a pop_per_turn file and averages the survival time for each player."""
    df = read_pop_per_turn(filename)

    # change each pop_per_turn list into a length,
    # then return average length by player type
    df = df[df['type']==player_type]
    df['pop_per_turn'] = df['pop_per_turn'].transform(len)
    return df.groupby('player_name')['pop_per_turn'].mean()

def make_mean_pop_csvs():
    """Script to make mean population files."""
    tppt = mean_pop_per_turn("pop_per_turn.csv", "trader")
    rppt = mean_pop_per_turn("pop_per_turn.csv", "regulator")

    tppt.to_csv("trader_survival.csv")
    rppt.to_csv("regulator_survival.csv")


def list_pop_per_turn(filename, player_type):
    """Returns a list of average pop per turn for each player."""
    df = read_pop_per_turn(filename)

    df = df[df['type']==player_type]
    return df.groupby('player_name')['pop_per_turn'].apply(element_wise_mean)

def element_wise_mean(list_of_lists):
    return [stats.mean(x) for x in itertools.zip_longest(*list_of_lists, fillvalue=0)]

def make_list_pop_csvs():
    """Script to make survival lines."""
    tppt = list_pop_per_turn("pop_per_turn.csv", "trader")
    rppt = list_pop_per_turn("pop_per_turn.csv", "regulator")

    # turn pop_per_turn into columns rather than a list in one column
    tppt = pd.merge(tppt, pd.DataFrame(tppt.values.tolist()), on=tppt.index).drop('pop_per_turn', axis=1)
    rppt = pd.merge(rppt, pd.DataFrame(rppt.values.tolist()), on=rppt.index).drop('pop_per_turn', axis=1)

    tppt.to_csv("trader_ppt.csv")
    rppt.to_csv("regulator_ppt.csv")


make_mean_pop_csvs()
make_list_pop_csvs()