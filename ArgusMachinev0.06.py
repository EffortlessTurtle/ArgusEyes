#       <ArgusMachine, webscraper for news stories, v0.06,Github,EffortlessTurtle>
########################################################################
#       <TODO>
# -finish other methods to scrape other sites
# -print all to a txt doc for user review
# -eventually to be hosted and then emails? result every 2 hours to a special account
# -Design classes to make code more efficient
# 
#
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


# Classes
# May need to build a couple more
class Quill: #For the write to file section of a FXN
    """very simple, for efficiency and readability"""
    
    def __init__(self, tit_CSI, exer_CSI, dat_CSI, file_fo):
        self.title = tit_CSI
        self.ex = exer_CSI
        self.date = dat_CSI
        self.fo = file_fo
        
    
    def write(title, ex, date, fo): #Writes this to the file from main()
        fo.write(str(date) + "\n")
        fo.write(title + "\n")
        fo.write(ex + "\n" + 140 * '-'+"\n")
        fo.write('\n')
        
    def title_write(name,fo): #Writes the of the title of site with different format to file. 
        name = str(name) + '\n\n'
        fo.write(15 * ' ' + name)
        fo.write(140 * "^" + '\n\n')

#Globals


#Must pass in 'fo' for the Quill class to work
def epoch_US(fo):  # Pulls title, blurb and date written for Epoch US
    """This is the logic to pull headlines.
    TODO:
    -write to a txt document 
    """
    url = 'https://www.theepochtimes.com/c-us'
    site_nam = '__The Epoch Times - US News__'
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    widgets = ['Fetching Epoch - US: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    Quill.title_write(site_nam,fo)
    #Begin collecting news stories
    for x in range(2, 6):
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
            Quill.write(title,more_info,date,fo)
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
    widgets = ['Fetching Epoch - Latest: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    i = 0
    fo.write(15 * ' ' + '__The Epoch Times - Latest News__\n\n')
    fo.write(140 * "^" + '\n\n')
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
                fo.write(str(date) + "\n")
                fo.write(title + "\n")
                fo.write("\n")
                fo.write(more_info + "\n" + 140 * '-'+"\n")
                fo.write('\n')
                bar.update(1)
                i += 1
            else:

                fo.write(str(date) + "\n")
                fo.write(title + "\n")
                fo.write("\n")
                fo.write(more_info + "\n" + 140 * '-'+"\n")
                fo.write('\n')
                bar.update(1)
            
        if i >= 29: #this is an emergency to kill any accidental race-condition
            print(str(i) + ' <- emergency break, EPOCH - LATEST')
            i = 0
            continue  #This break kicks from x in (2,12) for loop
        elif i >100:
            break
        url = f"https://www.theepochtimes.com/latest/" + str(x)
        
    print(("\n"+'Epoch - Latest: fetched'))
    
def epoch_USPol(fo):  # Pulls title, blurb and date written for Epoch latest
    """This is the logic to pull headlines.    """
    
    url = 'https://www.theepochtimes.com/c-us-politics'
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    widgets = ['Fetching Epoch - US Politics: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()

    i = 0
    fo.write(15 * ' ' + '__The Epoch Times - US Politics__\n\n')
    fo.write(140 * "^" + '\n\n')

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
            
            #print(' <- inside if, date2; i, epoch_latest()')
            fo.write(str(date) + "\n")
            fo.write(title + "\n")
            fo.write("\n")
            fo.write(more_info + "\n" + 140 * '-'+"\n")
            fo.write('\n')
            bar.update(1)
            i += 1
        else:

            #print(' <- i, epoch_latest();else, inside epoch_latest')
            fo.write(str(date) + "\n")
            fo.write(title + "\n")
            fo.write("\n")
            fo.write(more_info + "\n" + 140 * '-'+"\n")
            fo.write('\n')
            bar.update(1)
        
        if i >= 29: #this is an emergency to kill any accidental race-condition
            print(str(i) + ' <- emergency break, epoch_USPol')
            i = 0
            break  #This break kicks from x in (2,12) for loop
        elif i >100:
            break
    print(("\n"+'Epoch - US Politics: fetched'))    
    
def epoch_World(fo):        #Pulls title, blurb and date - Epoch - World
    """this pulls the Epoch world news
    ++++
   
    """
    url = 'https://www.theepochtimes.com/c-world'
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    widgets = ['Fetching Epoch - World: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    fo.write(15 * ' ' + '__ Epoch - World __\n\n')
    fo.write(140 * "^" + '\n\n')
    container_class_stand_in = "post_list"
    title_class_stand_in = "title"
    excerpt_class_stand_in = "excerpt more_info"
    time_class_stand_in = "time"
    response = requests.get(url)  # -MARK
    text = response.text
    data = BeautifulSoup(text, 'html.parser')  # -MARK
    
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
        fo.write(str(date) + "\n")
        fo.write(title + "\n")
        fo.write("\n")
        fo.write(more_info + "\n" + 140 * '-'+"\n")
        fo.write('\n')
        bar.update(1)
        
    print("\nEpoch - World: fetched")   

def BBC_World(fo):        #Pulls title, blurb and date - BBC world
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
    #Loading bar
    widgets = ['Fetching BBC - World: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    
    #Write title to document
    fo.write(15 * ' ' + '__ BBC - WORLD __\n\n')
    fo.write(140 * "^" + '\n\n')
    
    container_class_stand_in = "gs-c-promo-body gs-u-mt@xxs gs-u-mt@m gs-c-promo-body--flex gs-u-mt@xs gs-u-mt0@xs gs-u-mt@m gel-1/2@xs gel-1/1@s"
    title_class_stand_in = "gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text"
    excerpt_class_stand_in = "gs-c-promo-summary gel-long-primer gs-u-mt nw-c-promo-summary gs-u-display-none gs-u-display-block@m"
    time_class_stand_in = "gs-o-bullet__text date qa-status-date"
    
    #This must be here for the big bold headline BBC likes to put on their website
    bold_container = "gs-c-promo-body gs-u-mt@xxs gs-u-mt@m gs-c-promo-body--primary gs-u-mt@xs gs-u-mt@s gs-u-mt@m gs-u-mt@xl gel-1/3@m gel-1/2@xl gel-1/1@xxl"
    bold_title = "gs-c-promo-heading__title gel-paragon-bold gs-u-mt+ nw-o-link-split__text"
    bold_more_info = "gs-c-promo-summary gel-long-primer gs-u-mt nw-c-promo-summary"
    p_bold = data.find(class_=bold_container)
    p_bold_title = p_bold.find(class_=bold_title).text.strip() if p_bold.find(class_=bold_title) else ''
    p_bold_more_info = p_bold.find(class_=bold_more_info).text.strip() if p_bold.find(class_=bold_more_info) else ''
    #Write bold headline and excerpt to file along with today's date
    fo.write(str(dt.datetime.now()) + '\n')
    fo.write(str(p_bold_title) + '\n')
    fo.write('\n')
    fo.write(str(p_bold_more_info) + '\n' + 140 * '-' + '\n' + '\n')
    bar.update(1)
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
        fo.write(str(date) + "\n")
        fo.write(title + "\n")
        fo.write("\n")
        fo.write(more_info + "\n" + 140 * '-'+"\n")
        fo.write('\n')
        bar.update(1)
    #Let user know That it's finished    
    print("\nBBC - World: fetched")   
    
def BBC_UK(fo):        #Pulls title, blurb and date - BBC UK
    """this pulls the bbc UK news
    ++++
    NOTE:
    -this one has very long class names. and is the template of many of its contemporaries.
    """
    url = 'https://www.bbc.com/news/uk'
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')
    widgets = ['Fetching BBC - UK: ', progressbar.AnimatedMarker()]
    bar = progressbar.ProgressBar(widgets=widgets).start()
    fo.write(15 * ' ' + '__ BBC - UK __\n\n')
    fo.write(140 * "^" + '\n\n')
    container_class_stand_in = "gs-c-promo gs-t-News nw-c-promo gs-o-faux-block-link gs-u-pb gs-u-pb+@m nw-p-default gs-c-promo--inline gs-c-promo--stacked@m gs-c-promo--flex"
    title_class_stand_in = "gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text"
    excerpt_class_stand_in = "gs-c-promo-summary gel-long-primer gs-u-mt nw-c-promo-summary gs-u-display-none gs-u-display-block@m"
    time_class_stand_in = "gs-o-bullet__text date qa-status-date"
    response = requests.get(url)  # -MARK #gets the request from the website
    text = response.text # -MARK, makes typing much easier
    data = BeautifulSoup(text, 'html.parser')  # -MARK, Parses the data and makes more readable
    
    #To pull the big headline from BBC - UK site
    bold_container = "gs-c-promo gs-t-News nw-c-promo gs-o-faux-block-link gs-u-pb gs-u-pb+@m nw-p-default gs-c-promo--inline@m gs-c-promo--stacked@xxl gs-c-promo--flex"
    bold_title = "gs-c-promo-heading__title gel-paragon-bold gs-u-mt+ nw-o-link-split__text"
    bold_more_info = "gs-c-promo-summary gel-long-primer gs-u-mt nw-c-promo-summary"
    p_bold = data.find(class_=bold_container)
    p_bold_title = p_bold.find(class_=bold_title).text.strip() if p_bold.find(class_=bold_title) else ''
    p_bold_more_info = p_bold.find(class_=bold_more_info).text.strip() if p_bold.find(class_=bold_more_info) else ''
    #Write big headline from BBC - UK
    #fo.write(str(dt.datetime.today()) + '\n')
    #fo.write("\n"+str(p_bold_title) + '\n')
    #fo.write('\n')
    #fo.write(str(p_bold_more_info) + '\n' + 140 * '-' + '\n' + '\n')
    bar.update(1)
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
        Quill.write(title,more_info,date,fo)
    print("\nBBC - UK: fetched")   





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
    #Pass in "fo" to every FXN or Quill.<function>() won't work
    BBC_UK(fo)
    epoch_latest(fo)
    epoch_US(fo)
    epoch_USPol(fo)
    BBC_World(fo)
    epoch_World(fo)
   

# ___RUNNING PARTS___
main()


#       <other NOTE space>
#
#
#
#
#
#