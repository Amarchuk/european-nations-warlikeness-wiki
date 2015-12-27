# European nations warlikeness by Wikipedia.EN

**About:** This is a one-day project inspired by [this answer on Quora](http://qr.ae/RbjT5R). It provided interesting information from one sociological study:

>Professor Quincy Wright offers this further statistical evidence for the same period, that is, 1480-1940:

>Of the 278 wars involving European states during this period, the percentage of participation by the principal states was: England, 28; France, 26; Spain, 23; Russia, 22; Austria, 19; Turkey, 15; Poland, 11; Sweden, 9; Netherlands, 8; Germany (Prussia), 8; Italy (Savoy-Sardinia), 9; and Denmark, 7.

As anybody can see, there are no nation among the others that significantly was more addicted to wars. I try to find the full text of original quote in public acess and failed, so I wonder to check it by my own. I notice that Wikipedia has special [page](https://en.wikipedia.org/wiki/List_of_conflicts_in_Europe) listing every conflict in Europe with information about it belligerents and all I need to do is to parse the list and count countries.

**New tech background**: I want to try in action [Dbpedia](http://wiki.dbpedia.org/) with [SPARQL](http://dbpedia.org/sparql) queries and html parsing in python via [BeautifulSoup](https://wiki.python.org/moin/beautiful%20soup) (eh, weird name).

**Troubles:** 
1. SPARQL is tricky and confused. Due to huge amount of time for understanding it and lack of data in Dbpedia I realize that easiest way will be to crawl and parse wiki by myself.   
2. it is not obvious, how to count data properly for countries with several names (e.g. England equals Great Britain equals British Empire equals United Kingdom etc). I came up with few possible solutions started with manually write dictionary for synonym country's names. And it works. Second solution was to use wikipedia flag icon, that stands the same for many different country names. The last one was to use [List of alternative country names](https://en.wikipedia.org/wiki/List_of_alternative_country_names) that I wasn't make.
3. assumptions in counting throw different names and equality between wars (e.g. small vs huge, short vs long)

**Results:**  The result is quite similar to Wright's data and different at the same time.  Both sets suggest that there is no nation in Europe that significally more often involved in wars comparatively to others. The differences are in numbers and in positions inside top-12 countries. I suppose that it is true because of manual data collection and moving off negligible conflicts from discussion in previous study. Also small bias may be related to my treatment of name synonyms.

| Country     | #Wars |
| ----------- |:-----:|
| Denmark     |  15   |   
| Sweden      |  17   |   
| Poland      |  20   |  
| Netherlands |  21   |  
| Austria     |  23   |  
| Spain       |  26   |   
| Italy       |  36   |  
| England     |  37   |
| Russia      |  39   |
| France      |  39   |
| Germany     |  44   |
| Turkey      |  46   |
