import requests
from bs4 import BeautifulSoup
from typing import List

from time import sleep
import json  



# get urls of stories
def get_url(urlsoup: BeautifulSoup)->List:
    urls = []
    rooturl = 'https://americanliterature.com'
    rawlist = urlsoup.select("html body div.container div.jumbotron div.row div.col-md-4")
    for l in rawlist:
        urls.append(rooturl + l.a['href'])
    
    return urls 

def get_story(textsoup: BeautifulSoup)->List:
    story_title = textsoup.select("html body div.container div.jumbotron h1 cite")
    story_title = story_title[0].text

    story = [] #list of paragraphs
    paragraphs = textsoup.select("html body div.container div.jumbotron p")
    for block in paragraphs:
        content = block.text
        if content: # string is not empty
            story.append(block.text)
    story.pop(-1) #remove "return to [previous story] ... read another [next story]"

    return story_title, story



if __name__ == '__main__':
    #prepare short stories links in string
    urls = []
    for i in range(1,16):
        urlhtml = requests.get(f"https://americanliterature.com/short-story-library?page={i}").text
        urlsoup = BeautifulSoup(urlhtml, "html.parser")
        urls.extend(get_url(urlsoup))
        print(f"got {len(urls)} urls from page {i}")
        print("sleep for 5 seconds before sending another req")
        sleep(5) # wait for 5 seconds to send next request

    #open json file
    with open("shortstories.json", 'w', errors='replace') as f: #currently scraped files are not processed with "replace" parameter. If problem(unicode), apply this to scrape it again (before that, try to post-fix it)
        res = dict()
        #scrape one by one with interval of 5 seconds
        for url in urls:
            texthtml = requests.get(url).text
            textsoup = BeautifulSoup(texthtml, 'html.parser')
            title, paragraphs = get_story(textsoup)
            res[title] = paragraphs
            print(f"got {len(paragraphs)} paragraphs from story: {title}")
            print("wait another 5 seconds before sending another req")
            sleep(5) # wait for 5 seconds to send next request
        
        #link json in {title: link} format
        with open("stories_link.json", "w") as linkf:
            json.dump(
                        dict(
                            zip(res.keys(), urls)
                        ), 
                    linkf, indent=4)    
        
        json.dump(res, f, indent=4)






