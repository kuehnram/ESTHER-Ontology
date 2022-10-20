import re
from ESTHEREnums import *
import rdflib as rdflib
from itertools import islice

g = rdflib.Graph()
ontology = "esther"

g.parse('../esther.owl',
        format='application/rdf+xml')
esther = rdflib.Namespace('https://anonymous.org/')
g.bind('esther', esther)

error_message = "Invalid {}. Please choose one from the list above."


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


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
            # if operation == Operation.QM.value:
            #     operation = "_"
            break

    while True:
        linguistic_element = input(
            f"Linguistic Element: {operation} of ({linguistic_element_enum_string}): ").capitalize().strip()
        if linguistic_element not in [member.value for member in LinguisticElement]:
            print(error_message.format("linguistic element)"))
            continue
        else:
            # if linguistic_element == LinguisticElement.QM.value:
            #     linguistic_element = "_"
            # else:
            if linguistic_element != LinguisticElement.LETTER.value and linguistic_element != LinguisticElement.CONSONANT.value and linguistic_element != LinguisticElement.QM.value:
                linguistic_element += "Element"
            break

    while True:
        area = input(f"In which area does {operation} occur ({linguistic_element_enum_string}): ").capitalize().strip()
        if area not in [member.value for member in LinguisticElement]:
            print(error_message.format("area"))
            continue
        else:
            # if area == LinguisticElement.QM.value:
            #     area = "_"
            break

    while True:
        linguistic_object = input(
            f"Linguistic Object: {operation} of ({linguistic_object_enum_string}): ").capitalize().strip()
        if linguistic_object not in [member.value for member in LinguisticObject]:
            print(error_message.format("linguistic object"))
            continue
        else:
            # if linguistic_object == LinguisticObject.QM.value:
            #     linguistic_object = "_"
            break
    while True:
        position = input(f"Position: {operation} at the ({position_enum_string}): ").capitalize().strip()
        if position not in [member.value for member in Position]:
            print(error_message.format("position"))
            continue
        else:
            # if position == Position.QM.value:
            #     position = "_"
            if position == Position.BEGINNING_AND_END.value:
                position = "BeginningAndEnd"
            break

    print(
        f"\n...Searching for figures with {operation} of a {linguistic_element} in {linguistic_object} at the {position}...")
    query_builder(operation, area, linguistic_element, linguistic_object, position)


def query_builder(operation, area, linguistic_element, linguistic_object, position):
    # https://stackoverflow.com/questions/53492632/how-to-use-python-variables-inside-a-sparql-ontology-query

    if operation == Operation.REPETITION.value and linguistic_object == LinguisticObject.SAME_FORM.value:
        operation = "IsRepeatableElementOfSameForm"
    if operation == Operation.REPETITION.value and linguistic_object == LinguisticObject.DIFFERENT_FORM.value:
        operation = "IsRepeatableElementOfDifferentForm"
    if operation == Operation.OMISSION.value:
        operation = "IsOmitted"
    if operation == Operation.REPLACEMENT.value and linguistic_object == LinguisticObject.SAME_MEANING.value:
        operation = "IsReplacedByAnotherElementOfSameMeaning"
    if operation == Operation.REPLACEMENT.value and linguistic_object == LinguisticObject.DIFFERENT_FORM.value:
        operation = "IsReplacedByAnotherElementOfDifferentForm"
    if operation == Operation.REPLACEMENT.value and linguistic_object == LinguisticObject.OPPOSED_MEANING.value:
        operation = "IsReplacedByElementOfOppositeMeaning"

    esther_query_parts = []
    select = "SELECT DISTINCT ?Figure"
    where = "WHERE {"
    statement_area = "?Figure esther:IsInArea ?Area . "
    statement_area_name = "?Area rdfs:label ?AreaName ."
    statement_position = "?Figure esther:IsInPosition ?Position . "
    statement_position_name = "?Position rdfs:label ?PositionName ."
    statement_operation = "?Figure esther:" + operation + " ?LinguisticElement ."
    statement_operation_name = "?LinguisticElement rdfs:label ?LingElementName ."
    filter = "FILTER ("
    and_bool = " && "
    # if area == "_":
    #     filter_area = "?AreaName = _"
    # else:
    filter_area = "?AreaName ='" + area + "' "
    # if position == "_":
    #     filter_position = "?PositionName = _"
    # else:
    filter_position = "?PositionName = '" + position + "'"
    # if linguistic_element == "_":
    #     filter_ling_elem = "?LingElementName = _"
    # else:
    filter_ling_elem = "?LingElementName = '" + linguistic_element + "'"
    closing_filter = ")"
    closing_query = "}"

    esther_query_parts.append(select)
    esther_query_parts.append(where)
    if area != LinguisticElement.QM.value:
        esther_query_parts.append(statement_area)
        esther_query_parts.append(statement_area_name)
    else:
        esther_query_parts.append(statement_area)

    if position != Position.QM.value:
        esther_query_parts.append(statement_position)
        esther_query_parts.append(statement_position_name)
    else:
        esther_query_parts.append(statement_position)

    if operation != Operation.QM.value:
        esther_query_parts.append(statement_operation)
        esther_query_parts.append(statement_operation_name)
    # else:
    #     esther_query_parts.append(statement_operation)

    if area != LinguisticElement.QM.value or position != Position.QM.value or operation != Operation.QM.value:
        esther_query_parts.append(filter)
    if area != LinguisticElement.QM.value:
        esther_query_parts.append(filter_area)

    if position != Position.QM.value:
        if area != LinguisticElement.QM.value:
            esther_query_parts.append(and_bool)
        esther_query_parts.append(filter_position)

    if linguistic_element != LinguisticElement.QM.value:
        if area != LinguisticElement.QM.value or position != Position.QM.value:
            esther_query_parts.append(and_bool)
        esther_query_parts.append(filter_ling_elem)

    if area != LinguisticElement.QM.value or position != Position.QM.value or operation != Operation.QM.value:
        esther_query_parts.append(closing_filter)
    esther_query_parts.append(closing_query)
    esther_query = "\n".join(esther_query_parts)

    if area == LinguisticElement.QM.value and position == Position.QM.value and operation == Operation.QM.value and linguistic_element == LinguisticElement.QM.value and linguistic_object == LinguisticObject.QM.value:
        esther_query = """ SELECT DISTINCT ?Figure
        WHERE {?Figure esther:IsInArea ?Area . 
        }
        """

    print(esther_query)
    execute_query(esther_query)


def pretty_print_text(result_list, string_name):
    for result in result_list:
        result = str(result)
        result = re.sub(r'^.*?term.Literal\(', "", result)
        result = result.split(", datatype=", 1)
        print(f"{string_name}: {result[0]}")


def get_definition_and_examples(figure_name):
    definition = """
            SELECT distinct ?Figure ?Definition ?Value
                 WHERE {
                     ?Figure rdfs:label ?FigureName .
                     ?Figure rdfs:comment ?Value
                     Filter (?FigureName = '""" + figure_name + "') } """
    definition_result = g.query(definition)
    pretty_print_text(definition_result, "DEFINITION")

    example_sentence = """
            SELECT distinct ?Figure ?Example ?Value
              WHERE   {
              ?Figure   rdfs:label ?FigureName.
              ?Figure   esther:IsExample ?Value
              Filter(?FigureName = '""" + str(figure_name) + "')}"""
    example_result = g.query(example_sentence)
    pretty_print_text(example_result, "EXAMPLE")
    print()


def execute_query(esther_query):
    result = g.query(esther_query)
    result_length = len(result)
    if result_length > 0:
        print(f"Following {result_length} figures fit your description:")

        for row in result:
            row = str(row)
            row = re.sub(r'^.*?#', '', row)
            row = row[:-4]
            print(row)
            get_definition_and_examples(row)
    else:
        free_text_search()


def free_text_search():
    print("No figure matches the provided properties: Try to type comma-separated keywords:")
    keywords = input(f"Comma-separated keywords: ")
    keywords = keywords.split(",")
    keywords = [elem.strip() for elem in keywords]

    get_all_figure_definitions = """
    SELECT
    distinct ?Figure ?Definition ?Value
    WHERE
    {
    ?Figure
    rdfs: comment ?Value.} """
    all_figure_definitions = g.query(get_all_figure_definitions)

    possible_candidates_dict = {}  # Dict[str, int] = Dict[definition is key, number of occurence of the keywords]
    for definition in all_figure_definitions:
        for keyword in keywords:
            if str(keyword).lower() in str(definition).lower():
                if definition in possible_candidates_dict:
                    possible_candidates_dict[definition] += 1
                else:
                    possible_candidates_dict[definition] = 1

    if len(possible_candidates_dict) > 0:
        # Sort descending, definition with most matches has the highest number
        sorted_dict = dict(sorted(possible_candidates_dict.items(),
                                  key=lambda item: item[1],
                                  reverse=True))

    # Comment out to print only three top elements of sorted_dict
    # n_items = take(3, sorted_dict.items())

    for result in sorted_dict:
        result = str(result)
        figure_name = re.sub(r'^.*?#', '', result)
        figure_name = figure_name.split("'), None, rdflib.term", 1)
        figure_name = figure_name[0]
        print(figure_name)
        get_definition_and_examples(figure_name)
    else:
        print("Sorry, no match found!")


def execute_normal_query(query):
    result = g.query(query)
    print(len(result))
    for row in result:
        row = str(row)
        row = re.sub(r'^.*?#', '', row)
        row = row[:-4]
        print(row)
        get_definition_and_examples(row)

def main():
    print("Welcome to Find your Figure! Please specify the following characteristics.")
    user_inputter()
    # free_text_search()

    blub = """
SELECT DISTINCT ?Figure
WHERE { 
?Figure esther:IsInPosition ?Position . 
?Position rdfs:label ?PositionName .
?Figure esther:Repetition ?LinguisticElement .
?LinguisticElement rdfs:label ?LingElementName .
FILTER (
?PositionName = 'Beginning'
 && 
?LingElementName = 'WordElement'
)
}
    
    """
    # execute_normal_query(blub)



if __name__ == '__main__':
    main()