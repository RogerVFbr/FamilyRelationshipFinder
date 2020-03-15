"""

Questão prática
^^^^^^^^^^^^^^^
Escrever um agente inteligente que seja capaz de inferir logicamente relações familiares a partir de um banco de dados.
Descrição formal do agente:

Ambiente: Computador, mouse, teclado, prints, tela...
Sensor: familia.csv
Atuador: Relações familiares que não existiam no banco de dados/
Desempenho: Métrica de corretude nos casos de teste propostos:

Casos de teste:
Thais,_,Thomas
Thais,avô,_
Thais,_,Marilda
Fabiola,avô,_
Raphael,_,Tiago
Natalia,avó,_
Miguel,_,Darci
Tiago,_,Umbelino
Malaquias,_,Maria B
Anne,_,Thais

DB RELATIONSHIPS = ['mãe' 'pai' 'esposa' 'filho de' 'esposo' 'mae' 'bisavô']
ENUNCIADO RELATIONSHIPS = ['avô', 'avó',]

"""


"""

Maria B,mãe,Maria J
Maria B,mãe,Maria de Fátima
Maria B,mãe,Marcia
Maria B,mãe,Tania
Maria B,mãe,Sebastião
Maria B,mãe,Cristiano
Maria B,mãe,Marcio
Maria B,mãe,Lea
Maria J,mãe,Thais
Maria J,mãe,Thomas
Maria J,mãe,Tiago
Maria de Fátima,mãe,Fabiola
Maria de Fátima,mãe,Raphael
Marcia,mãe,Michele
Tania,mãe,Marcos
Cristiano,pai,Isac
Lea,mãe,Alex
Lea,mãe,Alan
Lea,mãe,Alexandra
Lea,mãe,Cassandra
Lea,mãe,Alessandra
Alessandra,mãe,Grazielle
Alessandra,mãe,Jonhathan
Maria de Fátima,esposa,Francisco
Maria J,esposa,Juarez
Maria B,esposa,João
Juarez,filho de,Darci
Juarez,filho de,Miguel
Jonas,filho de,Miguel
Marilene,filho de,Miguel
Marlem,filho de,Miguel
João V.,filho de,Miguel
Jonas,pai,Natalia
Jonas,pai,Priscilla
João V.,pai,Carla
João V.,pai,Carina
João V.,esposo,Luciene
Jonas,esposo,Marilda
Darci,esposa,Miguel
Umbelino,pai,Miguel
Maria Conceição,mãe,Miguel
Eugenia,mae,Maria B
Sabino,pai,João
Malaquias,bisavô,Thomas
Anne,esposa,Tiago

"""