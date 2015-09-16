#-*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import urllib2
import re
import operator

wiki = 'https://en.wikipedia.org'
wikilist = wiki + '/wiki/List_of_conflicts_in_Europe'
html_page = urllib2.urlopen(wikilist)
soup = BeautifulSoup(html_page)

dirty_warlist = []
inrange = False
for li in soup.findAll('li'):
    if len(li.contents) > 1 and str(li.contents[1]).startswith('<a href="'):
        # Start counting from 1479 - Battle of Guinegate
        # and finish in 1939 - Slovak-Hungarian War
        if str(li.contents[1]).__contains__('Battle of Guinegate'):
            inrange = True
        if inrange:
            #check page existence and language
            if not str(li.contents[1]).__contains__('class="new"') and \
                    not str(li.contents[1]).__contains__('class="extiw"'):
                dirty_warlist.append(li)
        if str(li.contents[1]).__contains__('Slovak-Hungarian War'):
            break

belligerents = {}
sideflags = {}
for war in dirty_warlist:
    date = str(war.contents[0])
    link = war.contents[1].get('href')
    war_html = urllib2.urlopen(wiki+link)
    soup = BeautifulSoup(war_html)
    if str(soup.html).__contains__('Belligerents'):
        trs = soup.findAll('tr')
        ind = 0
        multi = -1
        war_belligerents = ''
        for tr1 in enumerate(trs):
            tr = tr1[1]
            if tr.th and tr.th.contents and str(tr.th.contents[0]).__eq__('Belligerents'):
                ind = tr1[0]
            if tr.th and tr.th.contents and str(tr.th.contents[0]).__eq__('Commanders and leaders'):
                if tr1[0] != ind + 2:
                    multi = tr1[0]
                    break

        for tr1 in enumerate(trs):
            if multi != -1:
                # Several stages in war with different sides
                war_belligerents = ''.join([str(x) for x in list(enumerate(trs))[ind:multi]])
            else:
                if tr1[0] == ind + 1:
                    war_belligerents = tr1[1]

        # Count sides
        sides = set()
        for side in re.sub(r'<[^>]*>', r'', str(war_belligerents)).split('\n'):
            side_clean = side
            if side_clean.__contains__('['):
                side_clean = side_clean[0:side_clean.index('[')]
            if side_clean.__contains__(';'):
                side_clean = side_clean[side_clean.index(';')+1:len(side_clean)]
            side_clean = side_clean.strip()
            sides.add(side_clean)

        for side_clean in sides:
            if not belligerents.keys().__contains__(side_clean):
                belligerents[side_clean] = 1
            else:
                belligerents[side_clean] += 1

        # Count flags
        flags = set()
        for flag in re.findall(r'Flag_of_([a-zA-Z_]*).svg', str(war_belligerents)):
            flags.add(flag)

        for flag in flags:
            if not sideflags.keys().__contains__(flag):
                sideflags[flag] = 1
            else:
                sideflags[flag] += 1

    print date, str(soup.findAll('title')).replace(' - Wikipedia, the free encyclopedia', '')

country_synonyms = [
            ['France', 'Kingdom of France'],
            ['Russian Empire', 'Tsardom of Russia', 'Russian SFSR', 'Soviet Union'],
            ['Sweden', 'Swedish Empire'],
            ['England', 'United Kingdom', 'British Empire', 'Great Britain', 'British Army', 'Kingdom of England'],
            ['Prussia', 'German Empire', 'Saxony', 'Electorate of Saxony', 'Freikorps', 'Holy Roman Empire'],
            ['Italy', 'Kingdom of Italy', 'Duchy of Savoy',
             'Kingdom of Sardinia', 'Papal States', 'Republic of Venice', 'Naples', 'Kingdom of Naples'],
            ['Hungary', 'Kingdom of Hungary', 'Hungarian Soviet Republic'],
            ['Spain', 'Spanish Empire'],
            ['Austria', 'Archduchy of Austria', 'Austrian Empire', 'Habsburg Monarchy', 'Habsburg Empire'],
            ['Poland', 'Polish–Lithuanian Commonwealth', 'Polish Legions', 'Polish-Lithuanian Commonwealth'],
            ['Dutch Republic', 'Habsburg Netherlands', 'Dutch Republic (1666)', 'United Provinces'],
            ['Denmark', 'Denmark (1666)', 'Denmark-Norway', 'Denmark–Norway']]

for country_names in country_synonyms:
    for name in country_names[1:]:
        belligerents[country_names[0]] += belligerents[name]
        del belligerents[name]

print '# of sides: ', len(belligerents.keys())
print '# of conflicts: ', len(dirty_warlist)

sorted_belligerents = sorted(belligerents.items(), key=operator.itemgetter(1))

for side in sorted_belligerents:
    if int(side[1]) > 1:
        print side[0], ' ', side[1], ' ', float(side[1])/len(dirty_warlist)

print '-'*100

print '# of flags: ', len(sideflags)

sorted_sideflags = sorted(sideflags.items(), key=operator.itemgetter(1))

for flag in sorted_sideflags:
    if int(flag[1]) > 1:
        print flag[0], ' ', flag[1], ' ', float(flag[1])/len(dirty_warlist)