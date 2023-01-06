import psycopg2
import argparse
import pandas as pd
from config import Config
from psycopg2 import connect
from logger import Logger
from logger import INFO
from os.path import exists,abspath


#class that allows the connexion to the database
class ActionPlan():

    def __init__(self, config, log_level=INFO):
        self.logger = Logger(self.__class__.__name__, log_level)
        self._open_database(config)
        #TODO add rules file location to configuration file
        self.file_name = abspath('./rules.xlsx')

        if not exists(self.file_name):
            raise RuntimeError(f'{self.file_name} not found')


    def _open_database (self, config):
        try:
            conn = connect(database=config.database, user=config.user, password=config.password, host=config.host, port=config.port)
            self._connection = conn
            self._session = conn.cursor()
            self.logger.debug("Connected to the database")
        except psycopg2.Error as e:
            self.logger.error("Error %d: %s" % (e.args[0],e.args[1]))

    def close(self):
        self._session.close()
        self._connection.close()

   
    def fetch_data(self, app_name):

        self.logger.info("Retriving existing action items")
        db_full_name=f'{app_name}_central'.replace("-","_")
        
        
        query_path = f'set search_path={db_full_name}'
        query = "select distinct dmv.metric_id, dmv.snapshot_id, dmv.functional_date, dmr.object_id from dss_metric_values dmv, dss_metric_results dmr where dmv.metric_id = dmr.metric_id order by dmv.metric_id asc"
        self._session.execute(query_path,query)

        #delete the content of the viewer_action_plan
        sql=f'Delete from {db_full_name}.viewer_action_plans'
        self._session.execute(sql)
        self._connection.commit()


    def export_data(self):
        #open and read what we have in the rules files
        self.df = pd.read_excel(self.file_name)
        self.logger.debug("Dataframe", self.df)
        # TODO: debug.log

        priorities = ['Fix Now', 'Near Term', 'Mid Term', 'Long Term'] 
        severity = [0,1,2,3]
        tag = ['Extreme', 'High', 'Moderate', 'Low']
        
        self.logger.info("Adding action items")
        for p,s,t in zip(priorities,severity,tag):
            pd.set_option('mode.chained_assignment', None)
            fn = self.df[self.df['Final Priority'] == p]
            fn['adj_metric_id'] = fn['ID']+1
            ids = fn['adj_metric_id'].values.tolist()
            ids2 = str(ids).replace('[','(').replace(']',')')
            fn1 =fn.drop(columns=['Name', 'HREF', 'Business Criteria','Technical Criteria', 'Critical', 'Severity', 'TechnologyNames'])
            fn1.rename(columns={'Final Priority':'priority'}, inplace =True)
            sql = "insert into viewer_action_plans (metric_id, object_id, first_snapshot_date,last_snapshot_date,user_name,sel_date,priority,action_def,tag)"+\
                f"select distinct dmr.metric_id-1, object_id, (SELECT Max(functional_date) FROM dss_snapshots), timestamp '2100-01-01 00:00:00','admin', now(), {s}, '{p}', '{t}'"+\
                f"from dss_snapshots dmv, dss_metric_results dmr where dmr.snapshot_id = (select max(snapshot_id) from dss_snapshots) and metric_id in {ids2}"
           
            self._session.execute(sql)
            self._connection.commit()
        self.logger.info("Done")

    def run(self, app_name):
        self.fetch_data(app_name)
        self.export_data()

        


if __name__ == '__main__':
    print('\nCAST Action Plan Generation Tool')
    print('Copyright (c) 2022 CAST Software Inc.\n')
    print('If you need assistance, please contact Nevin Kaplan (NKA) from the CAST US PS team\n')

    parser = argparse.ArgumentParser(description='Assessment Action Plan Generation Tool')
    parser.add_argument('-c','--config', required=True, help='Configuration properties file')
    args = parser.parse_args()

    db = ActionPlan(Config(args.config))
    
    
 