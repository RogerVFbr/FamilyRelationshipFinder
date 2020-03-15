import pandas as pd
import pprint
from models.subject import Subject


class FamilyRelationshipFinder:

    def __init__(self, csv_file):

        self.df = pd.read_csv(csv_file)
        self.df.columns = ['subject_a', 'relationship', 'subject_b']
        self.names = pd.unique(self.df[['subject_a', 'subject_b']].values.ravel('K'))
        self.subjects = [Subject(x, self.df) for x in self.names]

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.subjects)

    def get_relationship(self, subject_a, subject_b, previous = []) -> (str, str, str):

        filter = [subject_a, subject_b]
        relationships = self.df.loc[(self.df['subject_a'].isin(filter)) | (self.df['subject_b'].isin(filter))]
        print(relationships)

        relationship = self.df.loc[(self.df['subject_a'] == subject_a) & (self.df['subject_b'] == subject_b)]
        if relationship.shape[0] == 1:
            return subject_a, relationship['relationship'].iloc[0], subject_b

        relationship = self.df.loc[(self.df['subject_a'] == subject_b) & (self.df['subject_b'] == subject_a)]
        if relationship.shape[0] == 1:
            return subject_b, relationship['relationship'].iloc[0], subject_a

        return None, None, None


if __name__ == "__main__":

    frf = FamilyRelationshipFinder("familia.csv")

    # people = ('Thais', 'Thomas')
    # subject_a, relationship, subject_b = frf.get_relationship(people[0], people[1])
    # print(f'{people} -> {subject_a} é {relationship} de {subject_b}.')
    # print()
    #
    # people = ('Thais', 'Marilda')
    # subject_a, relationship, subject_b = frf.get_relationship(people[0], people[1])
    # print(f'{people} -> {subject_a} é {relationship} de {subject_b}.')
    # print()
    #
    # people = ('Raphael', 'Tiago')
    # subject_a, relationship, subject_b = frf.get_relationship(people[0], people[1])
    # print(f'{people} -> {subject_a} é {relationship} de {subject_b}.')
    # print()
    #
    # people = ('Miguel', 'Darci')
    # subject_a, relationship, subject_b = frf.get_relationship(people[0], people[1])
    # print(f'{people} -> {subject_a} é {relationship} de {subject_b}.')
    # print()
    #
    # people = ('Tiago', 'Umbelino')
    # subject_a, relationship, subject_b = frf.get_relationship(people[0], people[1])
    # print(f'{people} -> {subject_a} é {relationship} de {subject_b}.')
    # print()
    #
    # people = ('Malaquias', 'Maria B')
    # subject_a, relationship, subject_b = frf.get_relationship(people[0], people[1])
    # print(f'{people} -> {subject_a} é {relationship} de {subject_b}.')
    # print()
    #
    # people = ('Anne', 'Thais')
    # subject_a, relationship, subject_b = frf.get_relationship(people[0], people[1])
    # print(f'{people} -> {subject_a} é {relationship} de {subject_b}.')
    # print()

