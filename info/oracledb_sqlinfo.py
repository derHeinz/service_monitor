import cx_Oracle
import logging

logger = logging.getLogger(__name__)

class OracleDBInfo(object):

    def __init__(self, **kwargs):
        self.url = kwargs['url']
        self.sid = kwargs['sid']
        self.port = kwargs['port']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.sql = kwargs.get('sql', None)
        self.sqls = kwargs.get('sqls', None)
        
        if (self.sql==None and self.sqls==None):
            raise ValueError("either 'sql' or 'sqls' must be given")
        if (self.sql and self.sqls):
            raise ValueError("Only one of 'sql' or 'sqls' must be given")
            
    def do_db(self, stmtnts, automcommit=False):
        dsn = cx_Oracle.makedsn(self.url, self.port, self.sid)
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
