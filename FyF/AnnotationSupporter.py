import re
from ESTHEREnums import *
import rdflib as rdflib

g = rdflib.Graph()
ontology = "esther"

g.parse('./esther.owl',
        format='application/rdf+xml')
esther = rdflib.Namespace('https://anonymous.org/')
g.bind('esther', esther)

error_message = "Invalid {}. Please choose one from the list above."


def build_enum_string(enum_class):
    enum_string = ""
    for enum in enum_class:
        enum_string += str(enum.value)
        enum_string += str(", ")
    enum_string = enum_string[:-2]  # remove last comma
    return enum_string


def user_inputter():
    operation_enum_string = build_enum_string(Operation)
    linguistic_element_enum_string = build_enum_string(LinguisticElement)
    linguistic_object_enum_string = build_enum_string(LinguisticObject)
    position_enum_string = build_enum_string(Position)

    while True:
        operation = input(f"Operation ({operation_enum_string}): ").capitalize().strip()
        if operation not in [member.value for member in Operation]:
            print(error_message.format("operation"))
            continue
        else:
            break
    while True:
        linguistic_element = input(
            f"Linguistic Element: {operation} of ({linguistic_element_enum_string}): ").capitalize().strip()
        if linguistic_element not in [member.value for member in LinguisticElement]:
            print(error_message.format("linguistic element)"))
            continue
        else:
            break

    while True:
        linguistic_object = input(
            f"Linguistic Object: {operation} of ({linguistic_object_enum_string}): ").capitalize().strip()
        if linguistic_object not in [member.value for member in LinguisticObject]:
            print(error_message.format("linguistic object"))
            continue
        else:
            break
    while True:
        position = input(f"Position: {operation} at the ({position_enum_string}): ").capitalize().strip()
        if position not in [member.value for member in Position]:
            print(error_message.format("position"))
            continue
        else:
            print(
                f"...Searching for figures with {operation} of a {linguistic_element} in {linguistic_object} at the {position}...")
            query_builder(operation, linguistic_element, linguistic_object, position)


def query_builder(operation, linguistic_element, linguistic_object, position):
    # https://stackoverflow.com/questions/53492632/how-to-use-python-variables-inside-a-sparql-ontology-query
    if operation == Operation.REPETITION and linguistic_object == LinguisticObject.SAME_FORM:
        operation = "IsRepeatableElementOfSameForm"
    linguistic_element += "Element"

    esther_query_parts = []
    select = "SELECT distinct ?Figure"
    where = "WHERE {"
    statement_area = "?Figure esther:IsInArea ?Area. ?Area rdfs:label ?AreaName ."
    statement_position = "?Figure esther:IsInPosition ?Position. ?Position rdfs:label ?PositionName ."
    filter = "FILTER ("
    filter_area = "?AreaName ='" + linguistic_element + "' && ?PositionName = '" + position + "'"
    closing_filter = ")"
    closing_query = "}"

    esther_query_parts.append(select)
    esther_query_parts.append(where)
    esther_query_parts.append(statement_area)
    esther_query_parts.append(statement_position)
    esther_query_parts.append(filter)
    esther_query_parts.append(filter_area)
    esther_query_parts.append(closing_filter)
    esther_query_parts.append(closing_query)
    esther_query = "\n".join(esther_query_parts)

    execute_query(esther_query)


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

    # SELECT  ?title
    # WHERE
    # { ?x
    # dc: title ?title
    # FILTER
    # regex(?title, "web", "i" )
    # }


def execute_normal_query(query):
    result = g.query(query)
    for row in result:
        print(row)


def main():
    user_inputter()

    # query = """ Select Distinct ?property
    # where {?class ?property ?value }
    #    """
    # # execute_query(query)
    #
    # query2 = """
    # Select distinct ?class
    # where {?bla a ?class}
    # """
    # execute_normal_query(query2)

    # cq5 = """
    # SELECT distinct ?Figure ?Example ?Value
    # WHERE {
    #     ?Figure rdfs:label ?FigureName .
    #     ?Figure esther:IsExample ?Value
    #     Filter (?FigureName = "Hendiadys") }
    # """
    # execute_normal_query(cq5)
    #
    #
    # queryx = """
    # SELECT ?Figure
    # where {
    #     ?Figure :LinguisitcOperation
    #
    # """


if __name__ == '__main__':
    main()
