import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

data = pd.read_csv("india_ev_charging_stations.csv")

# Clean coordinate columns
data['lattitude'] = data['lattitude'].astype(str).str.replace(',', '').astype(float)
data['longitude'] = data['longitude'].astype(str).str.replace(',', '').astype(float)

# Remove rows with missing values
data = data.dropna(subset=['lattitude', 'longitude'])

X = data[['lattitude', 'longitude']]
y = data['name']

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y)

def recommend_station(lattitude, longitude):
    prediction = knn.predict([[lattitude, longitude]])
    return prediction[0]
