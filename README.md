# ⚡ EV Charging Station Locator

 A full-stack web application that enables electric vehicle users to locate nearby charging stations in real time — powered by geolocation, distance-based filtering, and secure user authentication.

---

## 📌 Overview

EV adoption in India is growing rapidly, yet locating a compatible, reachable charging station remains a friction point for many drivers. This project addresses that gap by combining real-world geospatial data with a battery-aware distance algorithm — helping users find stations they can actually reach, not just stations that exist nearby.

Built as a full-stack application using **Flask**, **SQLite**, and the **Google Maps API**, it demonstrates end-to-end software development: from database design and RESTful backend logic to an interactive, user-friendly frontend.

---

## 🚀 Key Features

| Feature | Description |
|---------|-------------|
| 📍 Geolocation Detection | Automatically retrieves the user's current coordinates via the browser |
| 🔋 Battery-Aware Filtering | Calculates maximum reachable distance based on entered battery % and vehicle range |
| 🗺️ Interactive Map | Visualises reachable stations on a Google Maps interface with markers |
| 🔐 User Authentication | Secure register/login system with hashed password storage |
| 📊 Dataset Integration | Processes a curated dataset of EV charging stations across India using Pandas |
| 💾 Persistent Storage | SQLite database maintains user credentials across sessions |

---

## 🛠️ Tech Stack

**Frontend** — HTML5, CSS3, JavaScript  
**Backend** — Python, Flask  
**Database** — SQLite  
**Data Processing** — Pandas  
**External APIs** — Google Maps JavaScript API  

---

## 📂 Project Structure

```
EV-Charging-Locator/
│
├── app.py                          # Core Flask application & route handlers
├── database.py                     # Database initialisation & query logic
├── requirements.txt                # Python dependencies
├── india_ev_charging_stations.csv  # EV station dataset (location, type, availability)
├── users.db                        # SQLite user credentials store
│
├── templates/
│   ├── home.html                   # Landing page
│   ├── index.html                  # Main locator interface
│   ├── login.html                  # User login
│   ├── register.html               # User registration
│   └── result.html                 # Station results & map view
│
└── static/
    ├── style.css                   # Global stylesheet
    ├── forecast.png                # UI asset
    └── stations.png                # UI asset
```

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.10+
- A valid [Google Maps API key](https://developers.google.com/maps/documentation/javascript/get-api-key)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/ev-charging-locator.git
cd ev-charging-locator

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the Flask development server
python app.py
```

Then open your browser and navigate to `http://127.0.0.1:5000`

> **Note:** Add your Google Maps API key to the relevant template file before running.

---

## 🧠 How It Works

```
User Logs In
     │
     ▼
Browser Requests Geolocation
     │
     ▼
User Inputs Battery Percentage
     │
     ▼
Backend Calculates Max Reachable Range
     │  (battery % × vehicle range constant)
     ▼
Haversine Formula Filters Dataset
     │  (stations within calculated radius)
     ▼
Results Rendered on Google Maps + Sorted by Distance
```

The core distance logic uses the **Haversine formula** to compute great-circle distance between the user's coordinates and each station in the dataset — ensuring accuracy across geographic coordinates without relying on road-routing APIs.

---

## 📊 Dataset

The application uses `india_ev_charging_stations.csv`, a structured dataset containing station names, geographic coordinates, charger types, and operator information across major Indian cities and highways.

---

## 🔐 Security

- Passwords are stored using cryptographic hashing (not plain text)
- Sessions are managed server-side via Flask's session handling
- Input validation is applied on both client and server sides

---

## 🔭 Roadmap

- [ ] Integrate live charging station APIs (e.g., PlugShare, OCPP-based networks)
- [ ] Add real-time slot availability status
- [ ] Implement route optimisation with turn-by-turn directions
- [ ] Build a mobile-responsive UI / PWA version
- [ ] Add charger type filtering (AC/DC, connector standard)
- [ ] Deploy to cloud (AWS / Render / Railway)

---

👨‍💻 Author

Kaibalya Mohanty 
B.Tech Computer Science Engineering  
. [LinkedIn](www.linkedin.com/in/kaibalya-mohanty) 
· [GitHub](https://github.com/your-username) 

---

## 📄 License

This project was developed for educational purposes as part of my academic portfolio. Feel free to explore the codebase — attribution appreciated if you build on it.