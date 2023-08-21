"""
This module contains methods needed to extract the sightings records from the UFO sightings web site
"""
from bs4 import BeautifulSoup
import requests
import os, time

#Gets a list of month/year that contain actual records from the UFO sightings web site  
def GetAllListings():
    base_url = "https://nuforc.org/webreports/ndxevent.html" 
    response = requests.get(base_url)
    source = response.text
    soup = BeautifulSoup(source, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')[1:]
    all_listings = []
    for row in rows:
        columns = row.find_all('td')
        group_sighting = columns[0].text.strip()
        all_listings.append(group_sighting)
    return all_listings    


#Gets all the records data for a particular moth/year
def GetMonthlyRecords(s_year, s_month):
    base_url = "https://nuforc.org/webreports/ndxe" + s_year + s_month + ".html"
    #print('GetAllRecords is called', base_url)
    """
    browser = webdriver.Chrome()
    browser.get(base_url)
    source = browser.page_source
    time.sleep(5)
    """
    response = requests.get(base_url)
    source = response.text
    #print(source)
    soup = BeautifulSoup(source, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')[1:]
    sighting_list = []

    for row in rows:
        columns = row.find_all('td')
        time_stamp = columns[0].text.strip()
        city = columns[1].text.strip()
        state = columns[2].text.strip()
        country = columns[3].text.strip()
        shape = columns[4].text.strip()
        duration = columns[5].text.strip()
        summary = columns[6].text.strip()
        posted = columns[7].text.strip()
        image = columns[8].text.strip()        
    
        sighting = {
        'time_stamp': time_stamp,
        'city': city,
        'state': state,
        'country': country,
        'shape': shape,
        'duration': duration,
        'summary': summary,
        'posted': posted,
        'image': image  
        }

        sighting_list.append(sighting)

    
    #print(rows[1]) 
    return sighting_list