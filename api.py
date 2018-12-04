import datetime as dt
import json
import sys


filename = sys.argv[-1]
from flask import Flask, jsonify, request, json


class UserStatusSearch:

    RECORDS = [
        {'user_id': 1, 'created_at': '2017-01-01T10:00:00', 'status': 'paying'},
        {'user_id': 1, 'created_at': '2017-03-01T19:00:00', 'status': 'paying'},
        {'user_id': 1, 'created_at': '2017-02-01T12:00:00', 'status': 'cancelled'},
        {'user_id': 4, 'created_at': '2017-10-10T10:00:00', 'status': 'cancelled'},
        {'user_id': 3, 'created_at': '2017-10-01T10:00:00', 'status': 'paying'},
        {'user_id': 3, 'created_at': '2016-02-01T05:00:00', 'status': 'cancelled'},
    ]

    def __init__(self):
        pass

    def get_status(self, user_id, date):
        #for every user id return its status
        #RECORDS is a list of elements and not a dictionary (as RANGES)
        for record in self.RECORDS:
            record_user_id=record['user_id']
            record_status=record['status']
            record_date=str(record['created_at'])

            if ((user_id==record_user_id) and (record_date == str(date))):
                print ("date to print", date, record['created_at'])
                return(record_status)
            #else:
            #    print("no user founded")
        return ("non-paying")



class IpRangeSearch:

    RANGES = {
        'london': [
            {'start': '10.10.0.0', 'end': '10.10.255.255'},
            {'start': '192.168.1.0', 'end': '192.168.1.255'},
        ],
        'munich': [
            {'start': '10.12.0.0', 'end': '10.12.255.255'},
            {'start': '172.16.10.0', 'end': '172.16.11.255'},
            {'start': '192.168.2.0', 'end': '192.168.2.255'},
        ]
    }

    def __init__(self):
        pass

    def get_city(self, ip):
        # given an ip address as an output I want a city name -> city name within RANGES.
        # RANGES is a dictionary, so for every key(the name of the city), i will look up for every elemnts (the range address)
        for city_name,range_adr in self.RANGES.items():
            #need another for iteration to acess every value (range address), related to the key ()
            for r in range_adr:
                if (ip>=(r['start']) and ip<=(r['end'])):
                    print("city_name:",city_name)
                    return(city_name)
                #else:
                    #print("city_name:", city_name)
        #in case no city_name was found into the range of addresses
        return ("unknown")


def enrich_json(filename):
    with open(filename) as json_file:
        transactions = json.load(json_file)
        transactions_obj=[]
        for transaction in transactions:
            ip=transaction['ip']
            user_id=transaction['user_id']
            date=transaction['created_at']
            city=ip_range_search.get_city(ip)
            status=user_status_search.get_status(int(user_id), date)
            print (ip, city)
            transaction['city']=(city)
            transaction['status']=(status)
            transactions_obj.append(transaction)
        with open('transactions_out.json', 'w') as outfile:
            json.dump(transactions_obj, outfile,indent=4)

app = Flask(__name__)
user_status_search = UserStatusSearch()
ip_range_search = IpRangeSearch()


@app.route('/user_status/<user_id>')
def user_status(user_id):
    """
    Return user status for a give date

    /user_status/1?date=2017-10-10T10:00:00
    """
    date = dt.datetime.strptime(str(request.args.get('date')), '%Y-%m-%dT%H:%M:%S')

    return jsonify({'user_status': user_status_search.get_status(int(user_id), date)})


@app.route('/ip_city/<ip>')
def ip_city(ip):

    """
    Return city for a given ip
    
    /ip_city/10.0.0.0
    """
    #print (jsonify({'city': ip_range_search.get_city(ip)}))
    return jsonify({'city': ip_range_search.get_city(ip)})

@app.route('/')
def index():
    return ("working page")
 
if __name__ == '__main__':
    #app.run(host='0.0.0.0')
    app.run(debug=True)
   
   

