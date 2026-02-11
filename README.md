
#### Environment setup

- python -m venv myenv

- myenv\scripts\activate

#### install requirements

- pip install -r requirements.txt


#### safe-route-ai/
```
│
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI server entry point
│   │   ├── routes.py               # All API endpoints
│   │   ├── services/
│   │   │   ├── risk_service.py     # ML prediction logic
│   │   │   ├── route_service.py    # Route safety scoring
│   │   │   └── weather_service.py  # Weather API + caching
│   │   │   ├── heatmap_service.py      # Cluster/hotspot logic   
│   │   │   ├── explanation_service.py  # LLM AI summary          
│   │   │   ├── hazard_service.py       # Community report DB 
|   |   |   ├── geocode_service.py  # Convert Location to lat-lan form
|   |   |   
│   │   ├── models/
│   │   │   ├── risk_model.pkl      # Trained ML model
│   │   │   └── cluster_model.pkl   # Hotspot clustering model
│   │   │
│   │   ├── schemas.py              # Request/Response data models
│   │   └── database.py             # DB connection setup
│   │
│   ├── ML/
│   │   ├── preprocessing.py        # Cleaning + feature engineering
│   │   ├── clustering.py           # DBSCAN / KMeans hotspots
│   │   └── train_model.py          # Train & save ML models
│   │       
│   ├── Data/
│   │   ├── raw/accidents.csv       # Original dataset
│   │   └── processed/clean.csv     # Cleaned dataset
│   │
│   ├── DB/
│   │   └── db.sqlite               # Hazard reports + weather cache
│   │
│   ├── utils/
│   │   ├── config.py               # API keys, constants
│   │   └── helpers.py              # Utility functions
│   │
│   └── requirements.txt            # Python dependencies
│
├── frontend/
│   ├── public/
│   │   └── index.html              # Root HTML
│   │
│   └── src/
│       ├── App.jsx                 # Main React component
│       ├── main.jsx                # React entry point
│       │
│       ├── components/
│       │   ├── MapView.jsx         # Heatmap + routes + markers
│       │   ├── RouteForm.jsx       # Start/End inputs
│       │   ├── RiskPanel.jsx       # Risk % + AI explanation
│       │   ├── Charts.jsx          # Time trend graphs
│       │   └── ReportHazard.jsx    # Community reporting form
│       │
│       ├── services/
│       │   └── api.js              # Axios API calls to backend
│       │
│       ├── styles/
│       │   └── main.css            # UI styling
│       │
│       └── utils/
│           └── mapHelpers.js       # Map logic helpers
│
├── README.md
└── docker-compose.yml (optional)
```

