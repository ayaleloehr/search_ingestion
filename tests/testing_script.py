from ingestion.engine import Crawler

c = Crawler("http://127.0.0.1:5000",2,testing=True,protocol="http")
c.crawl()
print c.data
print c.urls
