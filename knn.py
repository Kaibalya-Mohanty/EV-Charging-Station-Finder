import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

# load dataset
data = pd.read_csv("india_ev_charging_stations.csv")

# remove rows with missing coordinates
data = data.dropna(subset=['lattitude','longitude'])

# features
X = data[['lattitude','longitude']]

# labels
y = data['name']

# train model
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X,y)

def recommend_station(lattitude, longitude):

    prediction = knn.predict([[lattitude, longitude]])

    return prediction[0]
