import re
import rdflib

dict_regex = {"directed" : r'^Who directed (.*)\?$',
              "produced" : r'^Who produced (.*)\?$',
              "based on" : r'^Is (.*) based on a book\?$',
              "released" : r'^When was (.*) released\?$',
              "duration" : r'^How long is (.*)\?$',
              "who starred in" : r'^Who starred in (.*)\?$',
              "did starred in" : r'^Did (.*) star in (.*)\?$',
              "born" : r'^When was (.*) born\?$',
              "what occupation" : r'^What is the occupation of (.*)\?$',
              "how many based on" : r'^How many films are based on books\?$',
              "academy award" : r'^How many films starring (.*) won an academy award\?$',
              "two occupations" : r'^How many (.*) are also (.*)\?$',
              "how many duration" : r'^How many films are of length (.*)\?$'}

prefix = "http://en.wikipedia.org/wiki/"


def question_manager(question):
    g = rdflib.Graph().parse('ontology.nt', format='nt')
    key, q = parse_question(question)
    print(call_query(key, q, g))


def parse_question(question):
    for key in dict_regex:
        q = re.search(dict_regex[key], question)
        if q:
            return key, q


def call_query(query_type, regex_output, graph):

    if query_type == "directed":
        film = prefix + regex_output.group(1).replace(" ", "_")
        return directed_query(film, graph)

    if query_type == "produced":
        film = prefix + regex_output.group(1).replace(" ", "_")
        return produced_query(film, graph)

    if query_type == "based on":
        film = prefix + regex_output.group(1).replace(" ", "_")
        return based_on_query(film, graph)

    if query_type == "released":
        film = prefix + regex_output.group(1).replace(" ", "_")
        return released_query(film, graph)

    if query_type == "duration":
        film = prefix + regex_output.group(1).replace(" ", "_")
        return duration_query(film, graph)

    if query_type == "who starred in":
        film = prefix + regex_output.group(1).replace(" ", "_")
        return who_starred_in_query(film, graph)

    if query_type == "did starred in":
        person = prefix + regex_output.group(1).replace(" ", "_")
        film = prefix + regex_output.group(2).replace(" ", "_")
        return did_starred_in_query(person, film, graph)

    if query_type == "born":
        person = prefix + regex_output.group(1).replace(" ", "_")
        return born_query(person, graph)

    if query_type == "what occupation":
        person = prefix + regex_output.group(1).replace(" ", "_")
        return what_occupation_query(person, graph)

    if query_type == "how many based on":
        return how_many_based_on_query(graph)

    if query_type == "academy award":
        person = prefix + regex_output.group(1).replace(" ", "_")
        return academy_award_query(person, graph)

    if query_type == "two occupations":
        occupation1 = prefix + regex_output.group(1).replace(" ", "_")
        occupation2 = prefix + regex_output.group(2).replace(" ", "_")
        return two_occupations_query(occupation1, occupation2, graph)

    if query_type == "how many duration":
        duration = prefix + regex_output.group(1).replace(" ", "_")
        return how_many_duration_query(duration, graph)


def directed_query(film, graph):
    query = f"SELECT ?person WHERE {{?person <http://en.wikipedia.org/directed> <{film}>.}}"
    output = execute_query(query, graph)
    return extract_answer(output)


def produced_query(film, graph):
    query = f'''SELECT ?person WHERE {{?person <http://en.wikipedia.org/produced> <{film}>.}}'''
    output = execute_query(query, graph)
    return extract_answer(output)


def based_on_query(film, graph):
    query = f'''SELECT (COUNT(*) as ?count) WHERE {{<{film}> <http://en.wikipedia.org/based_on> ?book.}}'''
    output = execute_query(query, graph)
    if int(output[0][0]) > 0:
        return "Yes"
    return "No"


def released_query(film, graph):
    query = f'''SELECT ?date WHERE {{<{film}> <http://en.wikipedia.org/released> ?date.}}'''
    output = execute_query(query, graph)
    return extract_answer(output)


def duration_query(film, graph):
    query = f'''SELECT ?duration WHERE {{<{film}> <http://en.wikipedia.org/duration> ?duration.}}'''
    output = execute_query(query, graph)
    return extract_answer(output)


def who_starred_in_query(film, graph):
    query = f'''SELECT ?person WHERE {{?person <http://en.wikipedia.org/starred_in> <{film}>.}}'''
    output = execute_query(query, graph)
    return extract_answer(output)


def did_starred_in_query(person, film, graph):
    query = f'''SELECT (COUNT(*) as ?count) WHERE {{<{person}> <http://en.wikipedia.org/starred_in> <{film}>.}}'''
    output = execute_query(query, graph)
    if int(output[0][0]) > 0:
        return "Yes"
    return "No"


def born_query(person, graph):
    query = f'''SELECT ?date WHERE {{<{person}> <http://en.wikipedia.org/born> ?date.}}'''
    output = execute_query(query, graph)
    return extract_answer(output)


def what_occupation_query(person, graph):
    query = f'''SELECT ?occupation WHERE {{<{person}> <http://en.wikipedia.org/occupation> ?occupation.}}'''
    output = execute_query(query, graph)
    return extract_answer(output)


def how_many_based_on_query(graph):
    query = f'''SELECT DISTINCT (COUNT(*) as ?count) WHERE {{?film <http://en.wikipedia.org/based_on> ?book.}}'''
    output = execute_query(query, graph)
    return str(output[0][0])


def academy_award_query(person, graph):
    query = f'''SELECT DISTINCT (COUNT(*) as ?count) WHERE {{<{person}> <http://en.wikipedia.org/starred_in> ?film.}}'''
    output = execute_query(query, graph)
    return str(output[0][0])


def two_occupations_query(occupation1, occupation2, graph):
    query = f'''SELECT (COUNT(DISTINCT(?person)) as ?count) WHERE {{?person <http://en.wikipedia.org/occupation> <{occupation1}>. ?person <http://en.wikipedia.org/occupation> <{occupation2}>.}}'''
    output = execute_query(query, graph)
    return str(output[0][0])


def how_many_duration_query(duration, graph):
    query = f'''SELECT DISTINCT (COUNT(*) as ?count) WHERE {{?film <http://en.wikipedia.org/duration> <{duration}>.}}'''
    output = execute_query(query, graph)
    return str(output[0][0])


def execute_query(query, graph):
    return list(graph.query(query))


def extract_answer(output):
    answer = [t[0].split("/")[-1].replace("_", " ") for t in output]
    answer.sort()
    return ', '.join(answer)


