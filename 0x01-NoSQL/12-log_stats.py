#!/usr/bin/env python3
"""MongoDB storage"""
import pandas as pd

df = pd.read_csv('access.log', sep=' ', header=None,
                 names=['ip', 'dash1', 'dash2', 'time', 'request', 'status', 'size', 'referer', 'user_agent', 'forwarded_for'])
df['time'] = df['time'].str.replace('[','').str.replace(']','')
df['time'] = pd.to_datetime(df['time'], format='%d/%b/%Y:%H:%M:%S %z')
df['method'] = df['request'].str.split().str[0]
df['path'] = df['request'].str.split().str[1]
print(f"{len(df)} logs where {len(df[df.method == 'GET'])} are GET, {len(df[df.method == 'POST'])} are POST, {len(df[df.method == 'PUT'])} are PUT, {len(df[df.method == 'PATCH'])} are PATCH, and {len(df[df.method == 'DELETE'])} are DELETE")
print(f"{len(df[(df.method == 'GET') & (df.path == '/status')])} logs where method=GET path=/status")
