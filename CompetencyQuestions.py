__author__ = "Anonymous"
__license__ = "CreativeCommons"
__version__ = "1.0."
__email__ = "a@b.c"

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
g.parse('esther.owl', format='application/rdf+xml')
esther = rdflib.Namespace('https://anonymous.org/')
g.bind('esther', esther)

# Q1: Which rhetorical figures have their defining element in a word?
cq1 = """
SELECT distinct ?Figure
WHERE {
    ?Figure esther:IsInArea ?Area .
    ?Area rdfs:label ?AreaName .
    Filter (?AreaName = "Word" ) }
"""

# Q2: In which rhetorical figures is a letter omitted?
cq2 = """
SELECT distinct ?Figure
WHERE {
    ?Figure esther:IsOmitted ?Element .
    ?Element rdfs:label ?ElementName .
    Filter (?ElementName = "Letter" ) }
"""

# Q3: What are figures that are neither figures of construction, nor figures of speech, nor figures of thought?
cq3 = """
SELECT distinct ?Figure
WHERE {
    ?Figure esther:IsRhetoricalGroup ?Group .
    ?Group rdfs:label ?GroupName .
    Filter (?GroupName != "FigureOfConstruction" && ?GroupName != "FigureOfThought" && ?GroupName != "FigureOfSpeech") }
"""

# Q4: Which figures belong to the rhetorical group of tropes (should be the same output as Q3)?
cq4 = """
SELECT distinct ?Figure
WHERE {
    ?Figure esther:IsRhetoricalGroup ?Group .
    ?Group rdfs:label ?GroupName .
    Filter (?GroupName = "Trope") }
"""

# Q5: What is an example sentence for the figure alliteration?
cq5 = """
SELECT distinct ?Figure ?Example ?Value
WHERE {
    ?Figure rdfs:label ?FigureName .
    ?Figure esther:IsExample ?Value
    Filter (?FigureName = "Alliteration") }
"""

# Q6: What is the definition of the figure parallelism?
cq6 = """
SELECT distinct ?Figure ?Definition ?Value
WHERE {
    ?Figure rdfs:label ?FigureName .
    ?Figure rdfs:comment ?Value
    Filter (?FigureName = "Parallelism") }
"""

# Q7: Which figures of speech or figures of thought have their defining element in the beginning?
cq7 = """
SELECT distinct ?Figure
WHERE {
    ?Figure esther:IsRhetoricalGroup ?Group .
    ?Group rdfs:label ?GroupName .
    ?Figure esther:IsInPosition ?Position .
    ?Position rdfs:label ?PositionLocation .
    Filter ((?GroupName = "FigureOfSpeech" || ?GroupName = "FigureOfThought") && ?PositionLocation = "Beginning") }
"""

# Q8: Which figures have  repeat an element in the same form?
cq8 = """
SELECT distinct ?Figure
WHERE {
    ?Figure esther:IsRepeatableElementOfSameForm ?_ .
}
"""

# Q9: In which figures is a word in the same form repeated?
cq9 = """
SELECT distinct ?Figure
WHERE {
    ?Figure esther:IsRepeatableElementOfSameForm ?Element .
    ?Element rdfs:label "WordElement" .
}
"""

# Q10: Which figures are the opposite of other figures?
cq10 = """
SELECT distinct ?FigureA ?FigureB
WHERE {
    ?FigureA esther:IsOppositeFigure ?FigureB .
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

print("\nCompetency Question Q3: What are figures that are neither figures of construction, nor figures of speech, nor figures of thought?"
      "nor figures of thought.")
result = g.query(cq3)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print("\nCompetency Question Q4: Which figures belong to the rhetorical group of tropes (should be the same output as Q3)?")
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

print("\nCompetency Question Q7: Which figures of speech or figures of thought have their defining element in the beginning?")
result = g.query(cq7)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print("\nCompetency Question Q8: Which figures have  repeat an element in the same form?")
result = g.query(cq8)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print("\nCompetency Question Q9: In which figures is a word in the same form repeated?")
result = g.query(cq9)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print("\nCompetency Question Q10: Which figures are the opposite of other figures?")
result = g.query(cq10)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

