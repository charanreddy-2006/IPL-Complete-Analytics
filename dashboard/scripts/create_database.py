import pandas as pd
import sqlite3
import os


# Dataset path

file = "../data/processed/ipl_cleaned.csv"


# Database path

db_folder = "../data/database"

os.makedirs(
    db_folder,
    exist_ok=True
)


db_path = (
    db_folder +
    "/ipl.db"
)



# Load CSV

df = pd.read_csv(
    file,
    low_memory=False
)



# Clean columns

df.columns = (

    df.columns
    .str.lower()
    .str.strip()

)



# Create connection

connection = sqlite3.connect(
    db_path
)



# Save table

df.to_sql(

    "matches",

    connection,

    if_exists="replace",

    index=False

)



connection.close()



print(
    "IPL Database Created Successfully"
)