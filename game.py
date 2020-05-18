import requests
import json
import time
from pymongo import MongoClient


def create_data(num=1, startweek=1, endweek=1, year=2019):
    data = {
        'sort': 'FantasyPoints-desc',
        'pageSize': str(num),
        'group': '',
        'filter': '',
        'filters.position': '',
        'filters.team': '',
        'teamkey': '',
        'filters.season': str(year),
        'filters.seasontype': '1',
        'filters.scope': '2',
        'filters.subscope': '1',
        'filters.redzonescope': '',
        'filters.scoringsystem': '1',
        'filters.leaguetype': '',
        'filters.searchtext': '',
        'filters.week': '',
        'filters.startweek': str(startweek),
        'filters.endweek': str(endweek),
        'filters.minimumsnaps': '',
        'filters.teamaspect': '',
        'filters.stattype': '',
        'filters.exportType': '',
        'filters.desktop': '',
        'filters.dfsoperator': '',
        'filters.dfsslateid': '',
        'filters.dfsslategameid': '',
        'filters.dfsrosterslot': '',
        'filters.page': '',
        'filters.showfavs': '',
        'filters.posgroup': '',
        'filters.oddsstate': '',
        'filters.showall': '',
        'filters.aggregatescope': '1',
        'filters.rangescope': '',
        'filters.range': '3'
    }
    return data


url = 'https://fantasydata.com'
endpoint = '/FantasyStatsNFL/FantasyStats_Read'
years = [2019, 2018, 2017, 2016]

# MongoDB
client = MongoClient()
db = client.fantasydata
collection = db.game

for year in years:
    # 17 weeks of data
    for week in range(1, 18):
        # one request to get total
        temp_data = create_data(num=1, startweek=week, endweek=week, year=year)
        temp_response = requests.post(url + endpoint, data=temp_data)

        total = json.loads(temp_response.text)["Total"]

        # second request to get all the data
        data = create_data(num=total, startweek=week, endweek=week, year=year)
        response = requests.post(url + endpoint, data=data)

        # insert records
        collection.insert_many(json.loads(response.text)["Data"])

        # no spamming servers
        time.sleep(5)

client.close()
