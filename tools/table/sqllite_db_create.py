'''
input: string
output: database
'''
import csv
import jsonlines
import pandas as pd
import numpy as np
import json
import os
import re
import sqlite3

def remove_emoji(string):
    # Remove emoji using regex (demoji not used for SQLite version)
    cleaned_string = re.sub(r'[\U00010000-\U0010FFFF]', '', string)
    return cleaned_string

def flights_db_loader():
    file_path = "/Users/joshua.noble/projects/ToolQA/data/external_corpus/flights/Combined_Flights_2022.csv"
    data = pd.read_csv(file_path)
    data = data.fillna("---")
    
    db_path = "flights.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    org_columns = ['FlightDate', 'Airline', 'Origin', 'Dest', 'Cancelled', 'Diverted',
       'CRSDepTime', 'DepTime', 'DepDelayMinutes', 'DepDelay', 'ArrTime',
       'ArrDelayMinutes', 'AirTime', 'CRSElapsedTime', 'ActualElapsedTime',
       'Distance', 'Year', 'Quarter', 'Month', 'DayofMonth', 'DayOfWeek',
       'Marketing_Airline_Network', 'Operated_or_Branded_Code_Share_Partners',
       'DOT_ID_Marketing_Airline', 'IATA_Code_Marketing_Airline',
       'Flight_Number_Marketing_Airline', 'Operating_Airline',
       'DOT_ID_Operating_Airline', 'IATA_Code_Operating_Airline',
       'Tail_Number', 'Flight_Number_Operating_Airline', 'OriginAirportID',
       'OriginAirportSeqID', 'OriginCityMarketID', 'OriginCityName',
       'OriginState', 'OriginStateFips', 'OriginStateName', 'OriginWac',
       'DestAirportID', 'DestAirportSeqID', 'DestCityMarketID', 'DestCityName',
       'DestState', 'DestStateFips', 'DestStateName', 'DestWac', 'DepDel15',
       'DepartureDelayGroups', 'DepTimeBlk', 'TaxiOut', 'WheelsOff',
       'WheelsOn', 'TaxiIn', 'CRSArrTime', 'ArrDelay', 'ArrDel15',
       'ArrivalDelayGroups', 'ArrTimeBlk', 'DistanceGroup',
       'DivAirportLandings']
    columns = [f'"{col}" TEXT' for col in org_columns]
    columns = ','.join(columns)
    cursor.execute(f"DROP TABLE IF EXISTS flights_data;")
    sql_cmd = f"CREATE TABLE flights_data({columns})"
    cursor.execute(sql_cmd)
    for _, row in data.iterrows():
        row_data = [str(row[i]) for i in org_columns]
        placeholders = ','.join(['?']*len(row_data))
        sql = f"INSERT INTO flights_data VALUES ({placeholders})"
        cursor.execute(sql, tuple(row_data))
    conn.commit()
    conn.close()

def coffee_db_loader():
    file_path = "/Users/joshua.noble/projects/ToolQA/data/external_corpus/coffee/coffee_price.csv"
    data = pd.read_csv(file_path)
    column_names = data.columns.to_list()
    data = data.fillna("---")
    db_path = "coffee.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    org_columns = column_names
    columns = [f'"{col}" TEXT' for col in org_columns]
    columns = ','.join(columns)
    cursor.execute(f"DROP TABLE IF EXISTS coffee_data;")
    sql_cmd = f"CREATE TABLE coffee_data({columns})"
    cursor.execute(sql_cmd)
    for _, row in data.iterrows():
        row_data = [str(row[i]) for i in org_columns]
        placeholders = ','.join(['?']*len(row_data))
        sql = f"INSERT INTO coffee_data VALUES ({placeholders})"
        cursor.execute(sql, tuple(row_data))
    conn.commit()
    conn.close()

def airbnb_db_loader():
    file_path = "/Users/joshua.noble/projects/ToolQA/data/external_corpus/airbnb/Airbnb_Open_Data.csv"
    data = pd.read_csv(file_path)
    column_names = data.columns.to_list()
    data = data.fillna("---")
    db_path = "airbnb.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    org_columns = [i.replace(" ","_").replace("lat", "latitude").replace("long", "longitude") for i in column_names]
    columns = [f'"{col}" TEXT' for col in org_columns]
    columns = ', '.join(columns)
    cursor.execute(f"DROP TABLE IF EXISTS airbnb_data;")
    sql_cmd = f"CREATE TABLE airbnb_data({columns})"
    cursor.execute(sql_cmd)
    for _, row in data.iterrows():
        row_data = [remove_emoji(str(row[column_names[j]]))[:250] for j in range(len(org_columns))]
        placeholders = ','.join(['?']*len(row_data))
        sql = f"INSERT INTO airbnb_data VALUES ({placeholders})"
        cursor.execute(sql, tuple(row_data))
    conn.commit()
    conn.close()

def yelp_db_loader():
    data_file = open("/Users/joshua.noble/projects/ToolQA/data/external_corpus/yelp/yelp_academic_dataset_business.json")
    data = []
    for line in data_file:
        data.append(json.loads(line))
    data = pd.DataFrame(data)
    column_names = data.columns.to_list()
    data = data.fillna("---")
    db_path = "yelp.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    org_columns = column_names
    columns = [f'"{col}" TEXT' for col in org_columns]
    columns = ','.join(columns)
    cursor.execute(f"DROP TABLE IF EXISTS yelp_data;")
    sql_cmd = f"CREATE TABLE yelp_data({columns})"
    cursor.execute(sql_cmd)
    for _, row in data.iterrows():
        row_data = [str(row[i])[:250] for i in org_columns]
        placeholders = ','.join(['?']*len(row_data))
        sql = f"INSERT INTO yelp_data VALUES ({placeholders})"
        cursor.execute(sql, tuple(row_data))
    conn.commit()
    conn.close()

def main():
    flights_db_loader()
    coffee_db_loader()
    airbnb_db_loader()
    yelp_db_loader()

if __name__ == "__main__":
    main()
