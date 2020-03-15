import pandas as pd


class Subject:

    def __init__(self, name, db):
        self.name = name
        self.spouse = self.__get_spouse(db)
        self.father = None
        self.mother = None
        self.__get_parents(db)
        self.brothers = self.__get_brothers(db)


    def __get_spouse(self, db):
        df = db.loc[((db['subject_a'] == self.name) | (db['subject_b'] == self.name))
                    & ((db['relationship'] == 'esposa') | (db['relationship'] == 'esposo'))]

        if df.shape[0] > 0:
            if df['subject_a'].iloc[0] == self.name:
                return df['subject_b'].iloc[0]
            else:
                return df['subject_a'].iloc[0]

        return None

    def __get_father(self, db):
        df = db.loc[(db['subject_b'] == self.name) & (db['relationship'] == 'pai')]
        if df.shape[0] > 0:
            return df['subject_a'].iloc[0]

        return None

    def __get_mother(self, db):
        df = db.loc[(db['subject_b'] == self.name) & (db['relationship'] == 'mãe')]
        if df.shape[0] > 0:
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
                self.father = df['subject_b'].iloc[0]


    def __get_brothers(self, db):
        df = db.loc[
            ((db['subject_a'] == self.mother) & (db['relationship'] == 'mãe') & (db['subject_b'] != self.name))
            | ((db['subject_a'] == self.father) & (db['relationship'] == 'pai') & (db['subject_b'] != self.name))
            | (((db['subject_b'] == self.mother) | (db['subject_b'] == self.father)) & (db['relationship'] == 'filho de') & (db['subject_a'] != self.name))
        ]
        if df.shape[0] > 0:
            return pd.unique(df[['subject_a', 'subject_b']].values.ravel('K'))

        return None

    def __add_relationship(self):
        pass

    def __repr__(self):
        return f'Subject(name={self.name}, spouse={self.spouse}, father={self.father}, mother={self.mother})'
        # return f'Subject(name={self.name}, spouse={self.spouse}, father={self.father}, mother={self.mother}, ' \
        #        f'brothers={self.brothers})'

