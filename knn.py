import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

# load dataset
data = pd.read_csv("stations.csv")

# features (latitude and longitude)
X = data[['latitude','longitude']]

# labels (station name)
y = data['name']

# train model
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X,y)

def recommend_station(latitude, longitude):

    prediction = knn.predict([[latitude, longitude]])

    return prediction[0]