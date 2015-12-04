# Search Ingestion Engine

The goal of this module is to add search to your website.  In order to do this you'll need to do a few things:

1. Create an index of all the pages you want to be searchable
2. Define a way to search across those pages
3. Write a search bar

In this tool, We've made the following design choices:
1. The search ingestion engine is used to index all the pages within a domain - which was inspired by [Greg Gersh's](https://github.com/greggersh) [module](https://github.com/adhocteam/hc.gov-usasearch).  
2. The search ingestion engine then feeds into the [i14y search](http://search.digitalgov.gov/developer/i14y.html) developed by the wonderful people over at DigitalGov Search.
3. The search bar then searches all indexed pages, which are fed into their backend and displays the search results.

I want to note, these are the choices we made, and they are certainly not the only ones.  For reference and for fun, at the end of this README I've included other similar projects that work extremely well as well as something I made for fun.


ToDo:
Write a rake file and a sample rails app that uses this and updates index on run - inspired by pages api search


# References && silly things

1. The amazing folks over at 18F made this [wonderful tool](https://github.com/18F/jekyll_pages_api_search) - big shout out to Aidan Feldman for his work on it as well as suggesting it to me.
2. The folks over at search.digitalgov have open sourced their platform for search, so you can roll it on your own - [here is the github repo](https://github.com/GSA/i14y) 
3. Suppose you want to experiment with indexing and don't have access to a cluster environemnt, no worries - I wrote [a little search module]() that let's you do testing before moving over to a cloud environment, or is just right for small websites :)