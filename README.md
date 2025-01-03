## 1. Dataset details
### Melbourne Housing dataset - Kaggle
URL - https://storage.googleapis.com/kaggle-data-sets/423/3430/compressed/Melbourne_housing_extra_data-18-08-2017.csv.zip

### Steps to get JSON
1. Download the latest CSV file, 
2. run CSV_to_JSON_Converter.py

## 2. Steps to upload raw data to MongoDB
1. Install MongoDB / create account on mongo atlas, get connection string. (I have used Atlas)
2. Install Python and required libraries
    pip install pymongo streamlit pandas geopandas folium streamlit-folium certifi
3. Run upload_to_monngo.py

## 3. Steps to run the EDA 
1. Install dependencines
      pip install numpy pandas seaborn matplotlib datetime sqlalchemy psycopg2-binary sklearn
2. jupyter notebook EDA_HousingData.ipynb

Note:- the cleaned data is uploaded to Postgresql in this step, hence the postgresql connection URL needs to be configured. 
I have used Neon hosted postgresql for this project, this can also be modified to a local version by changing the connection string.


## Running data explore application
1. Install dependencies
    pip install streamlit pymongo certifi psycopg2-binary sqlalchemy pandas folium streamlit-folium
2. python -m streamlit run app.py
3. Use the features on the app to browse the data and filter.
4. You can select the raw MongoDB/ Cleaned postgreSql DB to explore.


