import requests
import json
import time
from pymongo import MongoClient


def create_data(num=1, year=2019):
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
        'filters.scope': '1',
        'filters.subscope': '1',
        'filters.redzonescope': '',
        'filters.scoringsystem': '1',
        'filters.leaguetype': '',
        'filters.searchtext': '',
        'filters.week': '',
        'filters.startweek': '1',
        'filters.endweek': '1',
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
        'filters.aggregatescope': '2',
        'filters.rangescope': '',
        'filters.range': '8'
    }
    return data


url = 'https://fantasydata.com'
endpoint = '/FantasyStatsNFL/FantasyStats_Read'
years = [2019, 2018, 2017, 2016]

# MongoDB
client = MongoClient()
db = client.fantasydata
collection = db.season

for year in years:
    # one request to get total
    temp_data = create_data(num=1, year=year)
    temp_res = requests.post(url + endpoint, data=temp_data)

    total = json.loads(temp_res.text)["Total"]

    # second request to get all the data
    data = create_data(num=total, year=year)
    res = requests.post(url + endpoint, data=data)

    # insert records
    collection.insert_many(json.loads(res.text)["Data"])

    # no spamming servers
    time.sleep(5)

client.close()
