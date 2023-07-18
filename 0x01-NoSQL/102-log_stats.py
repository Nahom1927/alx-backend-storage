#!/usr/bin/env python3
"""Improved log stats module"""
from pymongo import MongoClient

client = MongoClient()
db = client.logs_database
collection = db.nginx

total_logs = collection.count_documents({})
print(f"{total_logs} logs")

methods = collection.aggregate([
    {"$group": {"_id": "$method", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
])

print("Methods:")
for method in methods:
    print(f"    method {method['_id']}: {method['count']}")

status_checks = collection.find({"status_code": "404"}).count()
print(f"{status_checks} status check")

ips = collection.aggregate([
    {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
])

print("IPs:")
for ip in ips:
    print(f"    {ip['_id']}: {ip['count']}")
