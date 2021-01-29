import json

class urlpool:
    """
    use this class to create a good gitapi url
    """
    url = "https://api.github.com/search/repositories?q=language:{}+size:{}&sort=date&order=desc&page={}&access_token={}"
    searchlist = {'language':[],'size':[],'access_token':[]}
    def __init__(self,fp):
        massage = json.load(fp)
        self.searchlist['language'] = massage['language']
        self.searchlist['size'] = massage['size']
        self.searchlist['access_token'] = massage['access_token']
    def geturl(self):
        for lan in self.searchlist['language']:
            for size in self.searchlist['size']:
                for token in self.searchlist['access_token']:
                    for page in range(1,11):
                        print(self.url.format(lan,size,page,token))
    pass
        