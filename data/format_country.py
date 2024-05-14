import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")

# Connect to the MySQL database
db = mysql.connector.connect(
    user = DB_USER,
    password = DB_PASSWORD,
    host = DB_HOST,
    database = DB_DATABASE,
)

# Create a cursor object to execute SQL queries
cursor = db.cursor()

# Format the country column. Reduce to iso code
cursor.execute("UPDATE hotels SET country = 'US' WHERE country = 'United-States'")
cursor.execute("UPDATE hotels SET country = 'GB' WHERE country = 'United-Kingdom'")
cursor.execute("UPDATE hotels SET country = 'FR' WHERE country = 'France'")
cursor.execute("UPDATE hotels SET country = 'DE' WHERE country = 'Germany'")
cursor.execute("UPDATE hotels SET country = 'IT' WHERE country = 'Italy'")
cursor.execute("UPDATE hotels SET country = 'ES' WHERE country = 'Spain'")
cursor.execute("UPDATE hotels SET country = 'DK' WHERE country = 'Denmark'")
cursor.execute("UPDATE hotels SET country = 'SE' WHERE country = 'Sweden'")
cursor.execute("UPDATE hotels SET country = 'NO' WHERE country = 'Norway'")
cursor.execute("UPDATE hotels SET country = 'FI' WHERE country = 'Finland'")
cursor.execute("UPDATE hotels SET country = 'DK' WHERE country = 'Faroe-Islands'")
cursor.execute("UPDATE hotels SET country = 'DK' WHERE country = 'FO'")
cursor.execute("UPDATE hotels SET country = 'IS' WHERE country = 'Iceland'")
cursor.execute("UPDATE hotels SET country = 'IE' WHERE country = 'Ireland'")
cursor.execute("UPDATE hotels SET country = 'NL' WHERE country = 'Netherlands'")
cursor.execute("UPDATE hotels SET country = 'BE' WHERE country = 'Belgium'")
cursor.execute("UPDATE hotels SET country = 'CH' WHERE country = 'Switzerland'")
cursor.execute("UPDATE hotels SET country = 'TR' WHERE country = 'Turkiye'")
cursor.execute("UPDATE hotels SET country = 'GR' WHERE country = 'Greece'")
cursor.execute("UPDATE hotels SET country = 'PT' WHERE country = 'Portugal'")
cursor.execute("UPDATE hotels SET country = 'CZ' WHERE country = 'Czech-Republic'")
cursor.execute("UPDATE hotels SET country = 'PL' WHERE country = 'Poland'")
cursor.execute("UPDATE hotels SET country = 'MC' WHERE country = 'Monaco'")
cursor.execute("UPDATE hotels SET country = 'MX' WHERE country = 'Mexico'")
cursor.execute("UPDATE hotels SET country = 'AT' WHERE country = 'Austria'")
cursor.execute("UPDATE hotels SET country = 'AU' WHERE country = 'Australia'")
cursor.execute("UPDATE hotels SET country = 'TH' WHERE country = 'Thailand'")
cursor.execute("UPDATE hotels SET country = 'JP' WHERE country = 'Japan'")
cursor.execute("UPDATE hotels SET country = 'IN' WHERE country = 'India'")
cursor.execute("UPDATE hotels SET country = 'DK' WHERE country = 'Greenland'")
cursor.execute("UPDATE hotels SET country = 'DK' WHERE country = 'GL'")
cursor.execute("UPDATE hotels SET country = 'MT' WHERE country = 'Malta'")
cursor.execute("UPDATE hotels SET country = 'HU' WHERE country = 'Hungary'")
cursor.execute("UPDATE hotels SET country = 'LT' WHERE country = 'Lithuania'")
cursor.execute("UPDATE hotels SET country = 'BR' WHERE country = 'Brazil'")

# Commit the changes
db.commit()

db.close()



