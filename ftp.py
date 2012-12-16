import paramiko

class FTP:
    def connect(self, host, port, username, password):
        self.transport = paramiko.Transport((host, port))
        self.transport.connect(username = username, password = password)

    def push(self, fileFrom, fileTo, encrypted=True):
        ftp = None

        if encrypted:
            ftp = paramiko.SFTPClient.from_transport(self.transport)
        else:
            ftp = paramkio.FTPClient.from_transport(self.transport)

        ftp.put(fileFrom, fileTo)
        ftp.close()

    def close(self):
        self.transport.close()
