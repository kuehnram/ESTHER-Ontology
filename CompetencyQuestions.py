__author__ = "Ramona Kühn"
__license__ = "MIT"
__version__ = "1.0."
__email__ = "ramona.kuehn@uni-passau.de"

"""
This file contains the competency questions (Grüninger and Fox 1995) to evaluate the Esther ontology of rhetorical
figures in English.
Q1 and Q2 are the same as used by the RetFig and GRhOOT ontology for comparison.

Q1: Which rhetorical figures have their defining element in a word?
Q2: In which rhetorical figures is a letter omitted?
Q3: What are figures that are neither figures of construction, nor figures of speech, nor figures of thought?
Q4: Which figures belong to the rhetorical group of tropes (should be the same output as Q3)?
Q5: What is an example sentence for the figure alliteration?
Q6: What is the definition of the figure parallelism?
Q7: Which figures of speech or figures of thought have their defining element in the beginning?
Q8: Which figures have  repeat an element in the same form?
Q9: In which figures is a word in the same form repeated?
Q10: Which figures are the opposite of other figures?
"""

import rdflib

g = rdflib.Graph()
g.parse('C:/Users/kuehn21/Documents/Paper/2023 - FOIS_ESTHER EnglishOntology/esther - Kopie.owl',
        format='application/rdf+xml')
esther = rdflib.Namespace('https://kuehnram.de/')
g.bind('esther', esther)

# Q1: Which rhetorical figures have their defining element in a word?
cq1 = """
SELECT ?figure
WHERE {
  ?figure rdf:type esther:RhetoricalFigure ;
          esther:isInArea esther:Word .
}

"""

# Q2: In which rhetorical figures is a letter omitted?
cq2 = """
SELECT  ?figure
WHERE {
    ?figure rdf:type esther:RhetoricalFigure ;
            esther:isOmitted esther:Letter .
}
"""

# Q3: What are figures that are neither figures of construction, nor figures of speech, nor figures of thought?
cq3 = """
SELECT ?figure
WHERE {
  ?figure rdf:type esther:RhetoricalFigure.
  FILTER NOT EXISTS {
    ?figure esther:isRhetoricalGroup esther:FigureOfConstruction.
  }
  FILTER NOT EXISTS {
    ?figure esther:isRhetoricalGroup esther:FigureOfThought.
  }
  FILTER NOT EXISTS {
    ?figure esther:isRhetoricalGroup esther:FigureOfSpeech.
  }
}
"""

# Q4: Which figures belong to the rhetorical group of tropes (should be the same output as Q3)?
cq4 = """
SELECT distinct ?figure
WHERE {
    ?figure rdf:type esther:RhetoricalFigure ;
        esther:isRhetoricalGroup esther:Trope
    }
"""

# Q5: What is an example sentence for the figure alliteration?
cq5 = """
SELECT ?example
WHERE {
  esther:Alliteration esther:isExample ?example .
}
"""

# Q6: What is the definition of the figure parallelism?
cq6= """
SELECT distinct ?definition
WHERE {
    esther:Parallelism rdfs:comment ?definition .
 }
"""



# Q7: Which figures of speech or figures of thought have their defining element in the beginning?
cq7 = """
SELECT distinct ?figure
WHERE {
    ?figure esther:isRhetoricalGroup ?group .
    ?figure esther:isInPosition esther:Beginning .
    ?group rdfs:label ?groupName .
    Filter (?groupName = "FigureOfSpeech" || ?groupName = "FigureOfThought") }
"""




# Q8: Which figures repeat an element in the same form?
cq8 = """
SELECT distinct ?figure
WHERE {
    ?figure esther:isRepeatableElementOfSameForm ?_ .
}
"""

# Q9: In which figures is a word in the same form repeated?
cq9 = """
SELECT distinct ?figure
WHERE {
    ?figure esther:isRepeatableElementOfSameForm esther:WordElement .
}
"""

# Q10: Which figures are the opposite of other figures?
cq10 = """
SELECT distinct ?figureA ?figureB
WHERE {
    ?figureA esther:isOppositeFigure ?figureB .
}
"""

print("Competency Question Q1: Which rhetorical figures have their defining element in a word?")
result = g.query(cq1)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)


print("\nCompetency Question Q2: In which rhetorical figures is a letter omitted?")
result = g.query(cq2)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print(
    "\nCompetency Question Q3: What are figures that are neither figures of construction, nor figures of speech, nor figures of thought?"
    "nor figures of thought.")
result = g.query(cq3)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print(
    "\nCompetency Question Q4: Which figures belong to the rhetorical group of tropes (should be the same output as Q3)?")
result = g.query(cq4)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print("\nCompetency Question Q5: What is an example sentence for the figure alliteration?")
result = g.query(cq5)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print("\nCompetency Question Q6: What is the definition of the figure parallelism?")
result = g.query(cq6)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print(
    "\nCompetency Question Q7: Which figures of speech or figures of thought have their defining element in the beginning?")
result = g.query(cq7)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print("\nCompetency Question Q8: Which figures repeat an element in the same form?")
result = g.query(cq8)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print("\nCompetency Question Q9: Which figures repeat a word in the same form?")
result = g.query(cq9)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print("\nCompetency Question Q10: Which figures are the opposite of other figures?")
result = g.query(cq10)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)
