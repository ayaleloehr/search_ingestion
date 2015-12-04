from ingestion.engine import Crawler
from api.clients import i14yClient
from sys import argv
import pickle
import json

website_creds = pickle.load(open("website_creds.pickle","r"))
backend_creds = pickle.load(open("backend_creds.pickle","r"))
c = Crawler(argv[1],int(argv[2])) #,username=website_creds["username"],password=website_creds["password"],basic_auth_required=True)
c.crawl()
#print c.data
#print c.urls
c.save_to_json()
index = json.load(open('index.json','r'))
for ind,elem in enumerate(index):
    i14yClient.create(ind,elem['content'],elem['path'],
                      elem['created'],backend_creds["drawer_handle"],backend_creds["secret_token"],
                      title=elem['title'],description=elem['description'],
                      promote=elem['promote'],language=elem['language']) 
    
