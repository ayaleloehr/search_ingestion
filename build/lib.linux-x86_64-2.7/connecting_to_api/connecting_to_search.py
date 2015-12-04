from subprocess import call
import json
from datetime import datetime
import time
class i14yClient:
    """
    document_id: an integer
    content: string - the content of the webpage to be indexed
    path: string - the url that has been scraped
    created: datetime object or string - the date and time that the object was scraped, if string must conform to the following: 2015-05-12T22:35:09Z
    drawer_handle: string - the name of the drawer (or bucket) that this content goes into
    secret_token: string - the secret token for the drawer found at: https://search.usa.gov/sites/{your user id}/i14y_drawers and then click on show (you can get to the above page by getting login credentials for search).
    title: string - the title of the page
    description: string - the description of the page
    promote: string (really a boolean and therefore should only take on true or false) - make the page stick to the top of search
    langauge: string (standard abbreviation of languages) - en stands for english
    """
    def create(self,document_id,content,path,created,drawer_handle,secret_token,title=None,description=None,promote="false",language="en"):
        #test drawer and key:"vets_staging:dd776d94f4d817c88496c1fb842fd440" -- REMOVE THIS BEFORE PUSHING TO GITHUB!!
        data = {}
        data["document_id"] = document_id
        if title: data["title"] = title
        data["path"] = path
        data["created"] = created
        if description: data["description"] = description
        data["content"] = content
        if promote: data["promote"] = promote
        if language: data["language"] = language
        datum = json.dumps(data)
        call(["curl","https://i14y.usa.gov/api/v1/documents","-XPOST","-H","Content-Type:application/json","-u",drawer_handle+":"+secret_token,"-d",datum])

    def delete(self,document_id,drawer_handle,secret_token):
        call(["curl","https://i14y.usa.gov/api/v1/documents/"+document_id,"-XDELETE", "-u", drawer_handle+":"+secret_token])

    def update(self,document_id,drawer_handle,secret_token,
               content=None,
               path=None,
               created=None,
               title=None,
               description=None,
               promote=None,
               language=None):
        data = {}
        #data["document_id"] = document_id
        if title: data["title"] = title
        if path: data["path"] = path
        if created: data["created"] = created
        if description: data["description"] = description
        if content: data["content"] = content
        if promote: data["promote"] = promote
        if language: data["language"] = language
        datum = json.dumps(data)
        print " ".join(["curl","https://i14y.usa.gov/api/v1/documents/"+document_id,"-XPUT","-H","Content-Type:application/json","-u",drawer_handle+":"+secret_token,"-d",datum])
        call(["curl","https://i14y.usa.gov/api/v1/documents/"+document_id,"-XPUT","-H","Content-Type:application/json","-u",drawer_handle+":"+secret_token,"-d",datum])


if __name__ == '__main__':
    client = i14yClient()
    client.create("1","Hello there, I am adding new content that should be deleted later","http://hackingagainstslavery.github.io",str(datetime.now()),"vets_staging","dd776d94f4d817c88496c1fb842fd440",title="please delete this",description="This content is from my personal website",promote="false",language="en")
    print "content created"
    #client.update("1","vets_staging","dd776d94f4d817c88496c1fb842fd440",content="This content is being updated")
    print "content updated"
    client.delete("1","vets_staging","dd776d94f4d817c88496c1fb842fd440")
    print "content deleted"
    #test drawer and key:"vets_staging:dd776d94f4d817c88496c1fb842fd440"

