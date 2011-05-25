'''
Created on May 5, 2011

@author: jingweigu
'''
from Crawler import Crawler


class Thread(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
    
    def run(self):
        robot_url = "http://allrecipes.com/"
        root = 'http://allrecipes.com/Recipes/ViewAll.aspx?Page=1'
        depth_limit = 5
        confine_reg = ['http://allrecipes.com/Recipes/ViewAll.aspx\?Page\=[0-9]*$','http://allrecipes.com/Recipe/[a-zA-Z0-9\-]*/Detail.aspx$']
        c = Crawler(root, depth_limit,confine_reg,robot_url)  
        c.crawl()     