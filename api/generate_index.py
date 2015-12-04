from ingestion.engine import Crawler
from api.clients import i14yClient
from sys import argv
import json

def main(website,depth):
    website = "https://" + website
    c = Crawler(website,int(depth))
    c.crawl()
    c.save_to_json()
    index = json.load(open('index.json','r'))
    for ind,elem in enumerate(index):
        i14yClient.create(ind,elem['content'],elem['path'],
                          elem['created'],os.environ["drawer_handle"],os.environ["search_secret_token"],
                          title=elem['title'],description=elem['description'],
                          promote=elem['promote'],language=elem['language']) 
    
