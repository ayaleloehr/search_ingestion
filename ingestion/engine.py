import requests
from requests.auth import HTTPBasicAuth
import json
from unidecode import unidecode
import sqlite3
import lxml.html
from subprocess import call
import os
from datetime import datetime
import pandas as pd

class DatabaseEngine:
    def initialize_database(self):
        self.create_schema()
        self.create_db()

    def create_schema(self):
        if os.path.exists("database.db"):
            os.remove("database.db")
        table = """
        drop table if exists html;
        create table html (
        id integer primary key autoincrement,
        url text not null,
        html text not null
        );
        """
        with open("schema.sql","w") as schema:
            schema.write(table)

    def create_db(self):
        call(["./create_db.sh"],shell=True)

    def save(self,url,html):
        if not os.path.exists("database.db"):
            self.initialize_database()
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("insert into html (url,html) values (?,?)",(url,html))
    
# class AuthenticatedCrawler:
# #6 as a max is recommended for depth
#     #Turn off saving, soon
#     def __init__(self,base_url,depth,grab_all=False,save_to_database=False):
#         self.base_url = base_url
#         #this gets the important parts of the base url
#         self.domain_name = self.get_domain_name(base_url)
#         self.start_depth = depth
#         self.urls = []
#         self.data = []
#         self.num_urls = 0
#         self.grab_all = grab_all
#         self.save_to_database = save_to_database
#         if self.save_to_database:
#             self.db = DatabaseEngine()
    
#     def save_to_json(self)

#     def setup_database_saving(self):
#         self.save_to_database = True
#         self.db = DatabaseEngine()

#     def get_domain_name(self, url):
#         return url.split("//")[1].split("/")[0]
    
#     def update_base_url(self,base_url):
#         self.base_url = base_url

#     def update_depth(self,depth):
#         self.start_depth = depth

#     def links_grab(self,url):
#         r = requests.get(url)
#         domain_name = self.get_domain_name(url)
#         html = lxml.html.fromstring(unidecode(r.text))
#         content = str(unidecode(html.text_content()))
#         content = "".join([elem for elem in content if not elem in ["\t","\n","\r"]])
#         content = " ".join([elem for elem in content.split(" ") if elem != ''])
#         if self.save_to_database: self.db.save(url,content) #saves to the database, database.db
#         self.data.append(content)
#         url_list = html.xpath("//a/@href") 
#         uri_list = []
#         for uri in url_list:
#             if uri.startswith("/"):
#                 uri_list.append(domain_name+uri)
#             else:
#                 uri_list.append(uri)
#         return uri_list + [url] #ensures the url is stored in the final list

#     def crawl(self):
#         return self.crawler([self.base_url],self.start_depth)
    
#     def crawler(self,urls,depth):
#         urls = list(set(urls))
#         url_list = []
#         for url in urls:
#             if self.grab_all:
#                 url_list += self.links_grab(url)
#             else:
#                 if self.domain_name in url:
#                     url_list += self.links_grab(url)
#         url_list = list(set(url_list)) #dedup list
#         url_list = [uri for uri in url_list if uri.startswith("http")]
#         if depth > 1:
#             url_list += self.crawler(url_list,depth-1)
#         self.urls += url_list
#         self.urls = list(set(self.urls))
#         self.num_urls = len(self.urls)
#         return url_list


class Crawler:
    #6 as a max is recommended for depth
    #Turn off saving, soon
    def __init__(self,base_url,depth,grab_all=False,
                 save_to_database=False,basic_auth_required=False,
                 username=None,password=None,testing=False,protocol="https"
    ):
        self.base_url = base_url
        self.protocol = protocol + "://"
        #this gets the important parts of the base url
        self.domain_name = self.protocol+self.get_domain_name(base_url) #change this back to https
        self.username = username
        self.basic_auth_required = basic_auth_required
        self.password = password
        self.created = str(datetime.now())
        self.start_depth = depth
        self.testing = testing
        if not self.testing: self.df = pd.read_excel("page_descriptions.xlsx")
        self.urls = []
        self.data = []
        self.num_urls = 0
        self.grab_all = grab_all
        self.save_to_database = save_to_database
        if self.save_to_database:
            self.db = DatabaseEngine()
    
    def save_to_json(self):
        if self.data != []:
            json.dump(self.data,open("index.json","w"))
            return json.dumps(self.data)
                
    def setup_database_saving(self):
        self.save_to_database = True
        self.db = DatabaseEngine()

    def get_domain_name(self, url):
        if "https://" in url:
            self.protocol = "https://"
        elif "http://" in url:
            self.protocol = "http://"
        else:
            self.protocol = None
        return url.split("//")[1].split("/")[0]
    
    def update_base_url(self,base_url):
        self.base_url = base_url

    def update_depth(self,depth):
        self.start_depth = depth
    
    def update_credentials(self,username,password):
        self.username = username
        self.password = password

    def url_exists(self,url):
        for datum in self.data:
            if url == datum["path"]:
                return True
        return False

    def incorrect_url_ending(self,url):
        if url.endswith(".csv"): return True
        if url.endswith(".do"): return True
        if url.endswith(".pdf"):return True
        if "search_jobs?" in url: return True
        if "settings?" in url: return True
        if "request-password-reset?" in url: return True
        else: return False

    def links_grab(self,url):
        if self.incorrect_url_ending(url): return [] 
        if self.basic_auth_required:
            r = requests.get(url,auth=HTTPBasicAuth(self.username, self.password))
        else:
            r = requests.get(url)
        html = lxml.html.fromstring(unidecode(r.text))
        #checks if VEC urls are in page
        #remove this after VEC goes live
        VEC = [
            "/veterans-employment-center/",
            "https://www.vets.gov/veterans-employment-center/",
            "https://www.vets.gov/employment/",
            "/employment/"
        ]
        if any([uri in html.xpath("//a/@href") for uri in VEC]): 
            print "found"
            return []
        
        content = str(unidecode(html.text_content()))
        if "Coming Soon." in content:
            print "found"
            return []
        content = "".join([elem for elem in content if not elem in ["\t","\n","\r"]])
        content = " ".join([elem for elem in content.split(" ") if elem != ''])
        if self.save_to_database: self.db.save(url,content) #saves to the database, database.db
        datum = {}
        try:
            datum["title"] = html.xpath("//title")[0].text_content()
        except:
            print r.url
        datum["path"] = r.url
        datum["created"] = self.created
        datum["content"] = content
        
        if self.testing:
            datum["description"] = 'none'
        else:
            try:
                datum["description"] = str(self.df.Description[self.df.Page_Address == r.url].tolist()[0]) 
            except:
                datum["description"] = "none"
        datum["promote"] = "false"
        datum["language"] = "en"
        #remove after VEC goes live
        if not "veterans-employment-center" in url: self.data.append(datum)
        url_list = html.xpath("//a/@href") 
        uri_list = []
        for uri in url_list:
            if uri.startswith("/"):
                uri_list.append(self.domain_name+uri)
            else:
                uri_list.append(uri)
        return uri_list + [url] #ensures the url is stored in the final list

    def crawl(self):
        return self.crawler([self.base_url],self.start_depth)
    
    def crawler(self,urls,depth):
        urls = list(set(urls))
        url_list = []
        for url in urls:
            if self.grab_all:
                url_list += self.links_grab(url)
            else:
                if self.domain_name in url:
                    url_list += self.links_grab(url)
        url_list = list(set(url_list)) #dedup list
        url_list = [uri for uri in url_list if uri.startswith(self.domain_name)] 
        if depth > 1:
            url_list += self.crawler(url_list,depth-1)
        self.urls += url_list
        #temporary prune
        self.urls = list(set(self.urls))
        self.data = {v['path']:v for v in self.data}.values()
        self.num_urls = len(self.urls)
        return url_list

if __name__ == '__main__':
    #initialize_database()
    c = Crawler("https://hackingagainstslavery.github.io",2,grab_all=True)
    c.crawl()
    print c.urls
    print c.num_urls
    print c.data
