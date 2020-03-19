import pandas as pd
import numpy as np


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

        # Initialize procedure.
        self.checked_names = []

        # Extract relevant relationships from db, invert Dataframe order.
        data = self.__find_relevant_relationships(subject_a, subject_b)[::-1].reset_index(drop=True)

        # Get relationship line and branch walk.
        relationship_line, depth_walk = self.__get_relationship_chain(subject_a, data)
        depth = sum(depth_walk)
        # print(f'Branch level: {branch_level}')
        print(f'Branch walk: {depth_walk}')

        # Direct relationship found on db.
        if len(data) == 1:
            return self.__decode_simple_relationship(subject_a, data), relationship_line

        # Same generation relationship.
        if depth == 0:
            parents = self.__get__parents(subject_a)
            siblings = self.__get_siblings(parents)
            return self.__decode_relationship(subject_b, list(siblings), depth), relationship_line

        # Higher generation relationship.
        elif depth > 0:
            direct_relatives = self.__get_higher_direct_relatives(subject_a, depth)
            return self.__decode_relationship(subject_b, list(direct_relatives), depth), relationship_line

        # Lower generation relationship.
        elif depth < 0:
            direct_relatives = self.__get_lower_direct_relatives(subject_a, depth)
            return self.__decode_relationship(subject_b, list(direct_relatives), depth), relationship_line


    @staticmethod
    def __decode_simple_relationship(subject, data):

        if data.subject_a.iloc[0] == subject:
            return data.relationship.iloc[0]
        elif data.relationship.iloc[0] == 'pai/mãe':
            return 'filho(a)'
        elif data.relationship.iloc[0] == 'filho(a)':
            return 'pai/mãe'
        else:
            return None

    @staticmethod
    def __decode_relationship(subject, direct_relatives, branch_level):

        if branch_level == 0 and subject in direct_relatives:
            return 'irmão(ã)'
        elif branch_level == 0 and subject not in direct_relatives:
            return 'primo(a)'
        elif branch_level == 1 and subject in direct_relatives:
            return 'filho(a)'
        elif branch_level == 1 and subject not in direct_relatives:
            return 'sobrinho(a)'
        elif branch_level == 2 and subject in direct_relatives:
            return 'neto(a)'
        elif branch_level == 2 and subject not in direct_relatives:
            return 'sobrinho-neto(a)'
        elif branch_level == 3 and subject in direct_relatives:
            return 'bisneto(a)'
        elif branch_level == 3 and subject not in direct_relatives:
            return 'sobrinho-bisneto(a)'
        else:
            return None

    def __get_higher_direct_relatives(self, subject, target_branch, relatives=np.array([]), branch_level=0):

        parents = self.__get__parents(subject)
        branch_level += 1

        if branch_level == target_branch:
            relatives = np.union1d(relatives, parents)
            return relatives

        for x in parents:
            new_relatives = self.__get_higher_direct_relatives(x, target_branch, relatives, branch_level=branch_level)
            relatives = np.union1d(relatives, new_relatives)

        return relatives

    def __get_lower_direct_relatives(self, subject, target_branch, relatives=np.array([]), branch_level=0):

        children = self.__get_children(subject)
        branch_level -= 1

        if branch_level == target_branch:
            relatives = np.union1d(relatives, children)
            return relatives

        for x in children:
            new_relatives = self.__get_higher_direct_relatives(x, target_branch, relatives, branch_level=branch_level)
            relatives = np.union1d(relatives, new_relatives)

        return relatives

    def __get__parents(self, subject):

        parents = np.array([])
        df = self.df.loc[(self.df.relationship == 'pai/mãe') & (self.df.subject_b == subject)]
        parents = np.union1d(parents, pd.unique(df.subject_a.values.ravel('K')))
        df = self.df.loc[(self.df.relationship == 'filho(a)') & (self.df.subject_a == subject)]
        parents = np.union1d(parents, pd.unique(df.subject_b.values.ravel('K')))
        if len(parents) < 2:
            cond_a = self.df.relationship == 'esposo(a)'
            cond_b = self.df.subject_a.isin(parents)
            cond_c = self.df.subject_b.isin(parents)
            df = self.df.loc[cond_a & (cond_b | cond_c)]
            parents = np.union1d(parents, pd.unique(df[['subject_a', 'subject_b']].values.ravel('K')))

        return parents

    def __get_children(self, subject):

        children = np.array([])
        couple = np.array([subject])

        cond_a = self.df.relationship == 'pai/mãe'
        cond_b = self.df.relationship == 'esposo(a)'
        cond_c = self.df.relationship == 'filho(a)'
        cond_d = self.df.subject_a == subject
        cond_e = self.df.subject_b == subject

        # Get subject's children
        df = self.df.loc[cond_c & cond_e]
        couple = np.union1d(couple, pd.unique(df.subject_a.values.ravel('K')))
        df = self.df.loc[cond_a & cond_d]
        couple = np.union1d(couple, pd.unique(df.subject_b.values.ravel('K')))

        # Attempt to get couple by "spouse" relationship.
        df = self.df.loc[cond_b & cond_d]
        couple = np.union1d(couple, pd.unique(df.subject_b.values.ravel('K')))
        df = self.df.loc[cond_b & cond_e]
        couple = np.union1d(couple, pd.unique(df.subject_a.values.ravel('K')))

        # Attempt to get spouse by children relationships.
        if len(couple) < 2:
            for child in children:
                cond_f = self.df.subject_a == child
                cond_g = self.df.subject_b == child
                df = self.df.loc[cond_a & cond_g]
                couple = np.union1d(couple, pd.unique(df.subject_a.values.ravel('K')))
                if len(couple) == 2:
                    break
                df = self.df.loc[cond_c & cond_f]
                couple = np.union1d(couple, pd.unique(df.subject_b.values.ravel('K')))
                if len(couple) == 2:
                    break

        # Get children of spouse.
        if len(couple) == 2:
            cond_h = self.df.subject_a == couple[1]
            cond_i = self.df.subject_b == couple[1]
            df = self.df.loc[cond_c & cond_i]
            children = np.union1d(children, pd.unique(df.subject_a.values.ravel('K')))
            df = self.df.loc[cond_a & cond_h]
            children = np.union1d(children, pd.unique(df.subject_b.values.ravel('K')))

        return children

    def __get_siblings(self, parents):

        siblings = np.array([])
        for parent in parents:
            df = self.df.loc[(self.df.relationship == 'pai/mãe') & (self.df.subject_a == parent)]
            siblings = np.union1d(siblings, pd.unique(df.subject_b.values.ravel('K')))
            df = self.df.loc[(self.df.relationship == 'filho(a)') & (self.df.subject_b == parent)]
            siblings = np.union1d(siblings, pd.unique(df.subject_a.values.ravel('K')))

        return siblings

    def __find_relevant_relationships(self, subject_a, subject_b, data=pd.DataFrame()):

        # Direct connection found, append and return.
        filter_a = self.df.subject_a.isin([subject_a, subject_b])
        filter_b = self.df.subject_b.isin([subject_a, subject_b])
        direct_relationship = self.df.loc[filter_a & filter_b]
        if direct_relationship.shape[0] > 0:
            data = data.append(direct_relationship, ignore_index=True)
            return data

        # Get related subjects
        related = self.df.loc[(self.df.subject_a == subject_a) | (self.df.subject_b == subject_a)]
        names = pd.unique(related[['subject_a', 'subject_b']].values.ravel('K'))
        names = names[names != subject_a]
        for x in names:
            if x in self.checked_names:
                continue
            self.checked_names.append(x)
            data = self.__find_relevant_relationships(x, subject_b, data)
            if data.shape[0] > 0:
                filter_a = self.df.subject_a.isin([x, subject_a])
                filter_b = self.df.subject_b.isin([x, subject_a])
                current_rel = self.df.loc[filter_a & filter_b]
                if current_rel.shape[0] > 0:
                    data = data.append(current_rel, ignore_index=True)
                    return data

        return data

    @staticmethod
    def __get_relationship_chain(subject, data):

        last_subject = subject
        depth_walk = []
        relationship_line = last_subject
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

            if x.relationship == 'filho(a)':
                depth_walk.append(1)
            elif x.relationship == 'pai/mãe':
                depth_walk.append(-1)
            elif x.relationship == 'bisavô':
                depth_walk.append(-3)
            elif x.relationship == 'esposo(a)':
                depth_walk.append(0)

            last_subject = x.subject_b

        return relationship_line, depth_walk


if __name__ == "__main__":

    f = FamilyFinder("familia.csv")

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
        r, r_l = f.get_relationship(a, b)
        print(f'{a} é {r} de {b}.')
        print(r_l)
        print()

