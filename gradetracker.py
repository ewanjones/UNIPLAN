#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GRADE TRACKER
"""

import modules
import pandas as pd

TOTAL_CREDITS = 120
THRESHOLDS = {'1st': 70,
              '2:1': 60,
              '2:2': 50,
              '3rd': 40,
              'Pass': 30,
              'Fail': 0}

BMS381 = Module('BMS381', 20, 'Practical')
BMS381.add_component('essay', 50, 'essay')
BMS381.add_component('exam', 50, 'exam')
BMS381.component['essay'].grade = 67
BMS381.component['exam'].grade = 76
BMS381.valid_comps()

module_list = {'BMS381': BMS381}

columns = ['Module', 'Component', 'Weight', 'Grade']
df = pd.DataFrame(columns=columns)

for module in module_list:
    components = module_list[module].component
    for comp in components:
        grade = components[comp].grade
        weight = components[comp].weight

        data = [module, comp, weight, grade]
        df.loc[len(df)] = data

print(df)


def calc_module_score(module):
    comps = module.component
    module_score = 0

    for item in comps:
        weight = comps[item].weight
        grade = comps[item].grade
        module_score += grade / 100 * weight

    return module_score


def calc_year_score():
    year_score = 0 
    
    for module in module_list:
        mod_score = calc_module_score(module_list[module])
        year_score += mod_score / TOTAL_CREDITS * module_list[module].credit
    
    year_score = round(year_score, 2) 
    return year_score


def calc_year_grade():
    year_score = calc_year_score()
    
    if
        
print(calc_year_score())