import pytagcloud

class TagCloud:
    def __init__(self):
        self._colors = [\
            # Orange
            (255, 153, 0),\
            # Grey
            (119, 119, 119),\
            # Black
            (0, 0, 0),\
            ]

    def makeCloud(self, tagsCounts, name="tag_cloud.png", height=500,\
        width=500, font="Droid Sans"):

        # Get rid of unigrams contained in bigrams
        tagsCounts = self.parseWords(tagsCounts)

        tags = pytagcloud.make_tags(tagsCounts, colors=self._colors)

        pytagcloud.create_tag_image(tags, name, size=(width, height),\
            fontname=font, rectangular=True)
    
    def parseWords(self, tagsCounts):
        # Remove unigram words of bigrams in list
        unigrams = set()

        for tagCount in tagsCounts:
            gram = tagCount[0]
            words = gram.split()

            if len(words) > 1:
                unigrams.add(words[0])
                unigrams.add(words[1])

        ret = []
        for tagCount in tagsCounts:
            if tagCount[0] not in unigrams:
                ret.append(tagCount)

        return ret

