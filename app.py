from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from knn_clustering import EVStationClusterer
from knn import recommend_station

import pandas as pd
import json
import math
import os
import sqlite3
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from werkzeug.security import generate_password_hash, check_password_hash
import requests as http_requests

app = Flask(__name__)
app.config['SECRET_KEY'] = "ev_charge_finder_secret_key_2026"

DATABASE = "users.db"
df = None
ml_model = None
clusterer = None


# ==============================
# DATABASE
# ==============================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


init_db()


# ==============================
# LOAD DATA
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(BASE_DIR, "india_ev_charging_stations.csv")

if os.path.exists(csv_file):

    df = pd.read_csv(csv_file)
    df.columns = df.columns.str.strip()

    df['lattitude'] = (
        df['lattitude']
        .astype(str)
        .str.replace(',', '')
        .astype(float)
    )

    df['longitude'] = (
        df['longitude']
        .astype(str)
        .str.replace(',', '')
        .astype(float)
    )

    df = df.drop_duplicates(subset=['name','lattitude','longitude'])

    print(f"Loaded {len(df)} stations")

else:
    df = pd.DataFrame()
    print("CSV NOT FOUND")


# ==============================
# ML DEMAND MODEL
# ==============================

def train_demand_model():

    global ml_model

    if df.empty:
        return

    X = df[['lattitude','longitude']].values
    y = np.random.randint(20,200,len(df))

    ml_model = RandomForestRegressor(n_estimators=50)
    ml_model.fit(X,y)

    print("Demand model ready")


train_demand_model()


def predict_station_demand(lat,lon):

    if ml_model is None:
        return 0

    try:
        return int(ml_model.predict([[lat,lon]])[0])
    except:
        return 0


# ==============================
# CLUSTERING MODEL
# ==============================

def init_clusterer():

    global clusterer

    if not df.empty:
        clusterer = EVStationClusterer(df)
        clusterer.fit(n_clusters=15,n_neighbors=5)

        print("Clusterer ready")


init_clusterer()


# ==============================
# DISTANCE
# ==============================

def calculate_distance(lat1, lon1, lat2, lon2):

    R = 6371

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)

    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1))*
         math.cos(math.radians(lat2))*
         math.sin(dlon/2)**2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R*c


# ==============================
# LANDING
# ==============================

@app.route('/')
def landing():
    return render_template("home.html")


# ==============================
# REGISTER
# ==============================

@app.route('/register',methods=['GET','POST'])
def register():

    if request.method=='POST':

        username=request.form['username']
        email=request.form['email']
        password=generate_password_hash(request.form['password'])

        try:

            conn=get_db_connection()

            conn.execute(
                "INSERT INTO users (username,email,password) VALUES (?,?,?)",
                (username,email,password)
            )

            conn.commit()
            conn.close()

            flash("Account created successfully")

            return redirect(url_for('login'))

        except sqlite3.IntegrityError:

            flash("User already exists")

    return render_template("register.html")


# ==============================
# LOGIN
# ==============================

@app.route('/login',methods=['GET','POST'])
def login():

    if request.method=='POST':

        username=request.form['username']
        password=request.form['password']

        conn=get_db_connection()

        user=conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user['password'],password):

            session['user_id']=user['id']
            session['username']=user['username']

            return redirect(url_for('dashboard'))

        flash("Invalid login")

    return render_template("login.html")


# ==============================
# LOGOUT
# ==============================

@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('landing'))


# ==============================
# DASHBOARD
# ==============================

@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template("index.html",username=session['username'])


# ==============================
# AI RECOMMEND API
# ==============================

@app.route('/recommend')
def recommend():

    try:

        lat=float(request.args.get("lat"))
        lon=float(request.args.get("lon"))

        result=recommend_station(lat,lon)

        return jsonify(result)

    except:
        return jsonify({"error":"invalid coordinates"})


# ==============================
# RESULT PAGE
# ==============================

@app.route('/result',methods=['POST'])
def result():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_lat = float(request.form.get("lat"))
    user_lon = float(request.form.get("lon"))
    battery=float(request.form.get('battery_percent',50))

    safe_battery=max(0,battery-5)
    max_range=safe_battery*2.5

    nearby_stations=[]
   
    for _,row in df.iterrows():

        try:

            s_lat=float(row['lattitude'])
            s_lon=float(row['longitude'])

            dist=calculate_distance(user_lat,user_lon,s_lat,s_lon)

            if dist<=max_range:

                demand=predict_station_demand(s_lat,s_lon)

                nearby_stations.append({

                    "name":row.get("name","N/A"),
                    "lat":s_lat,
                    "lon":s_lon,
                    "distance":round(dist,2),
                    "demand_score":demand,
                    "address":row.get("address",""),
                    "city":row.get("city",""),
                    "state":row.get("state","")

                })

        except:
            continue
    if len(nearby_stations) == 0:
        nearby_stations = []

        for _, row in df.head(50).iterrows():
            nearby_stations.append({
                "name": row.get("name", "EV Station"),
                "lat": float(row.get("lat") or row.get("latitude") or row.get("Latitude") or 0),
                "lon": float(row.get("lon") or row.get("longitude") or row.get("Longitude") or 0),
                "distance": 0,
                "demand_score": 50,
                "cluster_color": "#10b981",
                "cluster_id": -1,
                "address": row.get("address", ""),
                "city": row.get("city", ""),
                "state": row.get("state", "")
            })
    else:
        nearby_stations.sort(key=lambda x:(x.get('distance',0),-x.get('demand_score',0))


    # =========================
    # AI RECOMMENDATIONS
    # =========================

    try:
        ai_stations=recommend_station(user_lat,user_lon)
    except:
        ai_stations=[]


    # =========================
    # CLUSTER INFO
    # =========================

    if clusterer:

        knn_results=clusterer.find_nearest(user_lat,user_lon,k=10)

        knn_lookup={(r['lat'],r['lon']):r for r in knn_results}

        for s in nearby_stations:

            key=(s['lat'],s['lon'])

            if key in knn_lookup:

                s["cluster_id"]=knn_lookup[key]["cluster_id"]
                s["cluster_color"]=knn_lookup[key]["cluster_color"]


    nearby_stations.sort(key=lambda x:(x['distance'],-x['demand_score']))


    return render_template(

        "result.html",

        stations=nearby_stations,
        stations_json=json.dumps(nearby_stations),

        ai_stations=ai_stations,

        battery=int(battery),
        max_range=round(max_range,1),

        username=session['username'],

        u_lat=user_lat,
        u_lon=user_lon
    )


# ==============================
# ROUTE PLANNER
# ==============================

@app.route('/plan_route',methods=['POST'])
def plan_route():

    start=request.form.get("start")
    end=request.form.get("end")

    stations=[]

    for _,row in df.head(10).iterrows():

        stations.append({

            "name":row.get("name","EV"),
            "lat":float(row["lattitude"]),
            "lon":float(row["longitude"])

        })

    return jsonify({

        "start":start,
        "end":end,
        "stations":stations

    })


# ==============================
# AUTOCOMPLETE
# ==============================

OPENCAGE_API_KEY="YOUR_API_KEY"


@app.route('/autocomplete')
def autocomplete():

    query=request.args.get('q','')

    if len(query)<2:
        return jsonify([])

    resp=http_requests.get(

        "https://api.opencagedata.com/geocode/v1/json",

        params={
            "q":query,
            "key":OPENCAGE_API_KEY,
            "limit":6,
            "countrycode":"in"
        }
    )

    data=resp.json()

    results=[]

    for item in data.get("results",[]):

        results.append({

            "display_name":item["formatted"],
            "lat":item["geometry"]["lat"],
            "lon":item["geometry"]["lng"]

        })

    return jsonify(results)


# ==============================
# RUN APP
# ==============================

if __name__=="__main__":

    app.run(host="0.0.0.0",port=10000,debug=True)
