#       <ArgusEyes, webscraper for news stories, v0.14,Working,EffortlessTurtle>
########################################################################
#       <TODO>
# -finish other methods to scrape other sites
# -print all to a txt doc for user review
# -eventually to be hosted and then emails? result every 2 hours to a special account
# -Eventually output to css
# -Figure out multithreading
# -make different sections write to separate files at same time using multi-threading.
# -
#  
#########################################################################


# imports
import site
import requests
import progressbar
from bs4 import BeautifulSoup
import datetime as dt
from dateutil import parser
from pathlib import Path
import os
import time


# Classes
# May need to build a couple more
class Quill: #For the write to file section of a FXN
    """very simple, for efficiency and readability"""
    
    def __init__(self, tit_CSI, exer_CSI, dat_CSI, file_fo):
        self.title = tit_CSI
        self.ex = exer_CSI
        self.date = dat_CSI
        self.fo = file_fo    
    
    def write(title, ex, date,site_nam, fo): #Writes this to the file from main()
        fo.write(str(date) + "\n\n")
        fo.write(title + "\n")
        fo.write("\n")
        fo.write(ex)
        fo.write('\nfrom: '+ site_nam + "\n" + 140 * '-'+"\n")
        
        
    def title_write(name,fo): #Writes the of the title of site with different format to file. 
        name = str(name) + '\n\n'
        fo.write(15 * ' ' + name + '-- Date Pulled: ' + str(dt.date.today()) + "\n")
        fo.write(140 * "^" + '\n\n')
        
    #This part of the class will eventually be used to generate a pretty output
    def csv_file_prep(fo):
        fo.write('DATE' + "," + "HEADLINE" + "," + "EXCERPT" + "\n")
        
    def csv_tit_write(name, fo):
        date = dt.date.today()
        fo.write('\nPulled:' + str(date) + "," + name + ", " + "\n")
        
    def csv_write(title, excerpt, date,fo):
        fo.write(str(date) + "," + title + "," + excerpt)
#Globals

#Must pass in 'fo' for the Quill class to work
def epoch_US(fo):  # Pulls title, blurb and date written for Epoch US
    """This is the logic to pull headlines.
    TODO:
    -write to a txt document 
    """
    #Get text from website
    url = 'https://www.theepochtimes.com/c-us'
    site_nam = '__The Epoch Times - US News__'
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    
    #Write site name to fo
    Quill.title_write(site_nam,fo)
    
    #Loading bar
    widgets = ['Fetching Epoch - US: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    i = 0
    for i in range(50):
        time.sleep(0.1)
        bar.update(i)
    
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
            bar.update(1)
        #Readies the url to request next page    
        url = f"https://www.theepochtimes.com/c-us/" + str(x)
    #Let user know it's finished with this section    
    print("\n"+'Epoch - US: fetched')
        
def epoch_latest(fo):  # Pulls title, blurb and date written for Epoch latest
    """This is the logic to pull headlines.    """
    
    url = 'https://www.theepochtimes.com/latest/'
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    
    site_nam = 'Epoch - Latest'
    #Write site name to 'fo'
    Quill.title_write(site_nam,fo)
    
    #loading bar
    widgets = ['Fetching Epoch - Latest: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    i = 0
    for i in range(50):
        time.sleep(0.1)
        bar.update(i)
    
  
    #Gets first 3 pages
    for x in range(2, 3):
        response = requests.get(url)  # -MARK NOTE: marked must stay here, otherwise you never request the next page's content from website
        text = response.text
        data = BeautifulSoup(text, 'html.parser')  # -MARK
        
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
        
    print(("\n"+'Epoch - Latest: fetched'))
    
def epoch_USPol(fo):  # Pulls title, blurb and date written for Epoch latest
    """This is the logic to pull headlines.    """
    
    url = 'https://www.theepochtimes.com/c-us-politics'
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    
    site_nam = "Epoch Times - US Politics"
    
    #Write site name to file 'fo'
    Quill.title_write(site_nam,fo)
    
    #loading bar
    widgets = ['Fetching Epoch - US Politics: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    i =0
    for i in range(50):
        time.sleep(0.1)
        bar.update(i)
    
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
        #print(date2)
        #print(dt.date.today())
        if date2 != dt.date.today():  # counter to
            
            Quill.write(title,more_info,date,site_nam,fo)
            i += 1
        else:

            #print(' <- i, epoch_latest();else, inside epoch_latest')
            Quill.write(title,more_info,date,fo)
    print(("\n"+'Epoch - US Politics: fetched'))    
    
def epoch_World(fo):        #Pulls title, blurb and date - Epoch - World
    """this pulls the Epoch world news
    ++++
   
    """
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
    widgets = ['Fetching Epoch - World: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    i =0
    for i in range(50):
        time.sleep(0.1)
        bar.update(i)
    
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
        
    print("\nEpoch - World: fetched")   

def bbc_WOR(fo):        #Pulls title, blurb and date - BBC world
    """this pulls the bbc world news
    ++++
    NOTE:
    -this one has very long class names. and is the template of many of its contemporaries.
    """
    #Define url, and parse this into text
    url = 'https://www.bbc.com/news/world'
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    
    #Stand ins used for obvious reasons
    site_name = "BBC - WORLD"
    container_class_stand_in = "gs-c-promo-body gs-u-mt@xxs gs-u-mt@m gs-c-promo-body--flex gs-u-mt@xs gs-u-mt0@xs gs-u-mt@m gel-1/2@xs gel-1/1@s"
    title_class_stand_in = "gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text"
    excerpt_class_stand_in = "gs-c-promo-summary gel-long-primer gs-u-mt nw-c-promo-summary gs-u-display-none gs-u-display-block@m"
    time_class_stand_in = "gs-o-bullet__text date qa-status-date"
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
    
    #Write site name to file
    Quill.title_write(site_name,fo)
   
    #Loading bar
    widgets = ['Fetching BBC - World: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    i =0
    for i in range(50):
        time.sleep(0.1)
        bar.update(i)
    
    # For loop through each container for title, time and who reported
    for tag in data.find_all(class_=container_class_stand_in):

        # get title of article
        title = tag.find(class_=title_class_stand_in).text.strip(
        ) if tag.find(class_=title_class_stand_in) else ''
        
        # Get the short news excerpt
        more_info = tag.find(class_=excerpt_class_stand_in).text.strip(
        ) if tag.find(
            class_=excerpt_class_stand_in) else 'BBC - World'
        
        # Get Date article was written
        try:
            date = tag.find(class_=time_class_stand_in).datetime.text.strip()
        except AttributeError:
            date = ''
            
        #write to file section
        Quill.write(title,more_info,date,site_name,fo)
    #Let user know That it's finished    
    print("\nBBC - World: fetched")   
    
def bbc_UK(fo):        #Pulls title, blurb and date - BBC UK
    """this pulls the bbc UK news
    ++++
    NOTE:
    -this one has very long class names. and is the template of many of its contemporaries.
    """
    url = 'https://www.bbc.com/news/uk'
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    
    #Stand-ins used for obvious reasons
    container_class_stand_in = "gs-c-promo gs-t-News nw-c-promo gs-o-faux-block-link gs-u-pb gs-u-pb+@m nw-p-default gs-c-promo--inline gs-c-promo--stacked@m gs-c-promo--flex"
    title_class_stand_in = "gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text"
    excerpt_class_stand_in = "gs-c-promo-summary gel-long-primer gs-u-mt nw-c-promo-summary gs-u-display-none gs-u-display-block@m"
    time_class_stand_in = "gs-o-bullet__text date qa-status-date"
    site_nam = 'BBC - UK'
    bold_container = "gs-c-promo gs-t-News nw-c-promo gs-o-faux-block-link gs-u-pb gs-u-pb+@m nw-p-default gs-c-promo--inline@m gs-c-promo--stacked@xxl gs-c-promo--flex"
    bold_title = "gs-c-promo-heading__title gel-paragon-bold gs-u-mt+ nw-o-link-split__text"
    bold_more_info = "gs-c-promo-summary gel-long-primer gs-u-mt nw-c-promo-summary"
    
    #To pull the big headline from BBC - UK site
    p_bold = data.find(class_=bold_container)
    p_bold_title = p_bold.find(class_=bold_title).text.strip() if p_bold.find(class_=bold_title) else ''
    p_bold_more_info = p_bold.find(class_=bold_more_info).text.strip() if p_bold.find(class_=bold_more_info) else ''
    p_date = dt.datetime.today()
    
    #Write site name to document
    Quill.title_write(site_nam,fo)
    
    #Write big headline from BBC - UK
    Quill.write(p_bold_title,p_bold_more_info,p_date,site_nam,fo)    
    #loading bar
    widgets = ['Fetching BBC - UK: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    i =0
    for i in range(50):
        time.sleep(0.1)
        bar.update(i)
    
    # For loop through each container for title, time and who reported
    for tag in data.find_all(class_=container_class_stand_in):

        # get title of article
        title = tag.find(class_=title_class_stand_in).text.strip(
        ) if tag.find(class_=title_class_stand_in) else ''
        
        # Get the short news excerpt
        more_info = tag.find(class_=excerpt_class_stand_in).text.strip(
        ) if tag.find(
            class_=excerpt_class_stand_in) else 'BBC - UK'
        
        # Get Date article was written
        try:
            date = tag.find(class_=time_class_stand_in).datetime.text()
        except AttributeError:
            date = ''
        #write to file
        Quill.write(title,more_info,date,site_nam,fo)
    print("\nBBC - UK: fetched")   

def alja_us_can(fo):        #Pulls title, blurb and date - Al Jazeera US & Canada
    """this pulls the Al Jazeera US and CAN news"""

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
    widgets = ['fetching Al Jazeera - US & Canada: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    i =0
    for i in range(50):
        time.sleep(0.1)
        bar.update(i)
    
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
    print("\nAl Jazeera - US & Canada: fetched")  
 
def alja_EU(fo):        #Pulls title, blurb and date - Al Jazeera - EU
    """this pulls the  Al Jazeera - EU"""
    
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
    widgets = ['Fetching Al Jazeera - EU: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    i =0
    for i in range(50):
        time.sleep(0.1)
        bar.update(i)
    
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
    print("\nAl Jazeera - EU: fetched")   

def alja_MidEast(fo):        #Pulls title, blurb and date - Al Jazeera - Middle East
    """this pulls the Al Jazeera - Middle East news """
    
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
    widgets = ['Fetching Al Jazeera - Middle East: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    i =0
    for i in range(50):
        time.sleep(0.1)
        bar.update(i)
    
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
    print("\nAl Jazeera - Middle East: fetched")   

def alja_afr(fo):        #Pulls title, blurb and date - Al Jazeera - Africa
    """this pulls the Al Jazeera - Africa news"""
    
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
    widgets = ['Fetching Al Jazeera - Africa: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    i =0
    for i in range(50):
        time.sleep(0.1)
        bar.update(i)
    
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
    print("\nAl Jazeera - Africa: fetched")

def alja_asia(fo):        #Pulls title, blurb and date - Al Jazeera - Asia
    """this pulls the Al Jazeera - Asia news"""
    
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
    widgets = ['Fetching Al Jazeera - Asia: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    i =0
    for i in range(50):
        time.sleep(0.1)
        bar.update(i)
        
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
    print("\nAl Jazeera - Asia: fetched")

def alja_AsPac(fo):        #Pulls title, blurb and date - Al Jazeera - Asia-Pacific
   """this pulls the Al Jazeera - Asia-Pacific news"""
   
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
   widgets = ['Fetching Al Jazeera - Asia-Pacific: ', progressbar.AnimatedMarker()]
   bar = progressbar.ProgressBar(widgets=widgets).start()
   i =0
   for i in range(50):
        time.sleep(0.1)
        bar.update(i)
        
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
       
   print("\nAl Jazeera - Asia-Pacific: fetched")   
     
def india_today_IN(fo):        #Pulls title, blurb and date -India Today - India
    """this pulls the India Today - India news
    ++++
    This one is different from those before
    """
    
    #Get url, parse into text
    url = 'https://www.indiatoday.in/india'
    response = requests.get(url)
    time.sleep(.5)
    site_nam = 'India Today - India'
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    
    #Loading bar
    widgets = ['Fetching India Today - India: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    i =0
    for i in range(50):
        time.sleep(0.1)
        bar.update(i)
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
    print("\nIndia Today - India: fetched")       
    
def india_today_BUS(fo):        #Pulls title, blurb and date -India Today - Business
    """this pulls the India Today - Business news
    ++++
    This one is different from those before
    """
    
    #Get url, parse into text
    url = 'https://www.indiatoday.in/business'
    response = requests.get(url)
    time.sleep(.5)
    site_nam = 'India Today - Business'
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    
    #Loading bar
    widgets = ['Fetching India Today - Business: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    i =0
    for i in range(50):
        time.sleep(0.1)
        bar.update(i)
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
       # bar.update(i)
    print("\nIndia Today - Business: fetched")
    
def india_today_WOR(fo):        #Pulls title, blurb and date -India Today - World News
    """this pulls the India Today - World News
    ++++
    This one is different from those before
    """
    
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
    widgets = ['Fetching India Today - World News: ',progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    i = 0
    for i in range(50):
        time.sleep(0.1)
        bar.update(i)
    
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
       # bar.update(i)
    print("\nIndia Today - World News: fetched")
    
def nyt_US(fo):        #Pulls title, blurb and date - NYT - US
    """this pulls the NYT - US news
    ++++
    NOTE:
    -this one has very long class names. and is the template of many of its contemporaries.
    """
    
    
    #Get url, parse into text
    url = 'https://www.nytimes.com/section/us'
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    
    #Class name stand-ins (CSI)
    container_CSI = "css-ye6x8s"  #findall() makes a list, just use main container name
    title_CSI = "css-1j9dxys e15t083i0"
    excerpt_CSI = "css-1echdzn e15t083i1"
    time_CSI = "todays-date"
    site_nam = 'NYT - US'
    
    #Write in title
    Quill.title_write(site_nam,fo)
    #Pull Big headline
    bold_container = "css-xbztij"
    bold_title = "css-6i5eci ef62v182"
    bold_more_info = "css-1jhf0lz ef62v180"
    p_bold = data.find(class_=bold_container)
    p_bold_title = p_bold.find(class_=bold_title).text.strip() if p_bold.find(class_=bold_title) else ''
    p_bold_more_info = p_bold.find(class_=bold_more_info).text.strip() if p_bold.find(class_=bold_more_info) else ''
    date = f'Pulled: {dt.date.today()}'
    
    #Write Big headline to file with excerpt and Now()
    Quill.write(p_bold_title, p_bold_more_info, date,site_nam, fo)
    
    #Loading bar
    widgets = ['Fetching NYT - US: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    i = 0
    for i in range(50):
        time.sleep(0.1)
        bar.update(i)
        
    #for the smaller headline on the NYT sites
    bold_container = "css-11p8dg8"
    bold_title = "css-6i5eci ef62v183"
    bold_more_info = "css-4hrlf7 ef62v181"
    
    for tag in data.find(class_=bold_container):
        # get title of article
        title = tag.find(class_=bold_title).text.strip(
        ) if tag.find(class_=bold_title) else 'No Headline Found!'
        
        # Get the short news excerpt
        more_info = tag.find(class_=bold_more_info).text.strip(
        ) if tag.find(
            class_=bold_more_info) else ''
        
        # Get Date article was written
        try:
            date = tag.find(class_=time_CSI).datetime.text.strip()
        except AttributeError:
            date = f'Pulled: {dt.date.today()}'
            
        #write to file the date, title and excerpt
        Quill.write(title,more_info,date,site_nam,fo)

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
            date = tag.find(class_=time_CSI).datetime.text.strip()
        except AttributeError:
            date = f'from NYT - US {dt.date.today()}'
            
        #write to file the date, title and excerpt
        Quill.write(title,more_info,date,site_nam,fo)
    print("\nNYT - US: fetched")   
    
def nyt_WOR(fo):        #Pulls title, blurb and date - NYT - WORLD
    """this pulls the NYT - WORLD news
    ++++
    NOTE:
    -this one has very long class names. and is the template of many of its contemporaries.
    """
    
    
    #Get url, parse into text
    url = 'https://www.nytimes.com/section/world'
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    
    #Class name stand-ins (CSI)
    container_CSI = "css-1l4spti"  #findall() makes a list, just use main container name
    title_CSI = "css-1j9dxys e15t083i0"
    excerpt_CSI = "css-1echdzn e15t083i1"
    time_CSI = "todays-date"
    site_nam = 'NYT - WORLD'
    
    #Write in title
    Quill.title_write(site_nam,fo)

    #Loading bar
    widgets = ['Fetching NYT - WORLD: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    i = 0
    for i in range(50):
        time.sleep(0.1)
        bar.update(i)
        
    #for the smaller headline on the NYT sites
    bold_container = "css-10wtrbd"
    bold_title = "css-byk1jx e1hr934v1"
    bold_more_info = "css-tskdi9 e1hr934v4"
    
    #For top 3 stories on site
    for tag in data.find_all(class_=bold_container):
        # get title of article
        title = tag.find('h2', class_= bold_title).text.strip(
            ) if tag.find('h2', class_= bold_title) else 'No Headline NYT - World'
        more_info = tag.find('p', class_ =bold_more_info).text.strip(
            ) if tag.find('p', class_ =bold_more_info) else 'No excerpt'
        #This is here for the top 4 big headlines, this logic keeps out unwanted crap
        if title == 'No Headline NYT - World' and more_info == 'No excerpt':
            break
        date = f'Pulled: {dt.date.today()}'
        
        #Write to file
        Quill.write(title,more_info,date,site_nam,fo)
        
    # For loop through each container for title, time and who reported from list at bottom of site
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
            date = tag.find(class_=time_CSI).datetime.text.strip()
        except AttributeError:
            date = f'from NYT - WORLD {dt.date.today()}'
            
        #write to file the date, title and excerpt
        Quill.write(title,more_info,date,site_nam,fo)
    print("\nNYT - WORLD: fetched")   
    
def active_FXN(fo,fo_news): #This is just to make main() more readable
    bbc_UK(fo)
    bbc_WOR(fo)
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
    india_today_IN(fo)
    india_today_BUS(fo)
    india_today_WOR(fo)
    nyt_US(fo)
    nyt_WOR(fo)
    
    #Helps user find file
    print()
    print(f'\nNews fetched and located at: {fo_news}') 

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
    active_FXN(fo,fo_news)
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print(f'News fetched and located at: {fo_news}')

    
# ___RUNNING PARTS___
main()

#       <other NOTE space>
#
#
#
#
