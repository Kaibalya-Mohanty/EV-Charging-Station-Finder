import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

# load dataset
data = pd.read_csv("india_ev_charging_stations.csv")

# features (latitude and longitude)
X = data[['lattitude','longitude']]

# labels (station name)
y = data['name']

# train model
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X,y)

def recommend_station(lattitude, longitude):

    prediction = knn.predict([[lattitude, longitude]])

    return prediction[0]
