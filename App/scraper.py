import requests
import pandas as pd
from bs4 import BeautifulSoup as bs4


class GithubScrapper:

    def __init__(self, username, pages = 7):
        url = 'https://github.com/' + username + '?tab=repositories'
        self.Data = {}
        self.pages = pages
        self.url = url
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referrer': 'http://www.wikipedia.org/',
            'Connection': 'keep-alive',
            'Content-Type': 'text/html; charset=utf-8'
        }


    def nextPage(self, url):
        request = requests.get(url, headers=self.headers)
        soup = bs4(request.text, 'html.parser')
        token = soup.findAll('a', {'class': 'btn btn-outline BtnGroup-item'})
        # if token.text == 'Next':
        for t in token:
            if 'after' in t.get('href'):
                return t.get('href')


    def getRepo(self):
        url = self.url
        pages = self.pages
        Url = []
        RepoName = []
        for i in range(1, pages):
            try:
                result = {}
                base_url = "https://github.com/"
                request = requests.get(url, headers=self.headers)
                
                soup = bs4(request.text, 'html.parser')
                titles = soup.findAll('h3', {'class': 'wb-break-all'})
                url = self.nextPage(url)
                

                for title in titles:
                    hrefs = title.findAll('a')
                    href = [base_url + h.get('href') for h in hrefs]
                    text = title.text.strip()
                    Url.append(href[0])
                    RepoName.append(text)

                
                    self.Data['RepoName'] = RepoName
                    self.Data['Url'] = Url

                    
            except Exception as e:
                pass

        
        data = list(zip(self.Data['RepoName'], self.Data['Url']))
        df = pd.DataFrame(data=data, columns=["Repo Name", "url"])
 

        print('Yeah Bright')
        print('Complete...............')
        return df

    def saveCsv(self):
        data = list(zip(self.Data['RepoName'], self.Data['Url']))
        df = pd.DataFrame(data=data, columns=["Repo Name", "url"])

        return df.to_csv('Repo.csv')
        

