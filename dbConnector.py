import psycopg2

class DBConnector:
    def __init__(self):
        self._conn = None
    
    def connect(self, host, dbname, user, password):
        # Connect to database
        self._conn = None

        # Sometimes there are random problems connecting, try 100 times.
        # Realistically should connect on the first 1 or 2 attempts
        for i in range(100):
            try:
                connStr = "host='%s' dbname='%s' user='%s' password='%s'" % (host, dbname, user, password)
                self._conn = psycopg2.connect(connStr)
            except:
                if i == 99:
                    print("Unable to connect")
                    self._conn = None
                continue

            # Stop trying to connect once link established
            break

        return self._conn
