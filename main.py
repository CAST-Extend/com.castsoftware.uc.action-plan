from tkinter.tix import COLUMN
from typing import final
import psycopg2
import csv
import pandas as pd
import numpy as np
import argparse
from sqlite3 import Error, connect
import psycopg2.extras as extras
import pg8000

# File path and name.
fileName = 'ActionPlan_export.csv'


# function to connect to the database.
def connect(Hostname, PortNumber): 
    # connecting to the database called test
    # using the connect function
    try:
        conn=psycopg2.connect(database="postgres", user="operator", password="CastAIP", host=f'{Hostname}', port=f'{PortNumber}')
  
        # creating the cursor object
        cur = conn.cursor()
        print("connected to postgreSQL DB")
      
    except (Exception, psycopg2.DatabaseError) as error: 
        print ("Error while creating PostgreSQL table", error)
    # returing the conn and cur
    # objects to be used later
    return conn, cur


# a function to fetch the data 
#from the database table
def fetch_data(conn,cur, DatabaseName):

    db_full_name=f'{DatabaseName}_central'
    
    #execute our Query 
    cur.execute(f'set search_path={db_full_name}')
    cur.execute("select distinct dmv.metric_id, dmv.snapshot_id, dmv.functional_date, dmr.object_id from dss_metric_values dmv, dss_metric_results dmr where dmv.metric_id = dmr.metric_id order by dmv.metric_id asc") 

    # retrieve the records from the database
    records = cur.fetchall()

    headers = [i[0] for i in cur.description]
    # Open CSV file for writing.
    #store the data in an csv sheet
    csvFile = csv.writer(open(fileName, 'w', newline=''),  #c'est pas rules file
                        delimiter=',', lineterminator='\r\n',
                        quoting=csv.QUOTE_ALL, escapechar='\\')

    # Add the headers and data to the CSV file.
    csvFile.writerow(headers)
    csvFile.writerows(records)

    #delete the content of the viewer_action_plan
    sql=f'Delete from {db_full_name}.viewer_action_plans'
    cur.execute(sql)
    conn.commit()

    # Message stating export successful.
    print("Data export successful.")



# Function That display the dataframe exported from the database
def export_data(rules, output):
         
    #read the results in the excel template sheet which contains all the violation rules 
    df_template = pd.read_excel(rules)#call it rules after 
    #output = pd.read_csv(fileName) # excel which contains the 

    priorities = ['Fix Now', 'Near Term', 'Mid Term', 'Long Term'] 
    severity = [0,1,2,3]#tableau entiers
    tag = ['Extreme', 'High', 'Moderate', 'Low']
    
    for p,s,t in zip(priorities,severity,tag):
        fn = df_template[df_template['Final Priority'] == p]
        ids = fn['metric_id']+1
        ids = fn["metric_id"].values.tolist()
        ids2 = str(ids).replace('[','(').replace(']',')')
        fn1 =fn.drop(columns=['metric_name', 'href', 'Business Criteria','Technical Criteria', 'critical', 'severity', 'technologyNames'])
        fn1.rename(columns={'Final Priority':'priority'}, inplace =True)
        sql = f"insert into viewer_action_plans (metric_id, object_id, first_snapshot_date,last_snapshot_date,user_name,sel_date,priority,action_def,tag) select distinct dmr.metric_id, object_id, dmv.snapshot_date, timestamp '2100-01-01 00:00:00','admin', now(), {s}, '{p}', '{t}' from dss_snapshots dmv, dss_metric_results dmr where dmv.snapshot_id = (select max(snapshot_id) from dss_snapshots) and metric_id in {ids2}"
        cur.execute(sql)
        conn.commit()




#main function to call all the other functions
if __name__ == '__main__':

        parser = argparse.ArgumentParser(description='SQLite DB handler')
        parser.add_argument('-ho', '--host', required=True, help='Database host name')
        parser.add_argument('-p', '--port', required=True, help='Database port number')
        parser.add_argument('-a', '--application', required=True, help='schema triplet name')
        parser.add_argument('-r', '--rules', required=True, help='Rules name, including path')
        parser.add_argument('-o', '--output', required=True, help='')
        args = parser.parse_args()

        conn, cur = connect(args.host, args.port)
        
        fetch_data(conn,cur, args.application)
        export_data(args.rules, args.output)

        cur.close()
        conn.close()

#  py .\main.py -a backline -r C:\Action_Plan\rules.xlsx -o C:\Action_Plan\ActionPlan_export.csv


       

       
