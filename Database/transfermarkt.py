#!/usr/bin/python3

import requests
import json
import csv
import os
from bs4 import BeautifulSoup
from os.path import basename

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

def removeOldFiles():

    print('removeOldFiles()')
    os.system('rm players.json')
    print('Old files removed!')

def get_Liga_Portugal():

    print('get_Liga_Portugal()')
    print('Getting Liga Portugal players from transfermarkt.pt')

    league_url = 'https://www.transfermarkt.pt/liga-nos/startseite/wettbewerb/PO1'
    tree = requests.get(league_url, headers=headers, cookies={'__hs_opt_out': 'no'})
    soup = BeautifulSoup(tree.content, 'html.parser')
    table = soup.find('table', {'class':'items'})
    
    team_urls = []
    for row in table.tbody.find_all('tr'):
        cells = row.find_all('td')
        a = cells[2].find_all('a', href=True)
        team_url = 'https://www.transfermarkt.pt' + a[0]['href']
        team_urls.append(team_url)

    return team_urls

def get_Premier_League():

    print('get_Premier_League()')
    print('Getting Premier League players from transfermarkt.pt')

    league_url = 'https://www.transfermarkt.pt/premier-league/startseite/wettbewerb/GB1'
    tree = requests.get(league_url, headers=headers, cookies={'__hs_opt_out': 'no'})
    soup = BeautifulSoup(tree.content, 'html.parser')
    table = soup.find('table', {'class':'items'})
    
    team_urls = []
    for row in table.tbody.find_all('tr'):
        cells = row.find_all('td')
        a = cells[2].find_all('a', href=True)
        team_url = 'https://www.transfermarkt.pt' + a[0]['href']
        team_urls.append(team_url)

    return team_urls

def get_LaLiga():

    print('get_LaLiga()')
    print('Getting LaLiga players from transfermarkt.pt')

    league_url = 'https://www.transfermarkt.pt/laliga/startseite/wettbewerb/ES1'
    tree = requests.get(league_url, headers=headers, cookies={'__hs_opt_out': 'no'})
    soup = BeautifulSoup(tree.content, 'html.parser')
    table = soup.find('table', {'class':'items'})
    
    team_urls = []
    for row in table.tbody.find_all('tr'):
        cells = row.find_all('td')
        a = cells[2].find_all('a', href=True)
        team_url = 'https://www.transfermarkt.pt' + a[0]['href']
        team_urls.append(team_url)

    return team_urls

def get_players(team_urls):

    print('get_players()')

    # To test only with SL Benfica
    # team_urls = [team_urls[0]]

    players = []

    for url in team_urls:
        tree = requests.get(url, headers=headers, cookies={'__hs_opt_out': 'no'})
        soup = BeautifulSoup(tree.content, 'html.parser')
        table = soup.find('table', {'class':'items'})

        for row in table.tbody.find_all('table', {'class':'inline-table'}):
            cell = row.find('td', {'class':'hauptlink'})
            a = cell.find_all('a', href=True)
            name = a[0].text.strip()
            player_url = 'https://transfermarkt.pt' + a[0]['href']
            id = player_url.split("/")[-1]
            player = {}
            player['id'] = id
            player['name'] = name
            player['url'] = player_url
            players.append(player)

    return players

def edit_urls(players):

    print('edit_urls()')

    for player in players:
        new_url = player['url'].replace("profil", "rueckennummern")
        player['url'] = new_url

    return players

def get_player_history(player):

    print('get_player_history(' + player['name'] + ')')

    tree = requests.get(player['url'], headers=headers, cookies={'__hs_opt_out': 'no'})
    soup = BeautifulSoup(tree.content, 'html.parser')
    table = soup.find('table', {'class':'items'})

    for row in table.tbody.find_all('tr'):
        cells = row.find_all('a', href=True)
        url = cells[0]['href'].split('/')
        if url[6] not in player:
            player[url[6]] = url[4]

    return player

def build_csv(database):

    print('build_csv()')

    keys = set().union(*(d.keys() for d in database))

    with open('transfermarkt.csv', 'a', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(database)
    
def main():

    print('transfermarkt()')
    # removeOldFiles()
    team_urls = []
    #team_urls.extend(get_Liga_Portugal())
    #team_urls.extend(get_Premier_League())
    team_urls.extend(get_LaLiga())

    print('How many teams?', len(team_urls), 'teams parsed!')

    players = get_players(team_urls)
    players = edit_urls(players)

    print('How many players?', len(players), 'players parsed!')

    database = []
    for player in players:
        database.append(get_player_history(player))

    build_csv(database)

    # players = buildDatabase(playerDictionary)
    # for i, k in players.items():
        # print(i, k)

if __name__ == '__main__':
    main()