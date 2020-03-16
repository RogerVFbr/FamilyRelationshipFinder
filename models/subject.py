import pandas as pd
import numpy as np


class Subject:

    def __init__(self, name, db):
        self.name = name
        self.spouse = self.__get_spouse(db)
        self.father = None
        self.mother = None
        self.__get_parents(db)
        self.brothers = self.__get_brothers(db)
        self.children = self.__get_children(db)
        self.grand_fathers = self.__get_grand_fathers(db)
        self.grand_mothers = self.__get_grand_mothers(db)
        self.cousins = self.__get_cousins(db)

    def __get_spouse(self, db):

        filter_a = db['subject_a'] == self.name
        filter_b = db['subject_b'] == self.name
        filter_c = db['relationship'] == 'esposa'
        filter_d = db['relationship'] == 'esposo'

        df = db.loc[(filter_a | filter_b) & (filter_c | filter_d)]
        if df.shape[0] > 0:
            if df['subject_a'].iloc[0] == self.name:
                return df['subject_b'].iloc[0]
            else:
                return df['subject_a'].iloc[0]

        return None

    def __get_parents(self, db):

        df = db.loc[(db['subject_b'] == self.name) & (db['relationship'] == 'pai')]
        if df.shape[0] > 0:
            self.father = df['subject_a'].iloc[0]

        df = db.loc[(db['subject_b'] == self.name) & (db['relationship'] == 'mãe')]
        if df.shape[0] > 0:
            self.mother = df['subject_a'].iloc[0]

        if not self.father:
            df = db.loc[(db['subject_a'] == self.mother) & (db['relationship'] == 'esposa')]
            if df.shape[0] > 0:
                self.father = df['subject_b'].iloc[0]

        if not self.mother:
            df = db.loc[(db['subject_a'] == self.father) & (db['relationship'] == 'esposo')]
            if df.shape[0] > 0:
                self.mother = df['subject_b'].iloc[0]

    def __get_brothers(self, db):

        filter_a = db['subject_a'] == self.mother
        filter_b = db['relationship'] == 'mãe'
        filter_c = db['subject_b'] != self.name

        filter_d = db['subject_a'] == self.father
        filter_e = db['relationship'] == 'pai'

        filter_f = db['subject_b'] == self.mother
        filter_g = db['subject_b'] == self.father
        filter_h = db['relationship'] == 'filho de'
        filter_i = db['subject_a'] != self.name

        df_a = db.loc[(filter_a & filter_b & filter_c) | (filter_d & filter_e & filter_c)]
        df_b = db.loc[(filter_f | filter_g) & filter_h & filter_i]

        unique_a = pd.unique(df_a[['subject_b']].values.ravel('K'))
        unique_b = pd.unique(df_b[['subject_a']].values.ravel('K'))

        return np.union1d(unique_a, unique_b)

    def __get_children(self, db):

        filter_a = db['subject_a'] == self.name
        filter_b = db['relationship'] == 'pai'
        filter_c = db['relationship'] == 'mãe'

        filter_d = db['subject_b'] == self.name
        filter_e = db['relationship'] == 'filho de'

        df_a = db.loc[filter_a & (filter_b | filter_c)]
        df_b = db.loc[filter_d & filter_e]

        unique_a = pd.unique(df_a[['subject_b']].values.ravel('K'))
        unique_b = pd.unique(df_b[['subject_a']].values.ravel('K'))

        return np.union1d(unique_a, unique_b)

    def __get_grand_fathers(self, db):
        return []

    def __get_grand_mothers(self, db):
        return []

    def __get_cousins(self, db):
        return []

    def __repr__(self):
        # return f'Subject(name={self.name}, spouse={self.spouse}, father={self.father}, mother={self.mother})'
        return f'Subject(name={self.name}, spouse={self.spouse}, father={self.father}, mother={self.mother}, ' \
               f'brothers={self.brothers}, children={self.children})'

