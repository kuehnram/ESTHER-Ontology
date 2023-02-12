__author__ = "Anonymous"
__license__ = "MIT"
__version__ = "1.0."
__email__ = "a@b.c"

"""This tool helps users to find the proper name of a rhetorical figure. Often, it is easy to name the properties of
a figure, but it is hard to tell which name the figure has. With this tool, the users can specify the properties. 
Those are then translated into a SPARQL query which is executed on the ESTHER ontology, the ontology of rhetorical 
figure in the English Language. The name of the figure, its definition, and examples are presented to the user.
If the search was not successful, the users have the possibility to search for key words, separated by commas.
"""

import re
from ESTHEREnums import *
import rdflib as rdflib
from itertools import islice

g = rdflib.Graph()
ontology = "esther"
g.parse('../esther.owl', format='application/rdf+xml')
esther = rdflib.Namespace('https://anonymous.org/')
g.bind('esther', esther)

error_message = "Invalid {}. Please choose one from the list above."


def take(n, iterable):
    """Return first n items of the iterable as a list"""
    return list(islice(iterable, n))


def build_enum_string(enum_class):
    """Retrieve the enums from class ESTHEREnums and build strings, to present them to the user in user_inputter()"""
    enum_string = ""
    enum: Enum
    for i, enum in enumerate(enum_class, start=0):

        enum_string += f"{i}: {enum.value}\n"
    enum_string = enum_string.strip()
    return enum_string


def user_inputter():
    """Ask the users for their input/properties. The suggested properties are Enums from the class ESTHEREnums"""
    operation_enum_string = build_enum_string(Operation)
    linguistic_element_enum_string = build_enum_string(LinguisticElement)
    linguistic_object_enum_string = build_enum_string(LinguisticObject)
    position_enum_string = build_enum_string(Position)

    while True:
        try:
            operation_id = int(input(f"Which Operation takes place?\n"
                                     f"{operation_enum_string}\n"
                                     f"Your choice: ").strip())
            operations = [member.value for member in Operation]
            if operation_id not in range(len(Operation)):
                print(error_message.format("operation"))
                continue
            else:
                operation = operations[operation_id]
                print(f"Selected: {operation}")
                break
        except ValueError:
            continue
    print()

    while True:
        try:
            # noinspection PyUnboundLocalVariable
            linguistic_element_id = int(input(f"Which linguistic element is affected? {operation} of:\n"
                                              f"{linguistic_element_enum_string}\n"
                                              f"Your choice: ").strip())
            linguistic_elements = [member.value for member in LinguisticElement]
            if linguistic_element_id not in range(len(linguistic_elements)):
                print(error_message.format("linguistic element"))
                continue
            else:
                linguistic_element = linguistic_elements[linguistic_element_id]
                print(f"Selected: {linguistic_element}")
                if linguistic_element not in [LinguisticElement.LETTER.value,
                                              LinguisticElement.CONSONANT.value,
                                              LinguisticElement.QM.value]:
                    linguistic_element += "Element"
                break
        except ValueError:
            continue
    print()

    while True:
        try:
            area_id = int(input(f"In which area does {operation} occur:\n"
                                f"{linguistic_element_enum_string}\n"
                                f"Your choice: ").strip())
            areas = [member.value for member in LinguisticElement]
            if area_id not in range(len(areas)):
                print(error_message.format("area"))
                continue
            else:
                area = areas[area_id]
                print(f"Selected: {area}")
                break
        except ValueError:
            continue
    print()

    while True:
        try:
            linguistic_object_id = int(input(f"Linguistic Object: {operation} of\n"
                                             f"{linguistic_object_enum_string}\n"
                                             f"Your choice: ").strip())
            linguistic_objects = [member.value for member in LinguisticObject]
            if linguistic_object_id not in range(len(linguistic_objects)):
                print(error_message.format("linguistic object"))
                continue
            else:
                linguistic_object = linguistic_objects[linguistic_object_id]
                print(f"Selected: {linguistic_object}")
                break
        except ValueError:
            continue
    print()

    while True:
        try:
            position_id = int(input(f"Position: {operation} at the\n"
                                    f"{position_enum_string}\n"
                                    f"Your choice: ").strip())
            positions = [member.value for member in Position]
            if position_id not in range(len(positions)):
                print(error_message.format("position"))
                continue
            else:
                position = positions[position_id]
                if position == Position.BEGINNING_AND_END.value:
                    position = "BeginningAndEnd"
                print(f"Selected: {position}")
                break
        except ValueError:
            continue

    # Variables are bound otherwise while True would not have exited -> we can ignore the Inspection
    # noinspection PyUnboundLocalVariable
    print(
        f"\n...Searching for figures with {operation} of a {linguistic_element} in {linguistic_object} at the {position}...")
    # noinspection PyUnboundLocalVariable
    query_builder(operation, area, linguistic_element, linguistic_object, position)


def query_builder(operation, area, linguistic_element, linguistic_object, position):
    """Build a query with the specified properties. Properties are only appended if they are known.
    Combinations of operations and linguistic objects yield certain operations."""

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
    filter_area = "?AreaName ='" + area + "' "
    filter_position = "?PositionName = '" + position + "'"
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
    # print(esther_query)
    execute_query(esther_query)


def pretty_print_text(result_list, string_name):
    """Cut off irrelevant information and show only definitions or examples"""
    for result in result_list:
        result = str(result)
        result = re.sub(r'^.*?term.Literal\(', "", result)
        result = result.split(", datatype=", 1)
        print(f"{string_name}: {result[0]}")


def get_definition_and_examples(figure_name):
    """Retrieve definition and examples for a given figure name"""
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
    print()  # new line looks better


def execute_query(esther_query):
    """Executes a query and prints the figure name, definitions, and examples nicely. If no matching figure was found,
    the users have the possibility to search for free text"""
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
    """If no figure matches, users can search for commaseparated keywords that might appear in the definition.
    The results are then sorted descending according to the number of appearances of the keywords"""
    print("No figure matches the provided properties: Try to type comma-separated keywords:")
    keywords = input(f"Comma-separated keywords: ")
    keywords = keywords.split(",")
    keywords = [elem.strip() for elem in keywords]

    get_all_figure_definitions = """
    SELECT DISTINCT ?Figure ?Definition ?Value
    WHERE {
    ?Figure rdfs:comment ?Value.} """
    all_figure_definitions = g.query(get_all_figure_definitions)

    possible_candidates_dict = {}  # Dict[str, int] = Dict[definition is key, number of occurrence of the keywords]
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
    """Execute a query without any output styling or examples or definitions"""
    result = g.query(query)
    print(len(result))
    for row in result:
        print(row)


def main():
    print("Welcome to Find your Figure! Please specify the following characteristics.")
    user_inputter()


if __name__ == '__main__':
    main()
