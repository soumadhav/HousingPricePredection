import streamlit as st
from pymongo import MongoClient
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import certifi
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

# MongoDB Atlas connection details
MONGO_URI = "mongodb+srv://housing:housing_password@soumyamongo1.8eq0f.mongodb.net/?retryWrites=true&w=majority&appName=soumyaMongo1"
MONGO_DB_NAME = "housing_db"
MONGO_COLLECTION = "property_sales"

# PostgreSQL NEON connection details
POSTGRES_URI = "postgresql://housing_price_owner:RG5v9BhNSfZA@ep-curly-pond-a23y7nfa.eu-central-1.aws.neon.tech/housing_price?sslmode=require"
POSTGRES_TABLE = "housing_price"


# MongoDB Client
@st.cache_resource
def get_mongo_client():
    return MongoClient(MONGO_URI, tlsCAFile=certifi.where())

# PostgreSQL Engine
@st.cache_resource
def get_postgres_engine():
    return create_engine(POSTGRES_URI)

# Load data from MongoDB
@st.cache_data
def load_mongo_data():
    client = get_mongo_client()
    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION]
    data = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB ID
    return pd.DataFrame(data)

# Load data from PostgreSQL
@st.cache_data
def load_postgres_data():
    engine = get_postgres_engine()
    query = f"SELECT * FROM {POSTGRES_TABLE}"
    return pd.read_sql(query, engine)

# Fetch database characteristics
def get_db_characteristics(df):
    return {
        "Number of Rows": len(df),
        "Number of Columns": len(df.columns),
        "Columns": ", ".join(df.columns),
    }

# App layout
st.title("Housing Data Visualization - Melbourne")

# Database selection
db_choice = st.radio("Select Database:", ["MongoDB (Raw Data)", "PostgreSQL (Cleaned Data)"])

if db_choice == "MongoDB (Raw Data)":
    data = load_mongo_data()
    db_details = get_db_characteristics(data)
    query_shown = "MongoDB query: All documents fetched from the collection."
    price_column = "Price"
else:
    data = load_postgres_data()
    db_details = get_db_characteristics(data)
    query_shown = f"PostgreSQL query: SELECT * FROM {POSTGRES_TABLE}"
    price_column = "Price_log"

# Display database characteristics as cards
st.subheader("Database Details")
cols = st.columns(3)
cols[0].metric("Rows", db_details["Number of Rows"])
cols[1].metric("Columns", db_details["Number of Columns"])
cols[2].write(f"Columns: {db_details['Columns']}")

# Display the query
st.code(query_shown, language="sql")

# Convert relevant columns to numeric for visualization
data["Lattitude"] = pd.to_numeric(data["Lattitude"], errors="coerce")
data["Longtitude"] = pd.to_numeric(data["Longtitude"], errors="coerce")
data[price_column] = pd.to_numeric(data[price_column], errors="coerce")

# Filters
st.sidebar.header("Filters")
suburb_filter = st.sidebar.multiselect("Select Suburb", options=data["Suburb"].unique())
price_range = st.sidebar.slider(
    f"Select {price_column} Range",
    int(data[price_column].min()) if not data[price_column].isna().all() else 0,
    int(data[price_column].max()) if not data[price_column].isna().all() else 1,
    (0, int(data[price_column].max()) if not data[price_column].isna().all() else 1),
)

filtered_data = data[
    (data["Suburb"].isin(suburb_filter) if suburb_filter else True) &
    (data[price_column].between(*price_range) if not data[price_column].isna().all() else True)
]

# Display filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_data)

# Map Visualization
st.subheader("Heat Map")
m = folium.Map(location=[-37.81, 144.96], zoom_start=12)

if not filtered_data.empty:
    heat_data = filtered_data[["Lattitude", "Longtitude", price_column]].dropna()
    heat_data = heat_data.values.tolist()
    HeatMap(heat_data, radius=15).add_to(m)

st_folium(m, width=700, height=500)
