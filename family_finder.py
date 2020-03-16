import pandas as pd
import numpy as np
import pprint
from models.subject import Subject


class FamilyFinder:

    def __init__(self, csv_file):

        self.df = pd.read_csv(csv_file)
        self.df.loc[-1] = self.df.columns
        self.df.index = self.df.index + 1
        self.df = self.df.sort_index()
        self.df.columns = ['subject_a', 'relationship', 'subject_b']
        self.checked_names = []

        self.df.replace('mãe', 'pai/mãe', inplace=True)
        self.df.replace('pai', 'pai/mãe', inplace=True)
        self.df.replace('esposa', 'esposo(a)', inplace=True)
        self.df.replace('esposo', 'esposo(a)', inplace=True)
        self.df.replace('filho de', 'filho(a)', inplace=True)

    def get_relationship(self, subject_a, subject_b):
        self.checked_names = []
        data = self.__find_relevant_relationships(subject_a, subject_b)[2][::-1].reset_index(drop=True)
        relationship_line, branch_walk = self.__get_relationship_chain(subject_a, data)

        print(relationship_line)
        print(f'Branch walk: {branch_walk}')
        print(f'Branch total: {sum(branch_walk)}')

        # relatives = self.__get_direct_relatives(subject_a, sum(branch_walk))
        relatives = self.__get_direct_relatives(subject_a, 2)
        print(relatives)

        return data

    def __get_direct_relatives(self, subject, target_branch, relatives=np.array([]), branch_level=0):

        parents = np.array([])
        branch_level += 1

        df = self.df.loc[(self.df['relationship'] == 'pai/mãe') & (self.df['subject_b'] == subject)]
        if df.shape[0] > 0:
            parents = np.union1d(parents, pd.unique(df['subject_a'].values.ravel('K')))

        if len(parents) < 2:
            cond_a = self.df['relationship'] == 'esposo(a)'
            cond_b = self.df['subject_a'].isin(parents)
            cond_c = self.df['subject_b'].isin(parents)
            df = self.df.loc[cond_a & (cond_b | cond_c)]
            if df.shape[0] > 0:
                parents = np.union1d(parents, pd.unique(df[['subject_a', 'subject_b']].values.ravel('K')))

        if branch_level == target_branch:
            relatives = parents
            return relatives

        for x in parents:
            parents = self.__get_direct_relatives(x, target_branch, branch_level=branch_level)
            relatives = np.union1d(relatives, parents)

        return relatives

    def __find_relevant_relationships(self, subject_a, subject_b, data=pd.DataFrame()):

        # Direct connection found, append and return.
        filter_a = self.df['subject_a'].isin([subject_a, subject_b])
        filter_b = self.df['subject_b'].isin([subject_a, subject_b])
        direct_relationship = self.df.loc[filter_a & filter_b]
        if direct_relationship.shape[0] > 0:
            data = data.append(direct_relationship, ignore_index=True)
            return subject_a, subject_b, data

        # Get related subjects
        related = self.df.loc[(self.df['subject_a'] == subject_a) | (self.df['subject_b'] == subject_a)]
        names = pd.unique(related[['subject_a', 'subject_b']].values.ravel('K'))
        names = names[names != subject_a]
        for x in names:
            if x in self.checked_names:
                continue
            self.checked_names.append(x)
            data = self.__find_relevant_relationships(x, subject_b, data)[2]
            if data.shape[0] > 0:
                filter_a = self.df['subject_a'].isin([x, subject_a])
                filter_b = self.df['subject_b'].isin([x, subject_a])
                current_rel = self.df.loc[filter_a & filter_b]
                if current_rel.shape[0] > 0:
                    data = data.append(current_rel, ignore_index=True)
                    return subject_a, subject_b, data

        return subject_a, subject_b, data

    def __get_relationship_chain(self, subject, data):

        last_subject = subject
        branch_walk = []
        relationship_line = last_subject
        for i, x in data.iterrows():
            if x['subject_a'] != last_subject:
                a, b = x['subject_a'], x['subject_b']
                data.at[i, 'subject_a'] = b
                data.at[i, 'subject_b'] = a
                if x['relationship'] == 'pai/mãe':
                    data.at[i, 'relationship'] = 'filho(a)'
                elif x['relationship'] == 'filho(a)':
                    data.at[i, 'relationship'] = 'pai/mãe'

            relationship_line += f" -> {x['relationship']} de {x['subject_b']}"

            if x['relationship'] == 'filho(a)':
                branch_walk.append(1)
            elif x['relationship'] == 'pai/mãe':
                branch_walk.append(-1)
            elif x['relationship'] == 'bisavô':
                branch_walk.append(-3)
            elif x['relationship'] == 'esposo(a)':
                branch_walk.append(0)

            last_subject = x['subject_b']

        return relationship_line, branch_walk


if __name__ == "__main__":

    frf = FamilyFinder("familia.csv")

    use_cases = [
        ('Thais', 'Thomas'),
        ('Thais', 'Marilda'),
        ('Raphael', 'Tiago'),
        ('Miguel', 'Darci'),
        ('Tiago', 'Umbelino'),
        ('Malaquias', 'Maria B'),
        ('Anne', 'Thais')
    ]

    for a, b in use_cases:
        print(f'{a}, {b}')
        relationship = frf.get_relationship(a, b)
        print()

