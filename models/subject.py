import pandas as pd
import numpy as np


class Subject:

    def __init__(self, name, db):
        self.db = db
        self.name = name
        self.spouse = self.__get_spouse(name)
        self.parents = self.__get_parents(name)
        self.siblings = self.__get_siblings(name)
        self.children = self.__get_children(name)
        self.uncle_aunt = self.__get_uncle_aunt(name)
        self.cousins = self.__get_cousins(name)

    def __get_spouse(self, name):
        df = self.db
        df = df.loc[((df.subject_a == name) | (df.subject_b == name)) & (df.relationship == 'esposo(a)')]
        if df.shape[0] > 0:
            if df['subject_a'].iloc[0] == name:
                return df['subject_b'].iloc[0]
            else:
                return df['subject_a'].iloc[0]

        return np.array([])

    def __get_parents(self, name):
        parents, df = np.array([]), self.db
        df_a = df.loc[(df.relationship == 'pai/mãe') & (df.subject_b == name)]
        parents = np.union1d(parents, pd.unique(df_a.subject_a.values.ravel('K')))
        df_b = df.loc[(df.relationship == 'filho(a)') & (df.subject_a == name)]
        parents = np.union1d(parents, pd.unique(df_b.subject_b.values.ravel('K')))
        if len(parents) < 2:
            df_c = df.loc[(df.relationship == 'esposo(a)') & (df.subject_a.isin(parents) | df.subject_b.isin(parents))]
            parents = np.union1d(parents, pd.unique(df_c[['subject_a', 'subject_b']].values.ravel('K')))

        return parents

    def __get_siblings(self, name):
        df, parents = self.db, self.__get_parents(name)
        unique_a, unique_b = np.array([]), np.array([])
        for parent in parents:
            df_a = df.loc[(df.relationship == 'pai/mãe') & (df.subject_a == parent)]
            df_b = df.loc[(df.relationship == 'filho(a)') & (df.subject_b == parent)]
            unique_a = pd.unique(df_a.subject_b.values.ravel('K'))
            unique_b = pd.unique(df_b.subject_a.values.ravel('K'))
        siblings = np.union1d(unique_a, unique_b)
        return np.setdiff1d(siblings, np.array([name]))

    def __get_children(self, name):
        df = self.db
        name_and_spouse = [name] + list(self.__get_spouse(name))
        df_a = df.loc[df.subject_a.isin(name_and_spouse) & (df.relationship == 'pai/mãe')]
        df_b = df.loc[df.subject_b.isin(name_and_spouse) & (df.relationship == 'filho(a)')]
        unique_a = pd.unique(df_a['subject_b'].values.ravel('K'))
        unique_b = pd.unique(df_b['subject_a'].values.ravel('K'))
        return np.union1d(unique_a, unique_b)

    def __get_uncle_aunt(self, name):
        parents = self.__get_parents(name)
        uncle_aunts, uncle_aunts_spouses = np.array([]), np.array([])
        for parent in parents:
            uncle_aunts = np.union1d(uncle_aunts, self.__get_siblings(parent))
        if uncle_aunts.size == 0:
            return uncle_aunts
        uncle_aunts = np.setdiff1d(uncle_aunts, parents)
        if uncle_aunts.size == 0:
            return uncle_aunts
        for uncle_aunt in uncle_aunts:
            uncle_aunts_spouses = np.union1d(uncle_aunts_spouses, self.__get_spouse(uncle_aunt))
        return np.union1d(uncle_aunts, uncle_aunts_spouses)

    def __get_cousins(self, name):
        parents = self.__get_parents(name)
        uncle_aunts, cousins = np.array([]), np.array([])
        for parent in parents:
            uncle_aunts = np.union1d(self.__get_siblings(parent), uncle_aunts)
        if uncle_aunts.size == 0:
            return uncle_aunts
        uncle_aunts = np.setdiff1d(uncle_aunts, parents)
        if uncle_aunts.size == 0:
            return uncle_aunts
        for uncle_aunt in uncle_aunts:
            cousins = np.union1d(cousins, self.__get_children(uncle_aunt))

        return cousins

    def __repr__(self):
        return f'Subject(name={self.name}, spouse={self.spouse}, parents={self.parents}, ' \
               f'siblings={self.siblings}, children={self.children}, uncle_aunts={self.uncle_aunt}, ' \
               f'cousins={self.cousins})'


