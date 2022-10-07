import re

import rdflib as rdflib

g = rdflib.Graph()
ontology = "esther"

g.parse('./esther.owl',
        format='application/rdf+xml')
esther = rdflib.Namespace('https://anonymous.org/')
g.bind('esther', esther)


def user_inputter():
    operation = input("Operation (addition, removal, repetition, none, ?): ")
    area = input(f"{operation} of (word, sentence, phrase, other, ?): ")
    linguistic_object = input(
        f"{operation} of (same form, different form, same meaning, different meaning, opposed meaning, ?): ")
    position = input(f"{operation} at the (beginning, end, middle, beginning and end): ")

    # print(operation, linguistic_element, linguistic_obejct, position)
    query_builder(operation, area, linguistic_object, position)


def query_builder(operation, area, linguistic_object, position):
    esther_query = """
    SELECT distinct ?Figure
    WHERE {
        ?Figure esther:IsInArea ?Area .
        ?Area rdfs:label ?AreaName .
    Filter (?AreaName = "Word" ) }
"""
    execute_query(esther_query)


    # https://stackoverflow.com/questions/53492632/how-to-use-python-variables-inside-a-sparql-ontology-query

    area = "Word"
    esther_query_parts = []
    select = "SELECT distinct ?Figure"
    where = "WHERE {"
    statements = "?Figure esther:IsInArea ?Area. ?Area rdfs:label ?AreaName ."
    filter = "FILTER ("
    filter_area = "?AreaName ='" + area + "'"
    closing_filter = ")"
    closing_query = "}"

    esther_query_parts.append(select)
    esther_query_parts.append(where)
    esther_query_parts.append(statements)
    esther_query_parts.append(filter)
    esther_query_parts.append(filter_area)
    esther_query_parts.append(closing_filter)
    esther_query_parts.append(closing_query)
    esther_quer = "\n".join(esther_query_parts)
    execute_query(esther_quer)



    # = " SELECT distinct ?Figure    WHERE { ?Figure esther:IsInArea ?Area .  ?Area rdfs:label ?AreaName .Filter (?AreaName = '"+  area + "') }"
    # execute_query(esther_query2)

    # cq8 = """
    # SELECT distinct ?Figure
    # WHERE {
    #     ?Figure esther:IsRepeatableElementOfSameForm ?_ .
    # }
    # """
    # execute_query(cq8)


def execute_query(esther_query):
    result = g.query(esther_query)
    # print(result.serialize(format='csv'))
    # print(RDFS['label'])
    # print(OWL.title)
    # print(RDFS.uri)
    print(f"Following {len(result)} figures fit your description:")
    for row in result:
        row = str(row)
        row = re.sub(r'^.*?#', '', row)
        row = row[:-4]
        # row.split('#', 1)
        # row = row[:-3]
        print(row)
    print("\n")


def main():
    user_inputter()


if __name__ == '__main__':
    main()
