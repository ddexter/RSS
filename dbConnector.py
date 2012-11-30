import psycopg2

class DBConnector:
    def __init__(self):
        self._conn = None
    
    def connect(self, host, dbname, user, password):
        # Connect to database
        self._conn = None
        try:
            connStr = "host='%s' dbname='%s' user='%s' password='%s'" % (host, dbname, user, password)
            self._conn = psycopg2.connect(connStr)
        except:
            print("Unable to connect")

        return self._conn
