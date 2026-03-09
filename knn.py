import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

# Load dataset
data = pd.read_csv("india_ev_charging_stations.csv")

# Clean coordinate columns (remove commas and convert to float)
data['lattitude'] = data['lattitude'].astype(str).str.replace(',', '').astype(float)
data['longitude'] = data['longitude'].astype(str).str.replace(',', '').astype(float)

# Remove rows with missing coordinates
data = data.dropna(subset=['lattitude', 'longitude'])

# Features and labels
X = data[['lattitude', 'longitude']]
y = data['name']

# Train KNN model
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y)

def recommend_station(lattitude, longitude):
    """
    Returns nearest EV charging station
    """
    prediction = knn.predict([[lattitude, longitude]])
    return prediction[0]
