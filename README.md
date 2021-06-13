# Film_qa
Creats an Ontology based on winning Oscar films (since 2010) from Wikipedia, 
And allows querying it.

The crawler collects the following details on each film:
1. Release dates
2. Lenghts in minutes
3. Is/ is not based on a book
4. Produces
5. Directors
6. Start
And the following details on each producer/ director/ actor mentioned in one of the movies:
1. Birthday
2. Occupations

Supported queries' formats:
1. Who directed <film>?
2. Who produced <film>?
3. Is <film> based on a book?
4. When was <film> released?
5. How long is <film>?
6. Who starred in <film>?
7. Did <person> star in <film>?
8. When was <person> born?
9. What is the occupation of <person>?
10. How many films are based on books?
11. How many films starring <person> won an academy award?
12. How many <occupation1> are also < occupation2>?
13. How many movies are of length <duration>?

# How to use film_qa:
Creating an Ontology - python3 film_qa.py create
Querying the Ontology - python3 film_qa.py question <"your question">
