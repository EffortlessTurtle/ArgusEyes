#       <ArgusEyes,webscraper for news stories,v0.23,Working,EffortlessTurtle>
########################################################################
#       <TODO>
# -finish other methods to scrape other sites
# -Figure out multithreading (under investigation)
# -make different sections write to separate files at same time using multi-threading. (methodology under investigation)   
# -Check path to ensure that it's always pointed at the Desktop (methodology under investigatio)
# -eventually to be hosted and then emails? result every 2 hours to a special account
# -Eventually output to css
#
#########################################################################


# imports

import requests
import progressbar
from bs4 import BeautifulSoup
import datetime as dt
from dateutil import parser
from pathlib import Path
import os
import time
import feedparser as fp

# Classes

class Quill: #For the write to file section of a FXN
    """ Preps and makes both CSV and human readable file. Custom Class for ArgusEyes. """
    def __init__(self, tit_CSI, exer_CSI, dat_CSI, file_fo):
        """Do I really need to put anything here?"""
        self.title = tit_CSI
        self.ex = exer_CSI
        self.date = dat_CSI
        self.fo = file_fo    
    def write(title, ex, date,site_nam, fo): #Writes this to the file from main()
        """ Writes Human Readable file"""
        fo.write(str(date) + "\n\n")
        fo.write(title + "\n")
        fo.write("\n")
        fo.write(ex)
        fo.write('\nfrom: '+ site_nam + "\n" + 140 * '-'+"\n")
    def title_write(name,fo): #Writes the of the title of site with different format to file.
        """ Writes Human Readable title of source """ 
        name = str(name) + '\n\n'
        fo.write(15 * ' ' + name + '-- Date Pulled: ' + str(dt.date.today()) + "\n")
        fo.write(140 * "^" + '\n\n')
    def csv_file_prep(fo): #Preps files as CSV file
        """ Preps first line of file for CSV """
        fo.write('DATE' + "," + "HEADLINE" + "," + "EXCERPT" + "," + "Source" + "\n")
    def csv_tit_write(name, fo): #Writes title line of the CSV
        """Writes title line of the CSV """
        date = dt.date.today()
        fo.write('\nPulled:' + str(date) + "," + name + ", " + "\n")
    def csv_write(title, excerpt, date,fo): #Writes the entries to CSV
        """ Writes the entries to CSV """
        fo.write(str(date) + "," + title + "," + excerpt)
        
class LoadBar:
    """Loading bar class"""
    def __init__(self) -> None:
        pass
    def load_me(sit_name):
        #Loading bar
        widgets = [f'{sit_name} ', progressbar.AnimatedMarker()]
        bar = progressbar.ProgressBar(widgets=widgets).start()
        i = 0
        for i in range(50):
            time.sleep(0.1)
            bar.update(i)
#Globals

#Must pass in 'fo' for the Quill class to work
def epoch_US(fo):  # Pulls title, blurb and date written for Epoch - US
    """ Pulls Epoch - US News"""
    #Get text from website
    url = 'https://www.theepochtimes.com/c-us'
    site_nam = 'The Epoch Times - US News'
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    #Write site name to fo
    Quill.title_write(site_nam,fo)
    #Loading bar
    LoadBar.load_me(site_nam)
    #Begin collecting news stories
    for x in range(2, 3):
        response = requests.get(url)  # -MARK, must remain to keep requesting correct site
        text = response.text  #-MARK, must remain to keep requesting correct site
        data = BeautifulSoup(text, 'html.parser')  # -MARK, must remain to keep requesting correct site
        # For loop through each container for title, time and who reported
        for tag in data.find_all(class_="article_info text"):
            # get title of article
            title = tag.find(class_='title').text.strip(
            ) if tag.find(class_='title') else ''
            # Get the short news excerpt
            more_info = tag.find(class_='excerpt more_info').text.strip(
            ) if tag.find(
                class_='excerpt more_info') else 'Epoch - US'
            # Get Date article was written
            date = tag.find(class_='time').text.strip(
            ) if tag.find(class_='time') else ''
            #Write to file the date, title and blurb
            Quill.write(title,more_info,date,site_nam,fo)
            #update loading bar
        #Readies the url to request next page    
        url = f"https://www.theepochtimes.com/c-us/" + str(x) 

def epoch_latest(fo):  # Pulls title, blurb and date written for Epoch - latest
    """ Pulls Epoch - Latest """
    url = 'https://www.theepochtimes.com/latest/'
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    site_nam = 'Epoch - Latest'
    #Write site name to 'fo'
    Quill.title_write(site_nam,fo)
    #loading bar
    LoadBar.load_me(site_nam)
    #Gets first 3 pages
    for x in range(2, 3):
        response = requests.get(url)  # NOTE: marked must stay here, otherwise you never request the next page's content from website
        text = response.text
        data = BeautifulSoup(text, 'html.parser')  
        # For loop through each container for title, time and who reported
        for tag in data.find_all(class_="article_info text"):
            # get title of article
            title = tag.find(class_='title').text.strip(
            ) if tag.find(class_='title') else ''
            # Get the short news excerpt
            more_info = tag.find(class_='excerpt more_info').text.strip(
            ) if tag.find(
                class_='excerpt more_info') else 'Epoch - Latest'
            # Get Date article was written
            date = tag.find(class_='time').text.strip(
            ) if tag.find(class_='time') else 'No date available'
            date2 = parser.parse(date)
            if date2 != dt.date.today():  # counter to
                Quill.write(title,more_info,date,site_nam,fo)
            else:
                Quill.write(title,more_info,date,site_nam,fo)
        url = f"https://www.theepochtimes.com/latest/" + str(x)

def epoch_USPol(fo):  # Pulls title, blurb and date written for Epoch - Politics
    """ Pulls Epoch - US Polititcs """
    url = 'https://www.theepochtimes.com/c-us-politics'
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    site_nam = "Epoch Times - US Politics"
    #Write site name to file 'fo'
    Quill.title_write(site_nam,fo)
    #loading bar
    LoadBar.load_me(site_nam)
    for tag in data.find_all(class_="post_list"):
        # get title of article
        title = tag.find(class_='title').text.strip(
        ) if tag.find(class_='title') else ''
        # Get the short news excerpt
        more_info = tag.find(class_='excerpt more_info').text.strip(
        ) if tag.find(
            class_='excerpt more_info') else 'No Info Availabe'
        # Get Date article was written
        date = tag.find(class_='time').text.strip(
        ) if tag.find(class_='time') else 'No date available'
        date2 = parser.parse(date)
        if date2 != dt.date.today():  # counter to
            Quill.write(title,more_info,date,site_nam,fo)
        else:
            Quill.write(title,more_info,date,fo)

def epoch_World(fo):        #Pulls title, blurb and date Epoch - World
    """ Pulls the Epoch world news """
    #get request, parse into text
    url = 'https://www.theepochtimes.com/c-world'
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    #Variables
    site_nam ="Epoch - World"
    container_class_stand_in = "post_list"
    title_class_stand_in = "title"
    excerpt_class_stand_in = "excerpt more_info"
    time_class_stand_in = "time"
    #write site name to file
    Quill.title_write(site_nam,fo)
    #loading bar    
    LoadBar.load_me(site_nam)
    # For loop through each container for title, time and who reported
    for tag in data.find_all(class_=container_class_stand_in):
        # get title of article
        title = tag.find(class_=title_class_stand_in).text.strip(
        ) if tag.find(class_=title_class_stand_in) else ''
        # Get the short news excerpt
        more_info = tag.find(class_=excerpt_class_stand_in).text.strip(
        ) if tag.find(
            class_=excerpt_class_stand_in) else '\nEpoch - World'
        # Get Date article was written
        try:
            date = tag.find(class_=time_class_stand_in).datetime.text.strip()
        except AttributeError:
            date = ''
        #write to file section
        Quill.write(title,more_info,date,site_nam,fo)

def bbc_WOR_RSS(fo):        #Pulls title, blurb and date BBC world
    """ Pulls the bbc world news """
    #Define url, and parse this into text
    url = 'https://www.bbc.com/news/world'
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    site_name = "BBC - WORLD"
    #Write site name to file
    Quill.title_write(site_name,fo)
    #Loading bar
    LoadBar.load_me(site_name)
    #Stand ins used for obvious reasons
    bold_container = "gs-c-promo-body gs-u-mt@xxs gs-u-mt@m gs-c-promo-body--primary gs-u-mt@xs gs-u-mt@s gs-u-mt@m gs-u-mt@xl gel-1/3@m gel-1/2@xl gel-1/1@xxl"
    bold_title = "gs-c-promo-heading__title gel-paragon-bold gs-u-mt+ nw-o-link-split__text"
    bold_more_info = "gs-c-promo-summary gel-long-primer gs-u-mt nw-c-promo-summary"
    #This must be here for the big bold headline BBC likes to put on their website
    p_bold = data.find(class_=bold_container)
    p_bold_title = p_bold.find(class_=bold_title).text.strip() if p_bold.find(class_=bold_title) else ''
    p_bold_more_info = p_bold.find(class_=bold_more_info).text.strip() if p_bold.find(class_=bold_more_info) else ''
    p_date = dt.datetime.today()
    #Write bold headline and excerpt to file along with today's date
    Quill.write(p_bold_title,p_bold_more_info,p_date,site_name,fo)
    url = 'http://feeds.bbci.co.uk/news/world/rss.xml'
    parsed_url = fp.parse(url)
    x=0
    for entries in parsed_url:
        title = parsed_url.entries[x].title
        excerpt = parsed_url.entries[x].summary
        date = parsed_url.entries[x].published
        Quill.write(title,excerpt, date, site_name,fo)
        x+=1
    
def bbc_UK_RSS(fo):        #Pulls title, blurb and date BBC UK
    """ Pulls the bbc UK news """
    url = 'http://feeds.bbci.co.uk/news/uk/rss.xml#'
    site_nam = 'BBC - UK'
    parsed_url = fp.parse(url)
    #loading bar
    LoadBar.load_me(site_nam)
    #Write title to file
    Quill.title_write(site_nam,fo)
    x=0
    for entries in parsed_url:
        title = parsed_url.entries[x].title
        excerpt = parsed_url.entries[x].summary
        date = parsed_url.entries[x].published
        Quill.write(title,excerpt, date, site_nam,fo)
        x+=1

def alja_us_can(fo):        #Pulls title, blurb and date Al Jazeera US & Canada
    """ Pulls the Al Jazeera US and CAN news"""
    #Get url, parse into text
    url = 'https://www.aljazeera.com/us-canada/'
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    #Class name stand-ins (CSI)
    container_CSI = "gc__content"  #findall() makes a list, just use main container name
    title_CSI = "gc__title"
    excerpt_CSI = "gc__excerpt"
    time_CSI = "screen-reader-text"
    site_nam = 'Al Jazeera - US & Canada'
    #Write in title
    Quill.title_write(site_nam,fo)
    #Loading bar
    LoadBar.load_me(site_nam)
    # For loop through each container for title, time and who reported
    for tag in data.find_all(class_=container_CSI): #findall() makes a list, just use main container name
        # get title of article
        title = tag.find(class_=title_CSI).text.strip(
        ) if tag.find(class_=title_CSI) else 'No Headline Found!'
        # Get the short news excerpt
        more_info = tag.find(class_=excerpt_CSI).text.strip(
        ) if tag.find(
            class_=excerpt_CSI) else ''
        # Get Date article was written
        try:
            date = tag.find(class_=time_CSI).text.strip()
        except AttributeError:
            date = 'Al Jazeera - US & Canada'
        #write to file the date, title and excerpt
        Quill.write(title,more_info,date,site_nam,fo)

def alja_EU(fo):        #Pulls title, blurb and date Al Jazeera - EU
    """ Pulls the  Al Jazeera - EU"""
    #Get url, parse into text
    url = 'https://www.aljazeera.com/europe/'
    response = requests.get(url)
    site_nam = 'Al Jazeera - EU'
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    #Class name stand-ins (CSI)
    container_CSI = "gc__content"  #findall() makes a list, just use main container name
    title_CSI = "gc__title"
    excerpt_CSI = "gc__excerpt"
    time_CSI = "screen-reader-text"
    #Write in title
    Quill.title_write(site_nam,fo)
    #Loading bar
    LoadBar.load_me(site_nam)
    # For loop through each container for title, time and who reported
    for tag in data.find_all(class_=container_CSI): #findall() makes a list, just use main container name
        # get title of article
        title = tag.find(class_=title_CSI).text.strip(
        ) if tag.find(class_=title_CSI) else 'No Headline Found!'
        # Get the short news excerpt
        more_info = tag.find(class_=excerpt_CSI).text.strip(
        ) if tag.find(
            class_=excerpt_CSI) else ''
        # Get Date article was written
        try:
            date = tag.find(class_=time_CSI).text.strip()
        except AttributeError:
            date = 'Al Jazeera - EU'
        #write to file the date, title and excerpt
        Quill.write(title,more_info,date,site_nam,fo)

def alja_MidEast(fo):        #Pulls title, blurb and date Al Jazeera - Middle East
    """ Pulls the Al Jazeera - Middle East news """
    #Get url, parse into text
    url = 'https://www.aljazeera.com/middle-east/'
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    #Class name stand-ins (CSI)
    container_CSI = "gc__content"  #findall() makes a list, just use main container name
    title_CSI = "gc__title"
    excerpt_CSI = "gc__excerpt"
    time_CSI = "screen-reader-text"
    site_nam = 'Al Jazeera - Middle East'
    #Write in title
    Quill.title_write(site_nam,fo)
    #Loading bar
    LoadBar.load_me(site_nam)
    # For loop through each container for title, time and who reported
    for tag in data.find_all(class_=container_CSI): #findall() makes a list, just use main container name
        # get title of article
        title = tag.find(class_=title_CSI).text.strip(
        ) if tag.find(class_=title_CSI) else 'No Headline Found!'
        # Get the short news excerpt
        more_info = tag.find(class_=excerpt_CSI).text.strip(
        ) if tag.find(
            class_=excerpt_CSI) else ''
        # Get Date article was written
        try:
            date = tag.find(class_=time_CSI).text.strip()
        except AttributeError:
            date = 'Al Jazeera - Middle East'
        #write to file the date, title and excerpt
        Quill.write(title,more_info,date,site_nam,fo)

def alja_afr(fo):        #Pulls title, blurb and date Al Jazeera - Africa
    """ Pulls the Al Jazeera - Africa news"""
    #Get url, parse into text
    url = 'https://www.aljazeera.com/africa/'
    response = requests.get(url)
    site_nam = 'Al Jazeera - Africa'
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    #Class name stand-ins (CSI)
    container_CSI = "gc__content"  #findall() makes a list, just use main container name
    title_CSI = "gc__title"
    excerpt_CSI = "gc__excerpt"
    time_CSI = "screen-reader-text"
    #Write in title
    Quill.title_write(site_nam,fo)
    #Loading bar
    LoadBar.load_me(site_nam)
    # For loop through each container for title, time and who reported
    for tag in data.find_all(class_=container_CSI): #findall() makes a list, just use main container name
        # get title of article
        title = tag.find(class_=title_CSI).text.strip(
        ) if tag.find(class_=title_CSI) else 'No Headline Found!'
        # Get the short news excerpt
        more_info = tag.find(class_=excerpt_CSI).text.strip(
        ) if tag.find(
            class_=excerpt_CSI) else ''
        # Get Date article was written
        try:
            date = tag.find(class_=time_CSI).text.strip()
        except AttributeError:
            date = 'Al Jazeera - Africa'
        #write to file the date, title and excerpt
        Quill.write(title,more_info,date,site_nam,fo)

def alja_asia(fo):        #Pulls title, blurb and date Al Jazeera - Asia
    """ Pulls the Al Jazeera - Asia news"""
    #Get url, parse into text
    url = 'https://www.aljazeera.com/asia/'
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    #Class name stand-ins (CSI)
    container_CSI = "gc__content"  #findall() makes a list, just use main container name
    title_CSI = "gc__title"
    excerpt_CSI = "gc__excerpt"
    time_CSI = "screen-reader-text"
    site_nam = 'Al Jazeera - Asia'
    #Write in title
    Quill.title_write(site_nam,fo)
    #Loading bar
    LoadBar.load_me(site_nam)
    # For loop through each container for title, time and who reported
    for tag in data.find_all(class_=container_CSI): #findall() makes a list, just use main container name
        # get title of article
        title = tag.find(class_=title_CSI).text.strip(
        ) if tag.find(class_=title_CSI) else 'No Headline Found!'
        # Get the short news excerpt
        more_info = tag.find(class_=excerpt_CSI).text.strip(
        ) if tag.find(
            class_=excerpt_CSI) else ''
        # Get Date article was written
        try:
            date = tag.find(class_=time_CSI).text.strip()
        except AttributeError:
            date = 'Al Jazeera - Asia'
        #write to file the date, title and excerpt
        Quill.write(title,more_info,date,site_nam,fo)

def alja_AsPac(fo):        #Pulls title, blurb and date Al Jazeera - Asia-Pacific
   """ Pulls the Al Jazeera - Asia-Pacific news"""
   #Get url, parse into text
   url = 'https://www.aljazeera.com/asia-pacific/'
   response = requests.get(url)
   site_nam = 'Al Jazeera - Asia-Pacific'
   text = response.text
   data = BeautifulSoup(text, 'html.parser')
   #Class name stand-ins (CSI)
   container_CSI = "gc__content"  #findall() makes a list, just use main container name
   title_CSI = "gc__title"
   excerpt_CSI = "gc__excerpt"
   time_CSI = "screen-reader-text"
   #Write in title
   Quill.title_write(site_nam,fo)
   #Loading bar
   LoadBar.load_me(site_nam)
   # For loop through each container for title, time and who reported
   for tag in data.find_all(class_=container_CSI): #findall() makes a list, just use main container name
       # get title of article
       title = tag.find(class_=title_CSI).text.strip(
       ) if tag.find(class_=title_CSI) else 'No Headline Found!'
       # Get the short news excerpt
       more_info = tag.find(class_=excerpt_CSI).text.strip(
       ) if tag.find(
           class_=excerpt_CSI) else ''
       # Get Date article was written
       try:
           date = tag.find(class_=time_CSI).text.strip()
       except AttributeError:
           date = 'Al Jazeera - Asia-Pacific'
       #write to file the date, title and excerpt
       Quill.write(title,more_info,date,site_nam,fo)

def in_tod_IN(fo):        #Pulls title, blurb and date India Today - India
    """ Pulls the India Today - India news """
    #Get url, parse into text
    url = 'https://www.indiatoday.in/india'
    response = requests.get(url)
    time.sleep(.5)
    site_nam = 'India Today - India'
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    #Loading bar
    LoadBar.load_me(site_nam)
    #Write in title
    Quill.title_write(site_nam,fo)
    #Class name stand-ins (CSI)
    container_CSI = "detail"  #findall() makes a list, just use main container name
    # For loop through each container for title, time and who reported
    for tag in data.find_all(class_=container_CSI): #findall() makes a list, just use main container name
        # get title of article
        title = tag.find(class_="").text.strip(
            ) if tag.find(class_="") else ""
        more_info = tag.find(class_="").next_element.next_element.next_element.text.strip(
            ) if tag.find(class_="").next_element.next_element.next_element else ""
        date = f'pulled: {dt.date.today()}'
        #write to file the date, title and excerpt
        Quill.write(title,more_info,date,site_nam,fo)
       
def in_tod_BUS(fo):        #Pulls title, blurb and date India Today - Business
    """ Pulls the India Today - Business news """
    #Get url, parse into text
    url = 'https://www.indiatoday.in/business'
    response = requests.get(url)
    time.sleep(.5)
    site_nam = 'India Today - Business'
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    #Loading bar
    LoadBar.load_me(site_nam)
    #Write in title
    Quill.title_write(site_nam,fo)
    #Class name stand-ins (CSI)
    container_CSI = "detail"  #findall() makes a list, just use main container name
    # For loop through each container for title, time and who reported
    for tag in data.find_all(class_=container_CSI): #findall() makes a list, just use main container name
        # get title of article
        title = tag.find(class_="").text.strip(
            ) if tag.find(class_="") else ""
        more_info = tag.find(class_="").next_element.next_element.next_element.text.strip(
            ) if tag.find(class_="").next_element.next_element.next_element else ""
        date = f'pulled: {dt.date.today()}'
        #write to file the date, title and excerpt
        Quill.write(title,more_info,date,site_nam,fo)
    
def in_tod_WOR(fo):        #Pulls title, blurb and date India Today - World News
    """ Pulls the India Today - World News """
    #Get url, parse into text
    url = 'https://www.indiatoday.in/world'
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    #Class name stand-ins (CSI)
    container_CSI = "detail"  #findall() makes a list, just use main container name
    site_nam = 'India Today - World News'
    #Write in title
    Quill.title_write(site_nam,fo)
    #Loading bar
    LoadBar.load_me(site_nam)
    # For loop through each container for title, time and who reported
    for tag in data.find_all(class_=container_CSI): #findall() makes a list, just use main container name
        # get title of article
        title = tag.find(class_="").text.strip(
            ) if tag.find(class_="") else ""
        more_info = tag.find(class_="").next_element.next_element.next_element.text.strip(
            ) if tag.find(class_="").next_element.next_element.next_element else ""
        date = f'pulled: {dt.date.today()}'
        #write to file the date, title and excerpt
        Quill.write(title,more_info,date,site_nam,fo)
    
def nyt_US_RSS(fo):        #Pulls title, blurb and date NYT - US RSS feed
    """ Pulls the NYT - US news, uses RSS feed due to the volatile nature of the headline elements within
    the main website"""
    #Get url, parse RSS feed
    url = 'https://rss.nytimes.com/services/xml/rss/nyt/US.xml'
    parsed_url = fp.parse(url)
    site_nam = "NYT - US RSS feed"
    #Loading bar
    LoadBar.load_me(site_nam)
    #Write in title
    Quill.title_write(site_nam,fo)
    #Pull the headline and blurb from RSS site
    x=0
    for entries in parsed_url:
        title = parsed_url.entries[x].title
        excerpt = parsed_url.entries[x].summary
        date = parsed_url.entries[x].published
        Quill.write(title,excerpt, date, site_nam,fo)
        x+=1
    
def nyt_WOR_RSS(fo):        #Pulls title, blurb and date NYT - WORLD RSS feed
    """ Pulls the NYT - WORLD news """
    #Get url, parse into text
    url = 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml'
    site_nam = 'NYT - WORLD'
    parsed_url = fp.parse(url)
    #Loading bar
    LoadBar.load_me(site_nam)
    #Write title to file
    Quill.title_write(site_nam,fo)
    x=0
    for entries in parsed_url:
        title = parsed_url.entries[x].title
        excerpt = parsed_url.entries[x].summary
        date = parsed_url.entries[x].published
        Quill.write(title,excerpt, date, site_nam,fo)
        x+=1
    
def nyt_TEC_RSS(fo):        #Pulls title, blurb and date NYT - TECH RSS feed
    """ Pulls the NYT - TECH news """
    #Get url, parse into text
    url = 'https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml'
    site_nam = 'NYT - TECH'
    parsed_url = fp.parse(url)
    #Write in title
    Quill.title_write(site_nam,fo)
    #Loading bar
    LoadBar.load_me(site_nam)
    x=0
    for entries in parsed_url:
        title = parsed_url.entries[x].title
        excerpt = parsed_url.entries[x].summary
        date = parsed_url.entries[x].published
        Quill.write(title,excerpt, date, site_nam,fo)
        x+=1
   
def nyt_USPol_RSS(fo):        #Pulls title, blurb and date NYT - Politics RSS feed
    """ Pulls the NYT - Politics news"""
    #Get url, parse into text
    url = 'https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml'
    parsed_url = fp.parse(url)
    site_nam = 'NYT - POLITICS'
    #Write in title
    Quill.title_write(site_nam,fo)
    #Loading bar
    LoadBar.load_me(site_nam)
    x=0
    for entries in parsed_url:
        title = parsed_url.entries[x].title
        excerpt = parsed_url.entries[x].summary
        date = parsed_url.entries[x].published
        Quill.write(title,excerpt, date, site_nam,fo)
        x+=1

def espn_top_rss(fo):        #Pulls title, blurb and date ESPN - TOP, RSS feed
    """this pulls the ESPN - TOP news RSS feed """
    # Get url, parse into text
    url = 'https://www.espn.com/espn/rss/news'
    site_nam = 'ESPN - TOP, RSS'
    parsed_url = fp.parse(url)
    # Write in title
    Quill.title_write(site_nam,fo)
    # Loading bar
    LoadBar.load_me(site_nam)
    # For loop through each container for title, time and who reported
    x=0
    for entries in parsed_url:
        title = parsed_url.entries[x].title
        excerpt = parsed_url.entries[x].summary
        date = parsed_url.entries[x].published
        Quill.write(title,excerpt, date, site_nam,fo)
        x+=1
    
def espn_NFL_rss(fo):        #Pulls title, blurb and date ESPN - NFL, RSS feed
    """this pulls the ESPN - NFL, RSS feed """
    # Get url, parse into text
    url = 'https://www.espn.com/espn/rss/nfl/news'
    site_nam = 'ESPN - NFL, RSS'
    parsed_url = fp.parse(url)
    # Write in title
    Quill.title_write(site_nam,fo)
    # Loading bar
    LoadBar.load_me(site_nam)
        
    # For loop through each container for title, time and who reported
    x=0
    for entries in parsed_url:
        title = parsed_url.entries[x].title
        excerpt = parsed_url.entries[x].summary
        date = parsed_url.entries[x].published
        Quill.write(title,excerpt, date, site_nam,fo)
        x+=1

def espn_NBA_rss(fo):        #Pulls title, blurb and date ESPN - NBA, RSS feed
    """this pulls the ESPN - NBA, RSS feed """
    # Get url, parse into text
    url = 'https://www.espn.com/espn/rss/nba/news'
    site_nam = 'ESPN - NBA, RSS'
    parsed_url = fp.parse(url)
    # Write in title
    Quill.title_write(site_nam,fo)
    # Loading bar
    LoadBar.load_me(site_nam)
    # For loop through each container for title, time and who reported
    x=0
    for entries in parsed_url:
        title = parsed_url.entries[x].title
        excerpt = parsed_url.entries[x].summary
        date = parsed_url.entries[x].published
        Quill.write(title,excerpt, date, site_nam,fo)
        x+=1

def espn_MLB_rss(fo):        #Pulls title, blurb and date ESPN - MLB, RSS feed
    """this pulls the ESPN - MLB, RSS feed """
    # Get url, parse into text
    url = 'https://www.espn.com/espn/rss/mlb/news'
    site_nam = 'ESPN - MLB, RSS'
    parsed_url = fp.parse(url)
    # Write in title
    Quill.title_write(site_nam,fo)
    # Loading bar
    LoadBar.load_me(site_nam)
    # For loop through each container for title, time and who reported
    x=0
    for entries in parsed_url:
        title = parsed_url.entries[x].title
        excerpt = parsed_url.entries[x].summary
        date = parsed_url.entries[x].published
        Quill.write(title,excerpt, date, site_nam,fo)
        x+=1
    
def espn_NHL_rss(fo):        #Pulls title, blurb and date ESPN - NHL, RSS feed
    """this pulls the ESPN - NHL, RSS feed """
    # Get url, parse into text
    url = 'https://www.espn.com/espn/rss/mlb/news'
    site_nam = 'ESPN - NHL, RSS'
    parsed_url = fp.parse(url)
    # Write in title
    Quill.title_write(site_nam,fo)
    # Loading bar
    LoadBar.load_me(site_nam)
    # For loop through each container for title, time and who reported
    x=0
    for entries in parsed_url:
        title = parsed_url.entries[x].title
        excerpt = parsed_url.entries[x].summary
        date = parsed_url.entries[x].published
        Quill.write(title,excerpt, date, site_nam,fo)
        x+=1
    
def espn_u_rss(fo):        #Pulls title, blurb and date ESPNU, RSS feed
    """this pulls the ESPNU, RSS feed """
    # Get url, parse into text
    url = 'https://www.espn.com/espn/rss/espnu/news'
    site_nam = 'ESPNU, RSS'
    parsed_url = fp.parse(url)
    # Write in title
    Quill.title_write(site_nam,fo)
    # Loading bar
    LoadBar.load_me(site_nam)
    # For loop through each container for title, time and who reported
    x=0
    for entries in parsed_url:
        title = parsed_url.entries[x].title
        excerpt = parsed_url.entries[x].summary
        date = parsed_url.entries[x].published
        Quill.write(title,excerpt, date, site_nam,fo)
        x+=1
    
def espn_ncb_rss(fo):        #Pulls title, blurb and date ESPN - National College Basketball, RSS feed
    """this pulls the ESPN - National College Basketball, RSS feed """
    # Get url, parse into text
    url = 'https://www.espn.com/espn/rss/ncb/news'
    site_nam = 'ESPN - College Basketball, RSS'
    parsed_url = fp.parse(url)
    # Write in title
    Quill.title_write(site_nam,fo)
    # Loading bar
    LoadBar.load_me(site_nam)
    # For loop through each container for title, time and who reported
    x=0
    for entries in parsed_url:
        title = parsed_url.entries[x].title
        excerpt = parsed_url.entries[x].summary
        date = parsed_url.entries[x].published
        Quill.write(title,excerpt, date, site_nam,fo)
        x+=1

def espn_ncf_rss(fo):        #Pulls title, blurb and date ESPN - National College Football, RSS feed
    """this pulls the ESPN - National College Football, RSS feed """
    # Get url, parse into text
    url = 'https://www.espn.com/espn/rss/ncf/news'
    site_nam = 'ESPN - College Football, RSS'
    parsed_url = fp.parse(url)
    # Write in title
    Quill.title_write(site_nam,fo)
    # Loading bar
    LoadBar.load_me(site_nam)
    # For loop through each container for title, time and who reported
    x=0
    for entries in parsed_url:
        title = parsed_url.entries[x].title
        excerpt = parsed_url.entries[x].summary
        date = parsed_url.entries[x].published
        Quill.write(title,excerpt, date, site_nam,fo)
        x+=1
    

def active_FXN(fo): #This is just to make main() more readable
    bbc_UK_RSS(fo)
    bbc_WOR_RSS(fo)
    epoch_latest(fo)
    epoch_US(fo)
    epoch_USPol(fo)
    epoch_World(fo)
    alja_us_can(fo)
    alja_EU(fo)
    alja_MidEast(fo)
    alja_afr(fo)
    alja_asia(fo)
    alja_AsPac(fo)
    in_tod_IN(fo)
    in_tod_BUS(fo)
    in_tod_WOR(fo)
    nyt_WOR_RSS(fo)
    nyt_TEC_RSS(fo)
    nyt_USPol_RSS(fo)
    nyt_US_RSS(fo)
    espn_top_rss(fo)
    espn_NFL_rss(fo)
    espn_NBA_rss(fo)
    espn_MLB_rss(fo)    
    espn_NHL_rss(fo)
    espn_u_rss(fo)
    espn_ncb_rss(fo)
    espn_ncf_rss(fo)
    

# -----main-----
def main():
    #getting path to make news folder
    cwd_parent = Path.cwd().parent
    fo_file = f'{str(cwd_parent)}/news/{str(dt.date.today())}.txt'
    fo_news = str(cwd_parent)+"/news"
    #Try catch to stop the error if the directory isn't found
    try:
        fo = open(fo_file, "w")
        print(f'News at: {fo_news}')
    except:
        os.mkdir(fo_news)
        fo = open(fo_file, "w")
        print(f'News at: {fo_news}')
        #Pass in "fo" to FXN or Quill.<function>() won't work
    active_FXN(fo)
    
    #os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print(f'News fetched and located at: {fo_news}')

    
# ___RUNNING PARTS___
main()

#       <other NOTE space>
#
#
#
#
