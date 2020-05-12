"""
Author: Adityavardhan Agrawal

The Project:
A news aggregator that automatically sends customized news, arranged company-wise in 
chronological order in an excel sheet in the inbox of the employees to reduce time 
taken to search and read news manually.

Files and modules used:
requests, bs4, datetime, News (I created the news module, in the same project folder),
email, smtplib

Imp Notes:
I have clearly explained each step with doctrings and comments, to make it easier to modify the 
program as per the user need be. This can be achieved my modyfying the links and some bs4 object commands
to extract the desired news piece.
It is particularly important to understand how the target website functions before attempting to 
modify this code. A look at the website's code will allow users to identify 
"""


import requests
import News
import time
from bs4 import BeautifulSoup
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib
import xlsxwriter
import pandas as pd


company_urldict = {"TCS":"https://economictimes.indiatimes.com/tata-consultancy-services-ltd/stocksupdate/companyid-8345.cms", 
"INFY":"https://economictimes.indiatimes.com/infosys-ltd/stocksupdate/companyid-10960.cms", 
"HCLTECH":"https://economictimes.indiatimes.com/hcl-technologies-ltd/stocksupdate/companyid-4291.cms",
"WIPRO":"https://economictimes.indiatimes.com/wipro-ltd/stocksupdate/companyid-12799.cms", 
"TECHM":"https://economictimes.indiatimes.com/tech-mahindra-ltd/stocksupdate/companyid-11221.cms",
"PERSISTENT":"https://economictimes.indiatimes.com/persistent-systems-ltd/stocksupdate/companyid-21519.cms",
"L&TTECH":"https://economictimes.indiatimes.com/lt-technology-services-ltd/stocksupdate/companyid-64987.cms",
"eClerx":"https://economictimes.indiatimes.com/eclerx-services-ltd/stocksupdate/companyid-20366.cms",
"Info-Edge":"https://economictimes.indiatimes.com/info-edge-india-ltd/stocksupdate/companyid-18352.cms"
}


newsItems = []

def send_email():
    """
    Creates an email, using the email library 

    This method reads the mailinglist.txt file in the same folder,
    determining who to send the email to. It then proceeds to read 
    a emailtext.txt file to write the message of the email. The 
    """
    print("writing email...")

    message = MIMEMultipart()
    message['From'] = "indiatech.news.today@gmail.com"
    recipients =  ["blahblah@gmail.com","blahblahblah@gmail.com"]
    message['To'] = ", ".join(recipients)
    message['Subject'] = "Today's News"
    password = "xxxxxxxxxx" # add sender password here
    body = "Good Morning! PFA an excel sheet with today's news! Have a great day."
    message.attach(MIMEText(body,'html'))
    
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("news.xlsx", "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="news.xlsx"')
    message.attach(part)
    
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(message['From'], password)
    server.sendmail(message['From'], recipients, message.as_string())
    server.quit()


def scraper(companydict):
    """
    Returns a list newspiece, which contains news objects
    """
    print("scraping...")
    for company, url in companydict.items():
        print("Delaying for 2 seconds...")
        time.sleep(2)
        print(company)
        all_stories = get_stories(url)
        details = get_details(all_stories)
        dates = get_dates(all_stories)
        headlines = get_headerText(all_stories)
        titles = get_newsTitle(headlines)
        links = get_links(headlines)
        newspieces = create_newsObject(titles, dates, details, company, links, newsItems)
    return newspieces


def get_stories(url):
    """
    Returns a list containing all stories (an html format of the entire story)

    This method requests for the url, and stores into the variable page. Then, using
    the contents of this page, a BeautifulSoup object is created and stored in a 
    variable called soup. The method .find_all is used to find div tags whose class
    id eachStory, saving the returned list in a variable called all_stories.
    """
    #send a get request for the url, and convert the content in a BS object
    print("getting stories...")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    
    #get all the story items
    all_stories = soup.find_all("div", {"class": "eachStory"}, limit = None)
    return all_stories


def get_headerText(all_stories):
    """
    Returns a list containing all the header text (an html format of the entire story)

    Using, all_stories from get_stories(), this method loops over each story and 
    finds div tags with class headingText and appends it to the list headlines.
    """
    #get the heading text block for the story
    print("getting headines...")
    headlines = []
    for each_story in all_stories:
        text = each_story.find("div", {"class": "headingText"})
        headlines.append(text)
    return headlines


def get_newsTitle(headlines):
    """
    Returns a list containing all the news titles (between an html heading tag)

    This method requests for uses the headlines list and loops over each headline
    to find h3 tags. It saves all such tags in a list called titles
    """
    print("getting news titles...")
    #get the news titles
    titles = []
    for headline in headlines:
        title = headline.find("h3")
        titles.append(title.text)
    return titles


def get_dates(all_stories):
    print("getting dates...")
    """
    Returns a list dates of stories (between an html time tag)

    This method loops over the list all_stories and finds time tags. It
    saves all the time tags in a list called dates.
    """
    #get the dates of the story
    dates = []
    for story in all_stories:
        date = story.find("time")
        dates.append(date.text)
    return dates


def get_details(all_stories):
    print("getting details...")
    """
    Returns a list details of stories (between an html paragraph tag)

    This method loops over the list all_stories and finds paragraph tags. It
    saves all the paragraph tags in a list called details.
    """
    #get the additional details paragraph
    details = []
    for story in all_stories:
        detail = story.find("p")
        details.append(detail.text)
    return details


def get_links(headlines):
    print("getting links...")
    """
    Returns a list links of stories (between an html anchor tag)

    This method loops over the list headlines and finds a-tags and stores them
    in an a_tags list. It then loops over the a_tags list and finds the element 
    href, storing it in a list of hrefs for every tag. This list is stored in a 
    list call links. If the list of href is empty, 'no link' is saved, otherwise
    the link is saved.
    """
    #get a_tags as a list, so can differentiate 
    a_tags = []
    for headline in headlines:
        a_tag = headline.find_all("a")
        a_tags.append(a_tag)

    # between news items with no links and items with links
    links = []
    for a_tag in a_tags:
        if len(a_tag)!=0:
            link = a_tag[0].get('href')
            links.append("https://economictimes.indiatimes.com"+ link)
        else:
            links.append("No Link Given!")
    return links


def create_newsObject(titles, dates, details, company, links, newsItems):
    """
    Returns a list of news objects

    This method uses the titles, date, details, company and links
    to instantiate a news object and append it to the list newspieces
    """
    print("creating news objects list...")
    #create a news object and add it to the newsItems list
    newspiece = News.News(titles, dates, details, company,links)
    newsItems.append(newspiece)
    return newsItems


def create_dataframe(newsItems):
    """
    Returns a list with company wise dataframe objects containing the news 

    This method uses pandas to create a dataframe using the scraped data
    """
    print("Putting news into  dataframes...")
    dataframes = []
    for item in newsItems:
        News = {'Company': item.company,'Headlines': item.title,
            'Dates': item.day, 'Detail': item.detail, 'Link': item.link
            }
        df = pd.DataFrame(News)
        dataframes.append(df)
    return dataframes


def populate_excelsheet(dataframeslist):
    """
    Writes the dataframe to locally saved excel sheet

    This method writes the data frame to an excel sheet, saved in the 
    same project folder, and saves the file after populating the sheet
    """
    print("making an excel sheet...")
    companies = ("TCS", "INFY", "HCLT", "WIPRO","TECHM", "PERSISTENT", "L&TTech","eClerx", "Info-edge","Mindtree")
    writer = pd.ExcelWriter('news.xlsx', engine='xlsxwriter')
    i = 0
    for df in dataframeslist:
        df.to_excel(writer, sheet_name=companies[i])
        i += 1
    writer.save()

def run_application():
    """
    Calls functions to get news items list, create data frame, populate excel sheet and send the email
    """
    newsItems = scraper(company_urldict)
    anylist = create_dataframe(newsItems)
    populate_excelsheet(anylist)
    send_email()
    print('Program run complete!')

run_application()