# replace nans with closest non-nan value
def backfill(data):
    data = data.fillna(method='backfill')
    data = data.fillna(method='ffill')
    return data

# replace nans with zero
def cleanWithZeros(data):
    data = data.fillna(0)
    return data
