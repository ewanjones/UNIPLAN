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

    def __init__(self, module, credit, category):
        self.module = module.lower()
        self.credit = credit
        self.category = category

        c.execute('''SELECT module
                     FROM Modules
                     WHERE
                        module = ?''',
                 (self.module,)
        )

        msg = c.fetchone()

        if msg:
            # module_exists()
            print("Module already exists - function here to ask if they want to replace it / look at it / do nothing?")


        else:
            c.execute('''INSERT INTO Modules values (?,?,?)''', (self.module, self.credit, self.category))
            conn.commit()



        #This is just testing that it worked - returning the data
        c.execute('''SELECT credits, category
                     FROM Modules
                     WHERE module = ?''',(self.module,))
        print(c.fetchall()[0])

    def add_component(self, name, weight, category):
            c.execute('''INSERT INTO Components values (?,?,?,?)''', (self.module, name, weight, category,))
            conn.commit()

            c.execute('''SELECT *
                         FROM Components
                         WHERE module = ?''', (self.module,))
            print(c.fetchall())

    def check_comps(self):
        c.execute('''SELECT sum(weight)
                     FROM Components
                     WHERE
                        module = ?
                     GROUP BY
                        module''', (self.module,))

        total = c.fetchone()[0]
        print(str(total) + "%")
        # weighting = 0
        # for comp in self.component:
        #     weighting += self.component[comp].weight
        # if weighting != 100:
        #     raise ValueError('The component weightings do not add up to 100%.')


# =============================================================================
#  MODULE CREATION
# =============================================================================


module_list={}

def create_module(module, credit, category):
    module_list[module] = Module(module, credit, category)


#example_name = input("Enter the module name: ")
example_name = 'PHY250'
#example_credit = input("Enter module credits: ")
example_credit = 25
#example_category = input("Enter module category: ")
example_category = 'Exam'





create_module(example_name, example_credit, example_category)

# module_list[example_name].add_component('Class Test 1', 80, 'Exam')
module_list[example_name].check_comps()
