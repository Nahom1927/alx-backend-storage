#!/usr/bin/env python3
"""Prints statistics from the nginx collection"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs = client.logs.nginx

    print(logs.count_documents({}), 'logs')
    print('Methods:')
    method = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for req in method:
        print(f'\tmethod {req}:', logs.count_documents({'method': req}))
    print(logs.count_documents({'method': 'GET','path': '/status'}), 'status check')


    print('IPs:')
    ip_counts = logs.aggregate(
        [ { "$group" :
                { "_id": "$ip",
                  "count": { "$sum": 1 }
                }
          }, 
          { "$sort": {"count": -1} },
          { "$limit": 10 } ]
    )
    for data in ip_counts:
        print(f"\t{data['_id']}: {data['count']}")
