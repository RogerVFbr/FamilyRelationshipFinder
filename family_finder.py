import pandas as pd
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
        subj = Subject(subject_a, self.df)
        relationship = subj.get_relationship(subject_b)
        chain = subj.get_relationship_chain(subject_b)
        return relationship, chain

    def get_relative(self, subject_a, relationship):
        subj = Subject(subject_a, self.df)
        return subj.get_relative(relationship)


if __name__ == "__main__":

    f = FamilyFinder("familia.csv")

    get_relationship_use_cases = [
        # ('Thais', 'Thomas'), ('Thais', 'Marilda'), ('Raphael', 'Tiago'), ('Miguel', 'Darci'),
        ('Fabiola', 'João'),
        # ('Tiago', 'Umbelino'), ('Malaquias', 'Maria B'), ('Anne', 'Thais')
    ]

    for a, b in get_relationship_use_cases:
        relationship, chain = f.get_relationship(a, b)
        print(f'{a} é {relationship} de {b}. ({chain})')

    get_relative_use_cases = [('Thais', 'avô'), ('Fabiola', 'avô'), ('Natalia', 'avó')]

    # for a, b in get_relative_use_cases:
    #     relative = f.get_relative(a, b)
    #     print(f'{relative} é(são) {b}(s) de {a}.')
