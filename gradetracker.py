#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GRADE TRACKER
"""

import modules
import CONFIG
import pandas as pd

import sqlite3

file = 'database.sql'
conn = sqlite3.connect(file)
c = conn.cursor()


# Printing table of data
columns = ['Module', 'Component Name', 'Weight', 'Grade']

components = c.execute('''SELECT code, name, weight, grade
                          FROM Components''').fetchall()

df = pd.DataFrame(data=components, columns=columns)
print(df)

def check_comps(module):
    c.execute('''SELECT sum(weight)
                 FROM Components
                 WHERE
                    code = ?
                    AND
                    grade IS NOT NULL''', (module,))
    return c.fetchone()[0]

# Currently returns list. Index 0 = average%, Index 1 = max% (from components completed).
# [90, 100] = 90/100 = 90%, [20, 50] = 20/50 = 40%
def calc_module_score(module):
    c.execute('''SELECT
                    round(sum(1.0 * (grade * weight) / 100), 2)
                 FROM Components
                 WHERE
                    code = ?
                    AND
                    grade IS NOT null''', (module,))
    return [c.fetchone()[0], check_comps(module)]


def calc_year_score():
    modules = c.execute('''SELECT code
                           FROM modules'''
                       ).fetchall()

    modules_list = {}
    for module in modules:
        numbers = calc_module_score(module[0])
        modules_list[module[0]] = [numbers[0], numbers[1], c.execute('''SELECT credits
                                                                        FROM modules
                                                                        WHERE
                                                                            code = ?''', (module[0],)).fetchone()[0]]
    current = 0
    total_credits = 0
    for key,value in modules_list.items():
        current += value[0] * value[1] * value[2] / 10000
        total_credits += value[2]
    print("You have " + str(current) + "% out of an available " + str(total_credits*100 / 120) + "%")


def calc_year_grade():
    year_score = calc_year_score()



print(calc_year_score())
print(calc_module_score('phy250'))


