import pandas as pd

def backfill(data):
    data = data.fillna(method='backfill')
    return data

def cleanWithZeros(data):
    data = data.fillna(0)
    return data
