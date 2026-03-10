import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

data = pd.read_csv("india_ev_charging_stations.csv")

# FIX BAD DATA
data['lattitude'] = pd.to_numeric(data['lattitude'], errors='coerce')
data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')

# remove invalid rows
data = data.dropna()

# features
X = data[['lattitude','longitude']]

# labels
y = data['name']

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y)

def recommend_station(lat, lon):
    prediction = knn.predict([[lat, lon]])
    return prediction[0]
