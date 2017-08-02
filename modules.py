#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 23:52:21 2017
"""


class Module():
    '''Module objects store all components in dictionary of objects. They can be
    accessed using the .component[name].'''

    component = {}

    def __init__(self, name, credit, category):
        self.name = name
        self.credit = credit
        self.category = category

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


def create_module(name, credit, category):
    module_list[name] = Module(name, credit, category)

