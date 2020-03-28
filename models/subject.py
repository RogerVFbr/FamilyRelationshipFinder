import pandas as pd
import numpy as np


class Subject:

    def __init__(self, name, db):
        self.db = db
        self.name = name
        self.checked_names = []
        self.spouse = self.__get_spouse(name)
        self.parents = self.__get_relatives_by_generation(name, 1)
        self.siblings = self.__get_siblings(name)
        self.cousins = self.__get_cousins(name)
        self.children = self.__get_relatives_by_generation(name, -1)
        self.uncle_aunt = self.__get_uncle_aunt(name)
        self.grands = self.__get_relatives_by_generation(name, 2)
        self.great_grands = self.__get_relatives_by_generation(name, 3)
        self.brother_sister_in_law = self.__get_brother_sister_in_law(name)

    def get_relationship(self, subject):

        if subject == self.name:
            return 'o próprio'
        elif self.spouse and subject == self.spouse:
            return 'esposo(a)'
        elif self.parents.size > 0 and subject in self.parents:
            return 'filho(a)'
        elif self.siblings.size > 0 and subject in self.siblings:
            return 'irmão(ã)'
        elif self.cousins.size > 0 and subject in self.cousins:
            return 'primo(a)'
        elif self.children.size > 0 and subject in self.children:
            return 'pai/mãe'
        elif self.uncle_aunt.size > 0 and subject in self.uncle_aunt:
            return 'sobrinho(a)'
        elif self.great_grands.size > 0 and subject in self.great_grands:
            return 'bisneto(a)'
        elif self.brother_sister_in_law.size > 0 and subject in self.brother_sister_in_law:
            return 'cunhado(a)'
        else:
            return None

    def get_relative(self, relationship):

        if self.spouse and relationship == 'esposo(a)':
            return str(self.spouse)
        elif self.parents.size > 0 and relationship in ['pai/mãe']:
            return ', '.join(list(self.parents)) if self.parents.size > 1 else str(self.parents[0])
        elif self.siblings.size > 0 and relationship in ['irmão(â)']:
            return ', '.join(list(self.siblings)) if self.siblings.size > 1 else str(self.siblings[0])
        elif self.cousins.size > 0 and relationship in ['primo(a)']:
            return ', '.join(list(self.cousins)) if self.cousins.size > 1 else str(self.cousins[0])
        elif self.children.size > 0 and relationship in ['filho(a)']:
            return ', '.join(list(self.children)) if self.children.size > 1 else str(self.children[0])
        elif self.uncle_aunt.size > 0 and relationship in ['tio(a)']:
            return ', '.join(list(self.uncle_aunt)) if self.uncle_aunt.size > 1 else str(self.uncle_aunt[0])
        elif self.grands.size > 0 and relationship in ['avô/ó', 'avó', 'avô']:
            return ', '.join(list(self.grands)) if self.grands.size > 1 else str(self.grands[0])
        elif self.great_grands.size > 0 and relationship in ['bisavô/ó']:
            return ', '.join(list(self.great_grands)) if self.great_grands.size > 1 else str(self.great_grands[0])
        elif self.brother_sister_in_law.size > 0 and relationship in ['cunhado(a)']:
            return ', '.join(list(self.brother_sister_in_law)) if self.brother_sister_in_law.size > 1 \
                else str(self.brother_sister_in_law[0])
        else:
            return None

    def __get_brother_sister_in_law(self, name):
        spouse = self.__get_spouse(name)
        if not spouse:
            return np.array([])
        return self.__get_siblings(spouse)

    def __get_relatives_by_generation(self, name, target_gen, relatives=np.array([]), depth=0):
        if target_gen >= 0:
            acquired_relatives = self.__get_parents(name)
            depth += 1
        else:
            acquired_relatives = self.__get_children(name)
            depth -= 1

        if depth == target_gen:
            relatives = np.union1d(relatives, acquired_relatives)
            return relatives

        for x in acquired_relatives:
            new_relatives = self.__get_relatives_by_generation(x, target_gen, relatives, depth)
            relatives = np.union1d(relatives, new_relatives)

        return relatives

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

    def __find_relevant_relationships(self, subject_a, subject_b, data=pd.DataFrame()):

        # Direct connection found, append and return.
        df, subjects = self.db, [subject_a, subject_b]
        direct_relationship = df.loc[df.subject_a.isin(subjects) & df.subject_b.isin(subjects)]
        if direct_relationship.shape[0] > 0:
            data = data.append(direct_relationship, ignore_index=True)
            return data

        # Get related subjects
        related = df.loc[(df.subject_a == subject_a) | (df.subject_b == subject_a)]
        names = pd.unique(related[['subject_a', 'subject_b']].values.ravel('K'))
        names = names[names != subject_a]

        names_iterator = (x for x in names if x not in self.checked_names)
        for x in names_iterator:
            self.checked_names.append(x)
            data = self.__find_relevant_relationships(x, subject_b, data)
            if data.shape[0] > 0:
                subjects = [x, subject_a]
                current_rel = df.loc[df.subject_a.isin(subjects) & df.subject_b.isin(subjects)]
                if current_rel.shape[0] > 0:
                    data = data.append(current_rel, ignore_index=True)
                    return data
        return data

    def get_relationship_chain(self, subject):
        last_subject = relationship_line = self.name
        data = self.__find_relevant_relationships(self.name, subject)[::-1].reset_index(drop=True)
        for i, x in data.iterrows():
            if x.subject_a != last_subject:
                a, b = x.subject_a, x.subject_b
                data.at[i, 'subject_a'] = b
                data.at[i, 'subject_b'] = a
                if x.relationship == 'pai/mãe':
                    data.at[i, 'relationship'] = 'filho(a)'
                elif x.relationship == 'filho(a)':
                    data.at[i, 'relationship'] = 'pai/mãe'

            relationship_line += f" -> {x.relationship} de {x.subject_b}"
            last_subject = x.subject_b

        return relationship_line

    def __repr__(self):
        return f'Subject(\n' \
               f'    name={self.name},\n' \
               f'    spouse={self.spouse},\n' \
               f'    parents={list(self.parents)},\n' \
               f'    siblings={list(self.siblings)},\n' \
               f'    children={list(self.children)},\n' \
               f'    uncle_aunts={list(self.uncle_aunt)},\n' \
               f'    cousins={list(self.cousins)}\n' \
               f'    grands={list(self.grands)}\n' \
               f'    great_grands={list(self.great_grands)}\n' \
               f'    brother_sister_in_law={list(self.brother_sister_in_law)}\n' \
               f')'
