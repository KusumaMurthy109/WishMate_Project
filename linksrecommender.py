import requests
from bs4 import BeautifulSoup 

class LinksRecommender: #scrapes the internet to search for recommended links
    def links(self, word):
        link = f"https://www.google.com/search?q={word}" #google links
        dictionary = {"key": "value"}
        answer = requests.get(link, dictionary) 
        bs4 = BeautifulSoup(answer.text, 'html.parser') #use the beautiful soup software
        link_list = []
        for link in bs4.find_all('a'):
            href = link.get('href')
            if href.startswith('/url?q='):
                www = href.split('/url?q=')[1].split('&')[0]
                link_list.append(www)
    
        sort = []
        for link in link_list:
            if word in link:
                sort.append(link)
        
        return sort #return the list of links


                



        
