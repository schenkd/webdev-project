# ~*~ encoding: utf-8 ~*~
from pymongo import MongoClient
from pandas import read_csv
from os import getcwd, environ
from datetime import date


mongodb = MongoClient(environ.get('mongo_ip', 'localhost'), 27017)
db = mongodb['dev']
drug_collection = db['drug']

drugs = read_csv(getcwd() + '/data_import/bfarm_lieferenpass_meldung.csv', delimiter=';', encoding='iso8859_2').to_dict()

# Entfernen nicht benoetigter Spalten
drugs.pop('Id', None)
drugs.pop('aktuelle Bescheidart', None)
drugs.pop('Meldungsart', None)
drugs.pop('aktuelle Bescheidart', None)

data = dict()
for x in range(drugs['Verkehrsfähig'].__len__()):
    """
    if drugs['Ende Engpass'][x] == '-':
        data['end'] = None
    else:
        day, month, year = drugs['Ende Engpass'][x].split('.')
        data['end'] = date(int(year), int(month), int(day)).__str__()

    if drugs['Beginn Engpass'][x] == '-':
        data['initial_report'] = None
    else:
        day, month, year = drugs['Beginn Engpass'][x].split('.')
        data['initial_report'] = date(int(year), int(month), int(day)).__str__()

    if drugs['Datum der letzten Meldung'][x] == '-':
        data['last_report'] = None
    else:
        day, month, year = drugs['Datum der letzten Meldung'][x].split('.')
        data['last_report'] = date(int(year), int(month), int(day)).__str__()
    """

    data['substance'] = drugs['Wirkstoffe'][x].replace(' ', '').split(';')

    data['enr'] = int(drugs['Enr'][x])

    data['marketability'] = True if drugs['Verkehrsfähig'][x] == 'ja' else False

    data['atc_code'] = drugs['ATC-Code'][x]

    data['pzn'] = int(drugs['PZN'][x].split(' ')[0].replace(';', '')) if drugs['PZN'][x] != '-' else None

    data['drug_title'] = drugs['Arzneimittelbezeichnung'][x]

    data['hospital'] = True if drugs['Krankenhausrelevant'][x] == 'ja' else False

    drug_collection.update_one({'enr': data['enr']}, {'$set': data}, upsert=True)
