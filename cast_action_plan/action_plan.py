import psycopg2
import pandas as pd
from psycopg2 import connect
from cast_action_plan.config import Config
from cast_common.logger import Logger,INFO
from os.path import exists,abspath
from sys import path
from site import getsitepackages

__author__ = ["Nevin Kaplan","Shirley Truffier-Blanc"]
__email__ = ["n.kaplan@castsoftware.com,","s.truffier-blanc@castsoftware.com"]
__copyright__ = "Copyright 2022, CAST Software"

#class that allows the connexion to the database
class ActionPlan():

    def __init__(self, config:Config, log_level=INFO):
        self.logger = Logger(self.__class__.__name__, log_level)
        if self._open_database(config):
            
            site_packages=None
            for p in path:
                if 'site-packages' in p:
                    site_packages=p
                    break
            if site_packages is None:
                raise RuntimeError('rules file not found')

            self.file_name = abspath(f'{getsitepackages()[-1]}/cast_action_plan/rules.xlsx')
            if not exists(self.file_name):
                raise RuntimeError(f'{self.file_name} not found')
        else:
            raise RuntimeError("Database connection error")

    def _open_database (self, config:Config) -> bool:
        try:
            conn = connect(database=config.database, user=config.user, password=config.password, host=config.host, port=config.port)
            self._connection = conn
            self._session = conn.cursor()
            self.logger.debug("Connected to the database")
            return True
        except psycopg2.OperationalError as err : 
            self.logger.error(f"Database connection error: {err}")
            return False

    def close(self):
        self._session.close()
        self._connection.close()

   
    def fetch_data(self, app_name):

        self.logger.info(f"Retriving existing action items for {app_name}")
        db_full_name=f'{app_name}_central'.replace("-","_").replace(".","_")
        query_path = f'set search_path={db_full_name}'
        query = "select distinct dmv.metric_id, dmv.snapshot_id, dmv.functional_date, dmr.object_id from dss_metric_values dmv, dss_metric_results dmr where dmv.metric_id = dmr.metric_id order by dmv.metric_id asc"
        self._session.execute(query_path,query)

        #delete the content of the viewer_action_plan
        sql=f'Delete from {db_full_name}.viewer_action_plans'
        self._session.execute(sql)
        self._connection.commit()


    def export_data(self):
        #open and read what we have in the rules files
        self.logger.info(f'Reading Rules file: {self.file_name}')
        self.df = pd.read_excel(self.file_name)
        self.logger.debug("Dataframe", self.df)

        priorities = ['Fix Now', 'Near Term', 'Mid Term', 'Long Term', 'Tobereviewed'] 
        severity = [0,1,2,3,4]
        tag = ['Extreme', 'High', 'Moderate', 'Low', 'Tobereviewed']
        
        self.logger.info("Adding new action items")
        for p,s,t in zip(priorities,severity,tag):

            pd.set_option('mode.chained_assignment', None)
            fn = self.df[self.df['Final Priority'] == p]
            fn['adj_metric_id'] = fn['metric_id']+1
            ids = fn['adj_metric_id'].values.tolist()
            ids2 = str(ids).replace('[','(').replace(']',')')
            fn1 =fn.drop(columns=['metric_name', 'href', 'Business Criteria','Technical Criteria', 'critical', 'severity', 'technologyNames'])
            fn1.rename(columns={'Final Priority':'priority'}, inplace =True)
            sql = "insert into viewer_action_plans (metric_id, object_id, first_snapshot_date,last_snapshot_date,user_name,sel_date,priority,action_def,tag)"+\
                f"select distinct dmr.metric_id-1, object_id, (SELECT Max(functional_date) FROM dss_snapshots), timestamp '2100-01-01 00:00:00','admin', now(), {s}, '{p}', '{t}'"+\
                f"from dss_snapshots dmv, dss_metric_results dmr where dmr.snapshot_id = (select max(snapshot_id) from dss_snapshots) and metric_id in {ids2}"
                
            
            sql_1 = "SELECT action_def FROM viewer_action_plans WHERE action_def='Tobereviewed' ;"
            self._session.execute(sql)
            self._session.execute(sql_1)

            self._connection.commit()
        self.logger.info("Done")

    def run(self, app_name):
        self.fetch_data(app_name)
        self.export_data()

        
            
    
 