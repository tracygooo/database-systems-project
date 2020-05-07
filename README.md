## Spring 2020 CSCI-4380 Database Systems Final Project
### 1. General description
This project created a Postgres database based on three public datasets: [Motor vehicle collisions of New York City](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95), [Climate daily summaries of New York City](https://www.ncdc.noaa.gov/cdo-web/datasets), and [COVID-19 Testing in New York State](https://health.data.ny.gov/Health/New-York-State-Statewide-COVID-19-Testing/xdss-u53e/data). The GUI module Tkinter is applied to facilitate users' exploration and interaction with the database.

### 2. Code organization
- `db-setup.sql`: Create database with specified user and user password
- `requirements.txt`: Declare the dependencies of this project
- `datasets.txt`: Contains three URLs for the the three datasets
- `retrieve_data.py`: Download the three datasets in a newly created folder `datasets/`
- `load_data.py`: Load the data of the three datasets into the database 
- `schema.sql`: Create three temporary tables for the three datasets
- `table.sql`: Create the tables for the database and then drop the temporary tables created by `schema.sql`
- `application.py`: Create a user interface for users' interaction with database, the extracted information is displayed both on terminal and UI
- `video.txt`: The link for video presentation

### 3. How to run the code
1. Setup the database
    ```bash
    psql -U postgres postgres < db-setup.sql
    ```
2. Install the dependencies of this project
    ```bash
    pip install -r requirements.txt
    ```
3. Download the datasets
    ```bash
    python retrieve_data.py
    ```
4. Load the datasets into database
    ```bash
    python load_data.py
    ```
5. Running the application 
    - Run application
        ```bash
        python application.py
        ```
    - Go to the UI popped up on the screen 
    - Input the the information in the entries if neccessary
    - Click submit button and the exacted information is displayed both on UI and command line 
    - Please see the details in the User Interface section below

### 4. User Interface 

#### Covid19-1: check new positive case and total tests
- Input: (date, county to be checked) e.g. (2020-3-4, Albany)
- Output: the new positive cases and total tests conducted in Albany on Mar 03 2020 

#### Covid19-2: top counties with the largest amount of new tesing positives.
- Input: (start date, end date, top n counties to be checked), e.g. (2020-3-4, 2020-4-3, 5)
- Output: top 5 counties with the largest number of new positive cases from  Mar 4 to Apr 3 2020 

#### Covid19-3: calculate the positivity rate
- Input:(start date, end date, county), e.g. (2020-3-4, 2020-4-3, Albany)
- Output: the ratio of (new positives/total number of tests performed)

#### Crash-1: rank the most common factors contributing to crashs in NYC
- Input: 'top number of factors to be checked, e.g. (5)
- Output: top n most common factors that contribute to crashs in NYC.

#### Crash-2: rank boroughs the number of crashes
- Input: (start_date, end_date), e.g. (2020-3-4, 2020-4-3)
- Output: boroughs and corresponding number of total crashes occured in descending order 

#### Crash & Weather-1: compute average number of crashes in special weather type
- Input: (weather type), input one of the types below 
    - snow, rain, thunder, fog, smoke, mist, glaze, drizzle, wind
    - For instance, if snow is choosen, it will calculate the average number of crashed by dividing the number of crashes occurring on 'snowy' with the number of days it 'snows'
- Output: the number of crashes per day in this weather type

#### Crash & Weather-2: calculate average crashes within the precipitation range 
- Input: (lower limit of precipitation, upper limit of precipitation)
- Output: the average number of crashes occurring with the precipitation in selected range.

### References
[How to Program a GUI Application (with Python Tkinter)](https://www.youtube.com/watch?v=D8-snVfekto)  
[Building Out The GUI for our Database App - Python Tkinter GUI Tutorial #20](https://www.youtube.com/watch?v=AK1J8xF4fuk)
