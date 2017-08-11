#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 23:52:21 2017
"""

import sqlite3

file = 'database.db'
conn = sqlite3.connect(file)
c = conn.cursor()


class Module():

    def __init__(self, module, credits, name):
        self.module = module.lower()
        self.credits = credits
        self.name = name

        c.execute('''SELECT module
                     FROM Modules
                     WHERE
                        module = ?''',
                 (self.module,)
        )

        if c.fetchone():
            print("Module already exists - function here to ask if they want to replace it / look at it / do nothing?")
            return None

        else:
            c.execute('''INSERT INTO Modules values (?,?,?)''',
                         (self.module, self.credits, self.name))
            conn.commit()

    def add_component(self, name, category, weight, grade=200):
        c.execute('''INSERT INTO Components values (?,?,?,?,?)''',
                     (self.module, name, category, weight, grade,))
        conn.commit()

    def get_components(self):
        c.execute('''SELECT *
                     FROM Components
                     WHERE module = ?''',
                     (self.module,))
        for comp in c.fetchall():
            print(comp)

    def get_current_grade(self):
        c.execute('''SELECT
                        round(sum(1.0 * (grade * weight) / 100), 2)
                     FROM Components
                     WHERE
                        module = ?
                        AND
                        grade != 200''', (self.module,))
        return [c.fetchone()[0], self.check_comps()]

    def check_comps(self):
        c.execute('''SELECT sum(weight)
                     FROM Components
                     WHERE
                        module = ?
                        AND
                        grade != 200
                     GROUP BY
                        module''', (self.module,))
        return c.fetchone()[0]

    def change_module(self, module):
        c.execute('''UPDATE Modules
                     SET module = ?
                     WHERE module = ?''',
                     (module, self.module,))
        conn.commit

        self.module = module

    def change_credits(self, credits):
        c.execute('''UPDATE Modules
                     SET credits = ?
                     WHERE name = ?''',
                     (credits, self.name,))
        conn.commit

        self.credit = credits

    def change_name(self, name):
        c.execute('''UPDATE Modules
                     SET name = ?
                     WHERE module = ?''',
                     (name, self.module,))
        conn.commit

        self.name = name

    def what_do_i_need_to_average(self, desired):
        working = self.get_current_grade()
        return round((100 * (desired - working[0]))/(100 - working[1]), 3)

# =============================================================================
#  MODULE CREATION
# =============================================================================


module_list={}

def create_module(module, credit, category):
    module_list[module] = Module(module, credit, category)


#example_name = input("Enter the module name: ")
example_name = 'PHY250'.lower()
#example_credit = input("Enter module credits: ")
example_credit = 25
#example_category = input("Enter module category: ")
example_category = 'Exam'
# desired = input("Desired grade...")
desired = 70





create_module(example_name, example_credit, example_category)

# module_list[example_name].add_component('Essay', 'Coursework', 20, 72)
# module_list[example_name].add_component('Homework 1', 'Homework', 5, 92)
# module_list[example_name].add_component('Homework 2', 'Homework', 5, 90)
# module_list[example_name].add_component('Final Exam', 'Exam',70)

numbers = module_list[example_name].get_current_grade()
print(example_name.upper(), "current grade: " + str(numbers[0]) + "%\n"
        "Out of an available: " + str(numbers[1]) + "%\n"
        "Average mark: " + str(round(numbers[0] / numbers[1] * 100, 2)) + "%")

module_list[example_name].get_components()

print("You need to get " +
      str(module_list[example_name].what_do_i_need_to_average(desired))
      + "%" + " in the remaining components to get " +
      str(desired) + "% overall.")
