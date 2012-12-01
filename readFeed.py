import json
import urllib
import urllib2

class ReadFeed:
    def __init__(self):
        self._authToken = ""
        self._header = {}
        self._password = ""
        self._token = ""
        self._username = ""
    
    def login(self, username, password):
        self._username = username
        self._password = password

    def authenticate(self):
        # Get auth token
        authUrl = "https://www.google.com/accounts/ClientLogin"
        authReqData = urllib.urlencode({"Email": self._username,\
            "Passwd": self._password, "service": "reader"})
        authReq = urllib2.Request(authUrl, data=authReqData)
        authResp = urllib2.urlopen(authReq)
        authRespContent = authResp.read()
        authRespDict = dict(x.split('=')\
            for x in authRespContent.split('\n') if x)
        self._authToken = authRespDict["Auth"]

        # Create the cookie
        self._header['Authorization'] = 'GoogleLogin auth=%s' % self._authToken

        # Get API modifier token
        tokenUrl = "https://www.google.com/reader/api/0/token"
        tokenReq = urllib2.Request(tokenUrl, None, self._header)
        tokenResp = urllib2.urlopen(tokenReq)
        tokenRespContent = tokenResp.read()
        self._token = tokenRespContent[2:]

    def readStarred(self):
        readerUrl = "http://www.google.com/reader/api/0/stream/contents/user/-/state/com.google/starred?n=10000"
        readerReq = urllib2.Request(readerUrl, None, self._header)
        readerResp = urllib2.urlopen(readerReq)
        readerRespContent = readerResp.read()
        parsedContent = json.loads(readerRespContent)

        # item["origin"]["streamId"] = feed
        # item["id"] = id
        # item["title"] = title
        # item["summary"]["content"] = description
        # item["alternate"][0]["href"] = link
        # item["published"] = pubDate

        # Sometimes the description is in summary, sometimes content,
        # fix so that summary key already exists
        for item in parsedContent["items"]:
            if "summary" not in item.keys():
                if "content" in item.keys():
                    item["summary"] = item["content"]
                else:
                    item["summary"] = {}
                    item["summary"]["content"]= ''

        return parsedContent["items"]
    
    def removeStars(self, articles):
        url = "https://www.google.com/reader/api/0/edit-tag"
        for article in articles:
            # Remove star
            data = urllib.urlencode({"r":"user/-/state/com.google/starred",\
                "async":"true", "s":article["origin"]["streamId"],\
                "i":article["id"], "T":self._token})
            req = urllib2.Request(url, data, self._header)
            resp = urllib2.urlopen(req)

            # Mark as read
            data = urllib.urlencode({"a":"user/-/state/com.google/read",\
                "async":"true", "s":article["origin"]["streamId"],
                "i":article["id"], "T":self._token})
            req = urllib2.Request(url, data, self._header)

