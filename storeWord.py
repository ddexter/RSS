import nltk
import re
import string

class StoreWord:
    def __init__(self, conn):
        if conn == None:
            return

        self._TABLE = "words"
        self._conn = conn

        # Create table if it does not exist
        cursor = self._conn.cursor()
        existsStr = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='words')"
        cursor.execute(existsStr)

        if not cursor.fetchone()[0]:
            createStr = "CREATE TABLE words(id SERIAL PRIMARY KEY, word VARCHAR(60) NOT NULL, count INTEGER NOT NULL)"
            createIdx1Str = "CREATE INDEX word_idx ON words(word)"
            createIdx2Str = "CREATE INDEX count_idx ON words(count DESC)"
            cursor.execute(createStr)
            cursor.execute(createIdx1Str)
            cursor.execute(createIdx2Str)
            self._conn.commit()

    def formatWordList(self, words):
        # Strip HTML codes
        pattern = re.compile('&#[0-9]+;', re.UNICODE)
        tmp = [pattern.sub('', word) for word in words]

        # Strip punctuation
        # Strip "'s"
        tmp = [word.replace("'s", '') for word in tmp]
        # Strip non-alphanumerics
        pattern = re.compile('[\W_]+', re.UNICODE)
        tmp = [pattern.sub('', word) for word in tmp]

        # GTFO UNICODE!
        tmp = [word.encode('ascii', 'ignore') for word in tmp]

        # To lower case
        tmp = [word.lower() for word in tmp]

        # Remove stop words
        stopWords = nltk.corpus.stopwords.words('english')
        tmp = [word for word in tmp if word not in stopWords]

        # Remove empty words
        tmp = [word for word in tmp if word != '']

        # Lemmatize
        lmzr = nltk.stem.wordnet.WordNetLemmatizer()
        lemmaWords = [lmzr.lemmatize(word) for word in tmp]

        return lemmaWords

    def insert(self, articles):
        existsStr = "SELECT EXISTS(SELECT 1 FROM words WHERE word = '%s' LIMIT 1)"
        updateStr = "UPDATE words SET count = count + 1 WHERE word = '%s'"
        createStr = "INSERT INTO words (word, count) VALUES ('%s', 1)"

        cursor = self._conn.cursor()

        for article in articles:
            # Retrieve words in title of each article
            title = article["title"].replace('-', ' ')
            words = title.split()
            words = self.formatWordList(words)
            nWords = len(words)

            for i,word in enumerate(words):
                # Insert/increment unigram
                cursor.execute(existsStr % (word))
                
                eWord = cursor.fetchone()[0]
                if eWord:
                    cursor.execute(updateStr % (word))
                else:
                    cursor.execute(createStr % (word))
                self._conn.commit()

                # Insert/increment bigram
                if i < nWords - 1:
                    cursor.execute(\
                        existsStr % (word + ' ' + words[i + 1]))
                    
                    eWord = cursor.fetchone()[0]
                    if eWord:
                        cursor.execute(\
                            updateStr % (word + ' ' + words[i + 1]))
                    else:
                        cursor.execute(\
                            createStr % (word + ' ' + words[i + 1]))

                    self._conn.commit()

    def getTopHits(self, n=100):
        queryStr = "SELECT word, count FROM words ORDER BY count DESC LIMIT %d"

        cursor = self._conn.cursor()

        cursor.execute(queryStr % (n))
        wordList = cursor.fetchall()

        return wordList
