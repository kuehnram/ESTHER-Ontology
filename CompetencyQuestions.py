__author__ = "Anonymous"
__license__ = "CreativeCommons"
__version__ = "1.0."
__email__ = "a@b.c"

"""
This file contains the competency questions (Grüninger and Fox 1995) to evaluate the Esther ontology of rhetorical
figures in English.
Q1 and Q2 are the same as used by the RetFig and GRhOOT ontology for comparison.

Q1: Rhetorical figures that have their defining element in a word.
Q2: Rhetorical figures where a letter is omitted.
Q3: Figures that are neither figures of construction, nor figures of speech, nor figures of thought.
Q4: All figures that are tropes (should be same output as Q3).
Q5: Example sentences for the figure Alliteration.
Q6: Definition of the figure Parallelism.
Q7: Figures of speech or figures of thought with position beginning.
Q8: Figures with a repeated element of the same form.
Q9: Figures where a word in the same form is repeated.
Q10: Figures and their opposite figures.
"""

import rdflib

g = rdflib.Graph()
g.parse('esther.owl', format='application/rdf+xml')
esther = rdflib.Namespace('https://anonymous.org/')
g.bind('esther', esther)

# Q1: Rhetorical figures that have their defining element in a word.
cq1 = """
SELECT distinct ?Figure
WHERE {
    ?Figure esther:IsInArea ?Area .
    ?Area rdfs:label ?AreaName .
    Filter (?AreaName = "Word" ) }
"""

# Q2: Rhetorical figures where a letter is omitted.
cq2 = """
SELECT distinct ?Figure
WHERE {
    ?Figure esther:IsOmitted ?Element .
    ?Element rdfs:label ?ElementName .
    Filter (?ElementName = "Letter" ) }
"""

# Q3: Figures that are neither figures of construction, nor figures of speech, nor figures of thought
cq3 = """
SELECT distinct ?Figure
WHERE {
    ?Figure esther:IsRhetoricalGroup ?Group .
    ?Group rdfs:label ?GroupName .
    Filter (?GroupName != "FigureOfConstruction" && ?GroupName != "FigureOfThought" && ?GroupName != "FigureOfSpeech") }
"""

# Q4: All figure that are tropes (should be same output as Q3).
cq4 = """
SELECT distinct ?Figure
WHERE {
    ?Figure esther:IsRhetoricalGroup ?Group .
    ?Group rdfs:label ?GroupName .
    Filter (?GroupName = "Trope") }
"""

# Q5: Example sentences for the figure Alliteration.
cq5 = """
SELECT distinct ?Figure ?Example ?Value
WHERE {
    ?Figure rdfs:label ?FigureName .
    ?Figure esther:IsExample ?Value
    Filter (?FigureName = "Alliteration") }
"""

# Q6: Definition of figure Parallelism.
cq6 = """
SELECT distinct ?Figure ?Definition ?Value
WHERE {
    ?Figure rdfs:label ?FigureName .
    ?Figure rdfs:comment ?Value
    Filter (?FigureName = "Parallelism") }
"""

# Q7: Figures of speech or figures of thought with position beginning
cq7 = """
SELECT distinct ?Figure
WHERE {
    ?Figure esther:IsRhetoricalGroup ?Group .
    ?Group rdfs:label ?GroupName .
    ?Figure esther:IsInPosition ?Position .
    ?Position rdfs:label ?PositionLocation .
    Filter ((?GroupName = "FigureOfSpeech" || ?GroupName = "FigureOfThought") && ?PositionLocation = "Beginning") }
"""

# Q8: Figures with a repeated element of the same form.
cq8 = """
SELECT distinct ?Figure
WHERE {
    ?Figure esther:IsRepeatableElementOfSameForm ?_ .
}
"""

# Q9: Figures where a word in the same form is repeated.
cq9 = """
SELECT distinct ?Figure
WHERE {
    ?Figure esther:IsRepeatableElementOfSameForm ?Element .
    ?Element rdfs:label "WordElement" .
}
"""

# Q10: Figures and their opposite figures.
cq10 = """
SELECT distinct ?FigureA ?FigureB
WHERE {
    ?FigureA esther:IsOppositeFigure ?FigureB .
}
"""


print("Competency Question Q1: Neither a trope nor a figure of construction, but position at the beginning.")
result = g.query(cq1)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print("\nCompetency Question Q2: Rhetorical figures where a letter is omitted.")
result = g.query(cq2)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print("\nCompetency Question Q3: Figures that are neither figures of construction, nor figures of speech, "
      "nor figures of thought.")
result = g.query(cq3)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print("\nCompetency Question Q4: All figure that are tropes (should be same output as cq3).")
result = g.query(cq4)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print("\nCompetency Question Q5: Example sentences for the figure Alliteration.")
result = g.query(cq5)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print("\nCompetency Question Q6: Definition of figure Parallelism.")
result = g.query(cq6)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print("\nCompetency Question Q7: Figures of speech and figures of thought with position beginning.")
result = g.query(cq7)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print("\nCompetency Question Q8: Figures with a repeated element of the same form.")
result = g.query(cq8)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print("\nCompetency Question Q9: Figures where a word in the same form is repeated.")
result = g.query(cq9)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

print("\nCompetency Question Q10: All Figures that have opposite figures.")
result = g.query(cq10)
print(f"Number of matching rhetorical figures: {len(result)}")
for row in result:
    print(row)

