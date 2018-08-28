
# coding: utf-8

# In[ ]:

# %load ps5
# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================
# Problem 1

# TODO: NewsStory

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title 
        self.description = description 
        self. link = link 
        self.pubdate = pubdate 
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title 
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate
        

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger

def word_split(phrase):
    wordlist = []
    word = ""
    for index, letter in enumerate(phrase.lower()):
        if letter.isalpha() == True:
            if word.isalpha() == True:
                word += letter
            else:
                word = letter
            if index == len(phrase) -1:
                wordlist.append(word) 
        else:
            if word.isalpha() == True:
                wordlist.append(word)
                word = letter
            else:
                word = letter
    return wordlist
    
    

class PhraseTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger.lower()
    def is_phrase_in(self, phrase):
        trigger = " ".join(word_split(self.trigger))
        phrase = " ".join(word_split(phrase))
        a = trigger in phrase
        b = set(word_split(trigger)).issubset(word_split(phrase))
        if  a == True and b == True:
            return True
        else:
            return False

# Problem 3
# TODO: TitleTrigger

class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        phrase = story.get_title()
        return self.is_phrase_in(phrase) 

# Problem 4
# TODO: DescriptionTrigger

class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        phrase = story.get_description()
        return self.is_phrase_in(phrase) 


# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = datetime.strptime(trigger, "%d %b %Y %H:%M:%S").replace(tzinfo=pytz.timezone("EST"))
        

# Problem 6
# TODO: BeforeTrigger and AfterTrigger

class BeforeTrigger(TimeTrigger):
    def __init__(self, trigger):
        TimeTrigger.__init__(self, trigger)
    
    def evaluate(self, other):
        time = other.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
        return time < self.trigger 

class AfterTrigger(TimeTrigger):
    def __init__(self, trigger):
        TimeTrigger.__init__(self, trigger)
    
    def evaluate(self, other):
        time = other.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
        return time > self.trigger 

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
    def evaluate(self, story):
        if self.trigger.evaluate(story) == False:
            return True
        else:
            return False
        
# Problem 8
# TODO: AndTrigger


class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, story):
        if self.trigger1.evaluate(story) == True and self.trigger2.evaluate(story) == True:
            return True
        else:
            return False
        
# Problem 9
# TODO: OrTrigger

class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, story):
        if self.trigger1.evaluate(story) == False and self.trigger2.evaluate(story) == False:
            return False
        else:
            return True

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    num = []
    for index, news in enumerate(stories):
        for trigger in triggerlist:
            if trigger.evaluate(news) == True:
                num.append(index)
    stories2 = [news for index, news in enumerate(stories) if index in num]
    return stories2
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)


#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):

    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
    com_dict = {}
    
    for index, com in enumerate(lines):
        com_list = com.split(",")
        
        if com_list[0] != "ADD":
            if com_list[1].lower() == "title":
                com_dict[com_list[0]] = TitleTrigger(com_list[2])
                
            elif com_list[1].lower() == "description":
                com_dict[com_list[0]] = DescriptionTrigger(com_list[2])
                
            elif com_list[1].lower() == "before":
                com_dict[com_list[0]] = BeforeTrigger(com_list[2])
                
            elif com_list[1].lower() =="after":
                com_dict[com_list[0]] = AfterTrigger(com_list[2])
                
            elif com_list[1].lower() == "not":
                com_dict[com_list[0]] = NotTrigger(com_dict[com_list[2]])
        
            elif com_list[1].lower() == "and":
                com_dict[com_list[0]] = AndTrigger(com_dict[com_list[2]], com_dict[com_list[3]])
            
            elif com_list[1].lower() == "or":
                com_dict[com_list[0]] = OrTrigger(com_dict[com_list[2]], com_dict[com_list[3]])

        else:
            
            return [v for k, v in com_dict.items() if k in com_list]

SLEEPTIME = 1 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        #t1 = TitleTrigger("Trump")
        #t2 = DescriptionTrigger("USA")
        #t3 = DescriptionTrigger("Mexico")
        #t4 = AndTrigger(t2,t3)
        #triggerlist = [t1,t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
       
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()


