'''
Created on Apr 20, 2011

@author: jingweigu
'''
import sys
import re
import urlparse
from Queue import Queue
from Fetcher import Fetcher
import robotparser

class Crawler(object):
    '''
    classdocs
    '''
    def __init__(self, root, depth_limits,confine=None, robot_url=None, exclude=[], locked=True, filter_seen=True):
        '''
        Constructor
        initialize the crawler 
        input contains 
        root: the starting url 
        depth_limits: Max depth (number of hops from root)
        confine: Limit search to this prefix
        robot_url: the url stores robot policy file
        exclude: URL prefixes NOT to visit
        locked:  Limit search to a single host?
        filter_seen: if the filter can be seen 
        '''
        self.root = root
        self.host = urlparse.urlparse(root)[1]
        
        self.depth_limit = depth_limits
        self.locked = locked
        self.confine_prefix = confine
        self.exclude_prefixes = exclude
        
        #retrieve the robot rules
        self.rp = robotparser.RobotFileParser()
        self.rp.set_url('http://'+self.host+'/robots.txt')
        self.rp.read()
        
        self.url_seen = set()
        self.urls_remembered = set()
        self.visited_links = set()
        self.links_remembered = set()
        
        self.page_count = 0
        self.num_links = 0
        self.num_followed = 0
        
        self.pre_visit_filters = []
    
    def _url_filter(self, url, reg_list):
        ''' judge if the url has satisfy certain regular expression '''
        for reg in reg_list:
            result = re.match(reg, url)
            if not result == None:
                return True
            
        return False
            

        
    def crawl(self):
        '''
        main function in the crawling process 
        q <- starting page
        while q not empty:
           url <- q.get()
           if url is new and suitable:
              page <- fetch(url)   
              q.put(urls found in page)
           else:
              nothing
        
        '''
        q = Queue()
        q.put((self.root,0))  #0 stands for the level 
        
        while not q.empty():
            this_url, depth = q.get()
#            this_url_host = urlparse.urlparse(this_url)[1]
            
            #check if it obeys robot courtesy 
            try:
#                self.rp.set_url('http://'+this_url_host+'/robots.txt')
#                self.rp.read()
                #if not allowed by robots.txt, discard it 
                if not self.rp.can_fetch('PyCrawler', this_url):
                    #print this_url+'not allowed by robot\n'
                    continue
            except:
                pass
            
            #discard links over depth
            if depth > self.depth_limit:   
                continue
            
            #check if the page is new 
            if this_url in self.url_seen:
                continue
            else:
                self.url_seen.add(this_url)
            
            #if this url doesn't satisfy the filter condition
            filter_reg = self.confine_prefix;
            if not self._url_filter(this_url, filter_reg):
                continue
            
            #the url is new 
            
            do_not_follow = self.pre_visit_filters#[f for f in self.pre_visit_filters if not f(this_url)]
            
            if depth == 0 and [] != do_not_follow:
                print >> sys.stderr, "error, starting url is rejected"
                
            #if no filters failed
            if [] == do_not_follow:
                try:
                    self.visited_links.add(this_url)
                    #self.url_seen.add(this_url)
                    self.num_followed += 1
                    page = Fetcher(this_url,self.page_count)
                    page.fetch()  #fetch the page, save the file into local 
                    
                    self.page_count += 1
                    print self.page_count    #test 
                    for link_url in page.out_links():
                        if link_url not in self.url_seen:   #if the url is new 
                            q.put((link_url,depth+1))
                            #self.url_seen.add(link_url)
                            
                except:
                    print >>sys.stderr, "ERROR: Can't process url '%s' " % this_url
        
            
            
'''  test Crawler '''
'''
root = 'http://allrecipes.com/Recipes/ViewAll.aspx?Page=1'
depth_limit = 5
confine_reg = ['http://allrecipes.com/Recipes/ViewAll.aspx\?Page\=[0-9]*$','http://allrecipes.com/Recipe/[a-zA-Z0-9\-]*/Detail.aspx$']
c = Crawler(root, depth_limit,confine_reg)  
c.crawl()      
        
'''     
        
        