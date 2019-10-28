from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import os
import re
import time
import json

def visit_link(page_link):
    t=0
    page_response = ''
    while page_response == '':
        t += 1
        #  try 5 times, if no response skip this link
        if t <= 5:
            try:
                page_response = requests.get(page_link)
                break
            except:
                t += 1
                print("Connection refused by the server..")
                print("Let me sleep for 15 seconds")
                print("ZZzzzz...")
                time.sleep(15)
                print("Was a nice sleep, now let me continue...")
                continue
        else:
            page_response = 0
    return page_response
    
            
def grab_web(page_response, page_link):

    if page_response == 0:
        print('!!!! No response!')
        echo=0
    
    else:
        
        if page_response.status_code != 200:
            print("!!!You can't scrape this", page_response.status_code)
            echo = 0
            
        else:
            
            print("Grabbing...", page_link)
            domain = urlparse(page_link).netloc # domain name
            print("via domain", domain)
            print("Status is", page_response.status_code) # 200, 403, 404, 500, 503
            echo=1
            
    return echo
 
    

 #  get all url with the domain name       
def getInternalLinks(page_content, includeUrl):
    includeUrl = urlparse(includeUrl).scheme+"://"+urlparse(includeUrl).netloc
    internalLinks = []
    for link in page_content.findAll("a", href=re.compile("^(/|.*"+includeUrl+")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if(link.attrs['href'].startswith("/")):
                    internalLinks.append(includeUrl+link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])
    return internalLinks

    
    

def collect_text(page_content, page_link,file_name):
        all_content = []

        with open(filename +'.json','a') as outfile:
            outfile.write('--------------------------------- Contents from  '+page_link +'-----------------------------------\n')
        for paragraph in page_content.find_all('p'):
            Content_list = [text for text in paragraph.stripped_strings]
            if Content_list != []:
            
                for each in Content_list:
                    all_content.append(Content_list)
        
                with open(file_name+'.json','a') as outfile:
                    json.dump(Content_list, outfile, ensure_ascii=False)
                    outfile.write('\n')
        return all_content


        
        
        
    
linkslist = {}
linksset = set()
All_content={}

#you can choose your depth here
depth = 3
for d in range(depth):
    linkslist['url',d]=[]

    
i = 0
    
your_link = input("Enter the url to scrape: ")
#filename is the same as url
filename = your_link.replace('/','_')
path = os.getcwd()




if os.path.exists(os.path.join(path,filename +'.json')):
    
    choice = input('File existed, replace it?(ENTER 1 OR 2 (yes:1, no:2)):')
    if choice == '1':
        with open(filename +'.json','w') as outfile:
            outfile.write(' ROOT: '+ your_link +'\n')
    else:
        filename= input('new filename:')
        with open(filename +'.json','w') as outfile:
            outfile.write('ROOT:'+ your_link)


linkslist['url',0].append(your_link)
linksset.add(your_link)

while i < depth:
            
    print('-----------------------------------Grabbing the LAYER# ' , i,'-------------------------------------')
        
        
    for link in linkslist['url',i]:
        All_content[link] = []
        response = visit_link(link)
        allow_access = grab_web(response,link)
        if allow_access:
            
            content = BeautifulSoup(response.content, "html.parser")
            data=collect_text(content,link,filename)
            All_content[link]= data
            if i < depth-1:
                links = getInternalLinks(content, link)
    
                if links is None:
                    print('!!!no links on this webpage'+ link)
                    break
                else:
                    # Filter links and update linkslist
                    for j in range(len(links)):
                    
                        if links[j] not in linksset:
                            linkslist['url',(i+1)].append(links[j])
                            linksset.add(links[j])

        

    i+=1



            
    


    


            
            


            
    
    
