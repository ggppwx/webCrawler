'''
Created on Apr 25, 2011

@author: jingweigu
'''
#coding=utf-8
import re
import sys
import urllib2
import urlparse
from MyParser import Parser


#regular expression 
linkregex = re.compile('<a.*\shref=[\'"](.*?)[\'"].*?>')

class Fetcher(object):
    '''
    this class retrieves and interprets web pages 
    '''
    def __init__(self, url, page_count):
        '''
        Constructor
        input contains:
        url: the url of page to be fetched 
        page_count: count how many useful pages have been fetched 
        '''
        self.url = url
        self.out_urls = []
        self.page_count = page_count
        
    def out_links(self):
        return self.out_urls
    
    def _addHeaders(self, request):
        request.add_header("User-Agent","pyCrawler")
        
    '''
    open the current url 
    initialize the url parser
    '''
    def _open(self):
        url = self.url
        try:
            request = urllib2.Request(url)
            handle = urllib2.build_opener()
            
        except IOError:
            return None
        return (request, handle)
    
    '''
    save the fetched contents to local files
    '''
    def _save_to_file(self,path,data):
        f = open(path,'w')
        f.write(data)
        f.close()
        
    '''
    process the html file being fetched 
    get the contents of ingredients and recipe directions 
    '''
    def _process(self,url,content):
        p = Parser(content)
        title = p.parse_title_name()
        ingredients = p.parse_ingredients()
#        print ingredients
        directions = p.parse_directions()
        data = url + '\n-------------\n' + title +'\n-------------\n' + str(ingredients) +'\n-------------\n'+ str(directions)+'\n---------------\n'
        return title, data
        #self._save_to_file('./temp/'+title+'.txt', data)
    
    #process the links 
    #input a list of links 
    #output a storage format 
    def _process_links(self,links):
        data = ''
        for link in links:
            data = data + link + '\n'
        return data

    def fetch(self):
        '''
        main function in the fetcher class
        fetch the html page from a given url
        parse the content, extract userful informations and links this page contains 
        '''
        request, handle = self._open()
        self._addHeaders(request)
        if handle:
            try:
                data = handle.open(request)
                minme_type = data.info().gettype()
                url = data.geturl()
                content_temp = data.read()   #content is the content ofthis page 
                content = unicode(content_temp,"utf-8",errors = "replace")
                #get the title of this page 
                startPos = content.find('<title>')
                if startPos != -1:
                    endPos = content.find('</title>')
                    if endPos != -1:
                        title = content[startPos+7:endPos]
                        #print title
                  
                #process the content of the page   
                #save the content to files 
                content_title, content_data = self._process(self.url,content)
                  
                        
                #find all links of this page 
                links = linkregex.findall(content) 
                self.out_urls = self._queue_links(url, links, 0)
                
                '''TODO  process links '''
                link_data = self._process_links(self.out_urls)
                data = content_data + link_data
                #save data to file
                self._save_to_file('./temp/'+str(self.page_count)+'#'+content_title+'.txt', data)
                
                #content = unicode(data.read(),"uft-8",errors = "replace")
                
            except urllib2.HTTPError as error:
                if  error.code == 404:
                    print >> sys.stderr, "ERROR 404"
                else:
                    print >> sys.stderr, "ERROR is %s" % error
                
    '''
    process the fetched links
    filter some invalid links  
    '''
    def _queue_links(self,url,links, cid):
        out_put = []
        curl = urlparse.urlparse(url)
        for link in links:
            #process the link  
            if link.startswith('http://'):
                out_put.append(link)
            if link.startswith('/'):
                link = 'http://' + curl[1] + link
                out_put.append(link)
            elif link.startswith('#'):
                continue
            elif not link.startswith('http'):
                link = urlparse.urljoin(curl.geturl() ,link)
                out_put.append(link)    
                    
        return out_put 
            
