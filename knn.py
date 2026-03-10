import pandas as pd
from sklearn.neighbors import NearestNeighbors

# ==========================
# LOAD DATASET
# ==========================

data = pd.read_csv("india_ev_charging_stations.csv")

# Clean column names
data.columns = data.columns.str.strip()

# Convert coordinates to numbers
data['lattitude'] = pd.to_numeric(data['lattitude'], errors='coerce')
data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')

# Remove invalid rows
data = data.dropna(subset=['lattitude','longitude'])

# ==========================
# FEATURES
# ==========================

X = data[['lattitude','longitude']]

# ==========================
# TRAIN MODEL
# ==========================

knn = NearestNeighbors(n_neighbors=3)

knn.fit(X)

# ==========================
# RECOMMENDATION FUNCTION
# ==========================

def recommend_station(user_lat, user_lon):

    distances, indices = knn.kneighbors([[user_lat, user_lon]])

    stations = []

    for i in indices[0]:
        stations.append({
            "name": data.iloc[i]['name'],
            "lat": data.iloc[i]['lattitude'],
            "lon": data.iloc[i]['longitude']
        })

    return stations
