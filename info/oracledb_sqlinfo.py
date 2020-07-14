import cx_Oracle
import logging

logger = logging.getLogger(__name__)

class OracleDBInfo(object):

    def __init__(self, **kwargs):
        self.url = kwargs['url']
        
        self.sid = kwargs.get('sid', None)
        self.service_name = kwargs.get('service_name', None)
        
        self.port = kwargs['port']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.sql = kwargs.get('sql', None)
        self.sqls = kwargs.get('sqls', None)
        
        if (self.sql==None and self.sqls==None):
            raise ValueError("either 'sql' or 'sqls' must be given")
        if (self.sql and self.sqls):
            raise ValueError("Only one of 'sql' or 'sqls' must be given")
            
        if (self.sid==None and self.service_name==None):
            raise ValueError("either 'sid' or 'service_name' must be given")
        if (self.sid and self.service_name):
            raise ValueError("Only one of 'sid' or 'service_name' must be given")
            
    def do_db(self, stmtnts, automcommit=False):
        dsn = None
        if self.sid:
            dsn = cx_Oracle.makedsn(self.url, self.port, sid=self.sid)
        else:
            dsn = cx_Oracle.makedsn(self.url, self.port, service_name=self.service_name)
        results = []
        with cx_Oracle.connect(self.user, self.password, dsn) as connection:

            connection.autocommit = automcommit
            cursor = connection.cursor()
            
            for stmt in stmtnts:
                cursor.execute(stmt)
                logger.debug("executing: {}".format(stmt))
                logger.debug("result:")
                if (stmt.strip().lower().startswith("select")):
                    for row in cursor:
                        results.append(row)
                        logger.debug(row)
                else:
                    logger.debug("rows affected: " + str(cursor.rowcount))
        return results
    
        
    def query_info(self):
        stmts = None
        if self.sql:
           stmts = [self.sql]
        else:
            stmts = self.sqls
        
        res = self.do_db(stmts)
        return str(res)
