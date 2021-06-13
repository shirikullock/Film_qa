import rdflib
import requests
import lxml.html
import re


g = rdflib.Graph()

# Relations
duration = rdflib.URIRef('http://en.wikipedia.org/duration')
released = rdflib.URIRef('http://en.wikipedia.org/released')
directed = rdflib.URIRef('http://en.wikipedia.org/directed')
produced = rdflib.URIRef('http://en.wikipedia.org/produced')
starred_in = rdflib.URIRef('http://en.wikipedia.org/starred_in')
based_on = rdflib.URIRef('http://en.wikipedia.org/based_on')

born = rdflib.URIRef('http://en.wikipedia.org/born')
occupation = rdflib.URIRef('http://en.wikipedia.org/occupation')

prefix = "http://en.wikipedia.org"
prefix_not_href = "http://en.wikipedia.org/wiki/"
visited_people = set()
people = []


def start_to_crawl():
    crawl("https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films")
    return


def crawl(url):
    movies = []
    r = requests.get(url)
    doc = lxml.html.fromstring(r.content)
    for t in doc.xpath("//table[1]//tr[td[2]/a[1]/text() > '2009']//td[1]//a[contains(@href, '/wiki/')]/@href"):
        movies.append(f"{prefix}{t}")

    for next_movie in movies:
        crawl_movie(next_movie)

    for person in people:
        crawl_person(person)

    g.serialize("ontology.nt", format="nt")
    return


def crawl_movie(url):
    movie_node = rdflib.URIRef(url)

    r = requests.get(url)
    doc = lxml.html.fromstring(r.content)

    # Duration
    for t in doc.xpath("//table[contains(@class, 'infobox')]//tr[contains(th//text(), 'Running time')]//td[1]/text()"):
        movie_duration = rdflib.URIRef(f"{prefix_not_href}" + t.strip().replace(' ', '_'))
        g.add((movie_node, duration, movie_duration))
    for t in doc.xpath("//table[contains(@class, 'infobox')]//tr[contains(th//text(), 'Running time')]//td[1]//li/text()"):
        movie_duration = rdflib.URIRef(f"{prefix_not_href}" + t.strip().replace(' ', '_'))
        g.add((movie_node, duration, movie_duration))

    # Released
    for t in doc.xpath("//table[contains(@class, 'infobox')]//tr[contains(th//text(), 'Release date')]//span[contains(@class, 'bday')]/text()"):
        release_date = rdflib.URIRef(f"{prefix_not_href}" + t.strip().replace(' ', '_'))
        g.add((movie_node, released, release_date))

    # Based on
    for t in doc.xpath("//table[contains(@class, 'infobox')]//tr[contains(th//text(), 'Based on')]"):
        based = rdflib.URIRef(f"{prefix_not_href}"+"yes")
        g.add((movie_node, based_on, based))
        break

    # Directed
    for t in doc.xpath("//table[contains(@class, 'infobox')]//tr[contains(th//text(), 'Directed by')]//td[1]//a[not(contains(@href, 'cite_note'))]/@href"):
        director = rdflib.URIRef(f"{prefix}{t.strip().replace(' ', '_')}")
        g.add((director, directed, movie_node))
        if t not in visited_people:
            visited_people.add(t)
            people.append(f"{prefix}{t.strip().replace(' ', '_')}")
    for t in doc.xpath("//table[contains(@class, 'infobox')]//tr[contains(th//text(), 'Directed by')]//td[1]//li/text()"):
        director = rdflib.URIRef(f"{prefix_not_href}" + t.strip().replace(' ', '_'))
        g.add((director, directed, movie_node))
    for t in doc.xpath("//table[contains(@class, 'infobox')]//tr[contains(th//text(), 'Directed by')]//td[1]/text()"):
        if t.strip() is not "":
            director = rdflib.URIRef(f"{prefix_not_href}" + t.strip().replace(' ', '_'))
            g.add((director, directed, movie_node))

    # Produced
    for t in doc.xpath("//table[contains(@class, 'infobox')]//tr[contains(th//text(), 'Produced by')]//td[1]//a[not(contains(@href, 'cite_note'))]/@href"):
        producer = rdflib.URIRef(f"{prefix}{t.strip().replace(' ', '_')}")
        g.add((producer, produced, movie_node))
        if t not in visited_people:
            visited_people.add(t)
            people.append(f"{prefix}{t.strip().replace(' ', '_')}")
    for t in doc.xpath("//table[contains(@class, 'infobox')]//tr[contains(th//text(), 'Produced by')]//td[1]//li/text()"):
        producer = rdflib.URIRef(f"{prefix_not_href}" + t.strip().replace(' ', '_'))
        g.add((producer, produced, movie_node))
    for t in doc.xpath("//table[contains(@class, 'infobox')]//tr[contains(th//text(), 'Produced by')]//td[1]/text()"):
        if t.strip() is not ":":
            producer = rdflib.URIRef(f"{prefix_not_href}" + t.strip().replace(' ', '_'))
            g.add((producer, produced, movie_node))


    # Starred
    for t in doc.xpath("//table[contains(@class, 'infobox')]//tr[contains(th//text(), 'Starring')]//td[1]//a[not(contains(@href, 'cite_note'))]/@href"):
        actor = rdflib.URIRef(f"{prefix}{t.strip().replace(' ', '_')}")
        g.add((actor, starred_in, movie_node))
        if t not in visited_people:
            visited_people.add(t)
            people.append(f"{prefix}{t.strip().replace(' ', '_')}")
    for t in doc.xpath("//table[contains(@class, 'infobox')]//tr[contains(th//text(), 'Starring')]//td[1]/text()"):
        actor = rdflib.URIRef(f"{prefix_not_href}" + t.strip().replace(' ', '_'))
        g.add((actor, starred_in, movie_node))
    for t in doc.xpath("//table[contains(@class, 'infobox')]//tr[contains(th//text(), 'Starring')]//td[1]//li/text()"):
        actor = rdflib.URIRef(f"{prefix_not_href}" + t.strip().replace(' ', '_'))
        g.add((actor, starred_in, movie_node))


def crawl_person(person):
    person_node = rdflib.URIRef(person)

    r = requests.get(person)
    doc = lxml.html.fromstring(r.content)

    # Born
    ind_bday_found = 0
    if ind_bday_found == 0:
        for t in doc.xpath("//table[contains(@class, 'infobox biography') or contains(@class, 'infobox vcard')]//tr[contains(th/text(), 'Born')]/td[1]//span[contains(@class, 'bday')]/text()"):
            ind_bday_found = 1
            t = t.strip().replace(' ', '_')
            bday = rdflib.URIRef(f"{prefix_not_href}{t}")
            g.add((person_node, born, bday))
    if ind_bday_found == 0:
        for t in doc.xpath("//table[contains(@class, 'infobox biography') or contains(@class, 'infobox vcard')]//tr[contains(th//text(), 'Born')]//td[1]/text()"):
            years = re.findall(r'(\d{4})', t)
            if len(years) > 0:
                years = [int(y) for y in years]
                min_year = min(years)
                bday = rdflib.URIRef(f"{prefix_not_href}{min_year}")
                g.add((person_node, born, bday))

    # Occupation
    for t in doc.xpath("//table[contains(@class, 'infobox biography') or contains(@class, 'infobox vcard')]//tr[contains(th//text(), 'Occupation')]//td[1]//li/text()"):
        if t.strip() is not "":
            person_occupation = rdflib.URIRef(f"{prefix_not_href}" + t.lower().strip().replace(' ', '_'))
            g.add((person_node, occupation, person_occupation))
    for t in doc.xpath("//table[contains(@class, 'infobox biography') or contains(@class, 'infobox vcard')]//tr[contains(th//text(), 'Occupation')]//td[1]/text()"):
        for occ in re.split(',',t):
            if occ.strip() is not "":
                person_occupation = rdflib.URIRef(f"{prefix_not_href}" + occ.lower().strip().replace(' ', '_'))
                g.add((person_node, occupation, person_occupation))
    for t in doc.xpath("//table[contains(@class, 'infobox biography') or contains(@class, 'infobox vcard')]//tr[contains(th//text(), 'Occupation')]//td[1]//li/a/@href"):
        if t.strip() is not "":
            person_occupation = rdflib.URIRef(f"{prefix}{t.strip().lower().replace(' ', '_')}")
            g.add((person_node, occupation, person_occupation))
    for t in doc.xpath("//table[contains(@class, 'infobox biography') or contains(@class, 'infobox vcard')]//tr[contains(th//text(), 'Occupation')]//td[1]/a/@href"):
        if t.strip() is not "":
            person_occupation = rdflib.URIRef(f"{prefix}{t.strip().lower().replace(' ', '_')}")
            g.add((person_node, occupation, person_occupation))
