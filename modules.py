#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 23:52:21 2017
"""

# Imports sqlite and sets up the connection
import sqlite3

file = 'database.db'
conn = sqlite3.connect(file)
c = conn.cursor()


class Module():
    '''Module objects store all components in dictionary of objects. They can be
    accessed using the .component[name].'''

    component = {}

    def __init__(self, name, credit, category):
        self.name = name.lower()
        self.credit = credit
        self.category = category

        c.execute('''SELECT name
                     FROM Modules
                     WHERE
                        name = ?
                     GROUP BY
                        Name''',
                 (self.name,)
        )

        msg = c.fetchone()

        if msg:
            # module_exists()
            print("Module already exists - function here to ask if they want to replace it / look at it / do nothing?")


        else:
            c.execute('''INSERT INTO Modules values (?,?,?)''', (self.name, self.credit, self.category))
            conn.commit()



        #This is just testing that it worked - returning the data
        c.execute('''SELECT credits, category
                     FROM Modules
                     WHERE name = ?''',(self.name,))
        print(c.fetchall()[0])

    def add_component(self, name, weight, category):
            self.component[name] = self.Component(name, weight, category)

    def valid_comps(self):
        weighting = 0
        for comp in self.component:
            weighting += self.component[comp].weight
        if weighting != 100:
            raise ValueError('The component weightings do not add up to 100%.')


    # Component class holds info about each aspect of  module
    class Component():
        def __init__(self, name, weight, category):
            self.name = name
            self.weight = weight
            self.category = category

        def add_grade(self, grade_type, grade):
            self.grade_type = grade_type
            self.grade = grade


# =============================================================================
#  MODULE CREATION
# =============================================================================


module_list={}

def create_module(name, credit, category):
    module_list[name] = Module(name, credit, category)


# Just tesing it with values - on my editor I can't actually input values
#example_name = input("Enter the module name: ")
#example_credit = input("Enter module credits: ")
#example_category = input("Enter module category: ")

example_name = 'PHY250'
example_credit = 25
example_category = 'Exam'

create_module(example_name, example_credit, example_category)
