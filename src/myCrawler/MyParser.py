'''
Created on Apr 29, 2011

@author: jingweigu
'''
from BeautifulSoup import BeautifulSoup
import re


class Parser():
    '''
    classdocs
    '''


    def __init__(self, data):
        '''
        Constructor
        '''
        self.soup = BeautifulSoup(data)
    
    def find_text_inclass(self, tagname, classname):
        contents = self.soup.find(tagname,{"class":classname})
        return contents
    
    def find_text_intag(self,tagname):
        contents = self.soup.find(tagname)
        return contents
    
    #parse the title name of url  
    def parse_title_name(self):
        title = self.find_text_intag('title').string
        title = re.search('\s*(\S[^\n\r]*\S)\s*', title).group(1)
        return title
    
    '''
    parse the ingredients from the url  
    return a list of ingredients
    '''
    def parse_ingredients(self):
        ret_ingredients = ''
        ingredients = self.find_text_inclass('div', 'ingredients')
        if ingredients == None:
            return None
        else:
            ingredients = ingredients.fetch('li')
            for ingredient in ingredients:
                ingredient = re.search('\s*(\S[^\n\r]*\S)\s*', ingredient.string).group(1)
                ret_ingredients =ret_ingredients + (ingredient + ' \n')
        return ret_ingredients      
    
    '''
    parse the directions from the url    
    '''
    def parse_directions(self):
        ret_directions = ''
        directions = self.find_text_inclass('div', 'directions')
        if directions == None:
            return None
        else:
            directions = directions.fetch('span')
            for direction in directions:
                direction = re.search('\s*(\S[^\n\r]*\S)\s*', direction.string).group(1)
                ret_directions = ret_directions + (direction + ' \n')
        return ret_directions