import psycopg2

class DBConnector:
    def __init__(self):
        self._conn = None
    
    def connect(self, host, dbname, user, password):
        # Connect to database
        self._conn = None

        # Sometimes pyscopg2 does not connect right away.  Try 100 times and
        # fail if cannot connect after that
        for i in range(100):
            try:
                connStr = "host='%s' dbname='%s' user='%s' password='%s'" % (host, dbname, user, password)
                self._conn = psycopg2.connect(connStr)
            except:
                if i == 99:
                    print("Unable to connect")
                    self._conn = None
                    return

                continue

            # If we make it here, we're connected, so stop trying to reconnect
            break

        return self._conn
