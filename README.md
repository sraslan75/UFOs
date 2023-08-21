# UFOs
Demonstration project to update and access UFO sightings.

Attention: This project is for demonstration only. Please be aware that the code has not been reviewed for security, performance, or maintenance issues. It is not advised to run this code as is in a public-facing environment.   

--------------------------------------

Installation requirements:

Python version 3.x
The following libraries (using pip3 install): ‘Flask’, ‘Flask-MySQL’, flask-mysqldb, ‘beautifulsoup4’, requests,  

-------------------------------------- 
Setting up the database:

This application uses MySql database. You can install MySql using the following command:
sudo apt-get install mysql-server  

After installing MySql, use the following commands to login to MySql, create API user, create the database, and create the table:
{
mysql -u root -p    
CREATE USER 'ufo_admin'@'localhost' IDENTIFIED BY 'jiza_MA!_9182';	
GRANT ALL PRIVILEGES ON your_database_name.* TO 'your_username'@'localhost';
FLUSH PRIVILEGES;
CREATE DATABASE ufo_sightings;
CREATE TABLE sighting (id INT AUTO_INCREMENT PRIMARY KEY, time_stamp VARCHAR(255), city VARCHAR(255), state VARCHAR(255), country VARCHAR(255), shape VARCHAR(255), duration VARCHAR(255), summary TEXT,  posted VARCHAR(255), image VARCHAR(255));
EXIT;
}
-------------------------------------

Setting up the API server:

For this project we are using the Flask's Built-in Development Server. To install and run the API server, just run the following command from the application directory:
python3 ufo_process.py

------------------------------------
Running the application:

You can run the application (from the application directory) with the following arguments:

[-populate]: To populate the database records with the UFO sightings from the database run the command (note that you should only use this argument once when the database is empty):
{python3 ufo-info.py -populate}

[-update]: To update the database records with the new UFO sightings:
python3 ufo-info.py -update

[-all_records]: To retrieve the database records with the new UFO sightings (the records will be saved in a Json file under the ‘/data/' folder):
{python3 ufo-info.py -all_records}

[-search]: The user will be prompted to enter the search criteria, that includes the date of the sighting, the city, the state, and the country. All entries are optional but at least one has to be provided (the records will be saved in a Json file under the ‘/data/' folder):
{python3 ufo-info.py -search}

** To run automatc daily updates, you can schedule a task to run the following command (using task schedular or cron)
{python3 ufo-info.py -update} **

---------------------------------
