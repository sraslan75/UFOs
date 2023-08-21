"""
This module contains program tasks and methods to call API server and manage the results.
"""
import json, requests
import utility as util
from datetime import datetime
import os, time
from datetime import datetime

PROG_PATH = os.getcwd()
ENV_PATH = PROG_PATH + "/env/"
DATA_PATH = PROG_PATH + "/data/"
last_incident_flag = False

#Create folders for storing application data
def setup_prog_env():
    if not os.path.exists(PROG_PATH+'/env'): os.makedirs(PROG_PATH+'/env')
    if not os.path.exists(PROG_PATH+'/data'): os.makedirs(PROG_PATH+'/data')

#Get the last stored incident data/time from the 'last_record' file, so the updates will ignore all incedents that have been stored in the database 
def get_last_record_time_stamp():
    if not os.path.isfile(ENV_PATH + 'last_record'): return 'none' 
    with open(ENV_PATH + 'last_record', 'r') as time_file:
        record_time = time_file.readline()
        if not record_time: return 'none' 
    return record_time

#Saves the last incedent date/time in a file, so next updates will update newer incedents only
def save_incedent_time(incedent_time):
    with open(ENV_PATH + 'last_record', 'w') as time_file:
        time_file.write(incedent_time)
        print (f'Last incident date/time: {incedent_time} \nPlease wait..')

#Saves all sighting records in a particular month  
def save_sightings(year, month):
    global last_incident_flag
    monthly_sigtings = util.GetMonthlyRecords(year, month)
    if not last_incident_flag: 
        last_incident_datetime = monthly_sigtings[0]['time_stamp']
        last_incident_flag = True
        if last_incident_datetime: 
            save_incedent_time(last_incident_datetime)

    for record in monthly_sigtings:
        update_record(record)

        
    return monthly_sigtings    


#Adds a single sighting record to the database 
def update_record(record):
    url = "http://localhost:5000/data"  # Replace with the actual URL of your API
    try:
        response = requests.post(url, json=record)
        if response.status_code == 201:
            pass
            
        else:
            print("Error adding record:", response.json())

    except Exception as e:
        print("Error:", e)    


#Searches for records the meet user criteria (date, city, state, country)
def search_record(criteria):
    base_url = "http://localhost:5000/data/search"  # Update with your server's URL
    response = requests.get(base_url, params=criteria)

    if response.status_code == 200:
        return response.json()
    else:
        return "error"

#Saves search resuts in a json file named with the search request time stamp and stored under the '/data/' folder 
def save_search_results(results):
    current_time = datetime.now()
    filename = DATA_PATH + 'search-' + current_time.strftime('%Y-%m-%d-%H-%M-%S') + '.json'

    if results and results != 'error':
        formatted_result = []

        for record in results:
            formatted_record = {
                "time_stamp": record["time_stamp"],
                "city": record["city"],
                "state": record["state"],
                "country": record["country"],
                "shape": record["shape"],
                "duration": record["duration"],
                "summary": record["summary"],
                "posted": record["posted"],
                "image": record["image"]
    }
            formatted_result.append(formatted_record)
    
        with open(filename, 'w') as searchfile:
            json.dump(formatted_result, searchfile, indent=4)


#Extracts all records (for the year 2023) from the UFO sighting web-site and saves the records in the database 
def populate_database():
    full_list = util.GetAllListings()
    for listing in full_list:
        if listing.find('/') != -1:
            month_year = listing.split('/')
            s_month = month_year[0]
            s_year = month_year[1] 
            if s_month.isnumeric() and s_year.isnumeric():  
                if s_year == '2023':   
                    save_sightings(s_year, s_month)
        
    print ('Process complete: all records were populated..')


#Add all new records to the database
def update_sightings():
    global last_incident_flag 
    last_record_datetime = get_last_record_time_stamp().replace('\n','')
       
    full_list = util.GetAllListings()
    recent_list = full_list[0]
    if recent_list.find('/') != -1:
        month_year = recent_list.split('/')
        s_month = month_year[0]
        s_year = month_year[1]     
        monthly_sigtings = util.GetMonthlyRecords(s_year, s_month)
        records_saved = 0
        for record in monthly_sigtings:
            cur_record_time = datetime.strptime(record['time_stamp'], '%m/%d/%y %H:%M')
            last_record_time = datetime.strptime(last_record_datetime, '%m/%d/%y %H:%M')
            if cur_record_time > last_record_time:
                print('Record to save:', str(record))
                update_record(record)
                records_saved = records_saved + 1
                if not last_incident_flag: 
                    save_incedent_time(record['time_stamp'])
                    last_incident_flag = True
    print (f'Process complete: {records_saved} records saved.')        

#Retrieves all records from the database
def get_all_records():
    base_url = "http://localhost:5000/data"  # Update with your server's URL
    response = requests.get(base_url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve data"}


# Calls the function to retrieve all records from the database and save the results to a Json file with the time stamp in the '/data/' folder  
def get_sightings_data():
    all_records = get_all_records()
    save_search_results(all_records)
    print("** Process complete.. Results are saved in the '/data' folder **")
    
    
#Processes the search entries and call the function to retrieve the matching records from the database
def get_search_results(s_date='', s_city='', s_state='', s_country=''):
    search_criteria = {}
    if s_date: search_criteria['time_stamp'] = s_date
    if s_city: search_criteria['city'] = s_city
    if s_state: search_criteria['state'] = s_state
    if s_country: search_criteria['country'] = s_country
    results=''
    final_recs=[]
    results = search_record(search_criteria)
    if s_date:    
        for record in results:
            rec_date = datetime.strptime(record['time_stamp'], '%m/%d/%y %H:%M')
            rec_date_str = rec_date.strftime('%m/%d/%y')
            #print(f'record date: {rec_date_str}  ||| critera_date: {s_date}')
            if rec_date_str == s_date:
                final_recs.append(record) 
    else:
        final_recs=results

    if results == 'error': 
        print('Unexpected error')
        return

    if len(final_recs) == 0: 
        print('No records found')
        return

    if results != 'error' and len(final_recs) > 0: 
        save_search_results(final_recs)
        print(f'Search results: (Total records = {str(len(final_recs))})')
        #print(final_recs) 
        print("** Results are saved in the '/data' folder **")

    


