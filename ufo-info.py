"""
This is the main application module that takes command argument to process inquiries (populate database, retrieve all records, update new records, and search database)
"""
import sys, re
import ufo_functions as ufo_task

#Prompts the user to enter search criteria
def process_search():
    search_date = input('Search by Date: (date format: mm/dd/yy) \n[Press enter to skip]\n>> ')
    if search_date:
         pattern = r"^\d{2}/\d{2}/\d{2}$"
         if not re.match(pattern, search_date):
            search_date = input('Incorrect date format (date format must be: mm/dd/yy)\n>> ') 
            if not re.match(pattern, search_date): 
                print('Incorrect date format. Program will exit. Please reenter the command to start over!')
                return

    search_city = input('Search by City: \n[Press enter to skip]\n>> ')
    search_state = input('Search by State: \n[Press enter to skip]\n>> ')
    search_country = input('Search by Country: \n[Press enter to skip]\n>> ')
    if search_date or search_city or search_state or search_country: 
        ufo_task.get_search_results(search_date, search_city, search_state, search_country)
    else: 
        print('No search parameters were provided. Program will exit. ')
        return


if __name__ == "__main__":
    # Check if there is at least one command line argument
    ufo_task.setup_prog_env()
    if len(sys.argv) < 2:
        print("Usage: command arguument is missing. Valid arguments are:\n(-populate), (-update), (-search), (-all_records).")
    else:
        # Access the command line argument 
        argument = sys.argv[1]
        if argument == '-populate': 
            ufo_task.populate_database()
        elif argument == '-update':
            ufo_task.update_sightings()
        elif argument == '-all_records':
            ufo_task.get_sightings_data()
        elif argument == '-search':
            process_search()    
        else: print("Usage: incorrect command arguument. Valid arguments are:\n(-populate), (-update), (-search), (-all_records).")
        #print("Command line argument:", argument)