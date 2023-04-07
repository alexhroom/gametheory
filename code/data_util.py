"""Utilities for data analysis."""
import re
import ast

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

tppt = mean_pop_per_turn("pop_per_turn.csv", "trader")
rppt = mean_pop_per_turn("pop_per_turn.csv", "regulator")

tppt.to_csv("trader_pop_per_turn.csv")
rppt.to_csv("regulator_pop_per_turn.csv")