# Project predicting Covid Outbreak in India

 ##############################################################
#                                                            #
#              Author : Ved Prakash Gupta                    #
#                                                            #
#   Note : pls run this program pn any Notebook not Idle     #
#           copyright(c)2020 Ved Prakash Gupta.              #
#                    All Right Reserved.                     #
#                                                            #
##############################################################


# ----------- user define function for Blank line
def space():
    print("\n\n")


# ------------ find all global keys on program
def key():
    key = globals()
    for x in key:
        print(x)


# ---------------- importing the required libraries

import pandas as pd

# Visualisation libraries
import matplotlib.pyplot as plt
#%matplotlib inline

import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import folium 
from folium import plugins

# Manipulating the default plot size
plt.rcParams['figure.figsize'] = 10, 12

#----------------Disable warnings 
import warnings
warnings.filterwarnings('ignore')

#----------------Operational library

# for date and time opeations
from datetime import datetime
# for file and folder operations
import os
# for regular expression opeations
import re
# for listing files in a folder
import glob
# for getting web contents
import requests 
# for scraping web contents
from bs4 import BeautifulSoup


#------------------Get data from the website form of HTML

# get data

# link at which web data recides
link = 'https://www.mohfw.gov.in/'

# get web data
req = requests.get(link)
print(req)
#print(type(str(req)))
if str(req) == "<Response [200]>":
  print("*Succesfully Connected with Ministry of Health and  Family Wellfare ")
# parse web data
soup = BeautifulSoup(req.content, "html.parser")
print("*Write 'soup' for seeing HTML data ")
#print(soup)
space()  #--for blank line

#----------------------find the table from HTML

# find the table
# ==============
# our target table is the last table in the page

# get the table head
# table head may contain the column names, titles, subtitles
# [-1] using for removing list bracket[] from content
thead = soup.find_all('thead')[-1]
print(thead)
space()

# get all the rows in table head
# it usually have only one row, which has the column names
head = thead.find_all('tr')
print(head)
space()

# get the table tbody
# it contains the contents
# [-1] using for removing list bracket[] from content
tbody = soup.find_all('tbody')[-1]
print(tbody)
space()

# get all the rows in table body
# each row is each state's entry
body = tbody.find_all('tr')
print(body)
space()



#-----------------change table content to list

# get the table contents
# ======================

# container for header rows / column title
head_rows = []
# container for table body / contents
body_rows = []

# loop through the head and append each row to head
for tr in head:
    td = tr.find_all(['th', 'td'])
    row = [i.text for i in td]
    head_rows.append(row)
print(head_rows)

# loop through the body and append each row to body
for tr in body:
    td = tr.find_all(['th', 'td'])
    row = [i.text for i in td]
    body_rows.append(row)
print(body_rows)
space()

# ----------------------------------------------------- content on DataFrame

# save contents in a dataframe
# ============================
    
# skip last 3 rows, it contains unwanted info
# and other last 3 rows contain sum of Confirm / Recovered and Death
# head_rows contains column title
df_bs = pd.DataFrame(body_rows[:len(body_rows)-6], 
                     columns=head_rows[0])         

# Drop 'S. No.' column
df_bs.drop('S. No.', axis=1, inplace=True)

# there are 36 states+UT in India
df_bs.head(36)
# print(df_bs)


# --------------------------------------------------- Data Cleaning & Wrangling
print("*Content in process on Data Cleaning & Wrangling !")
# date-time information
# =====================
#saving a copy of the dataframe
df_India = df_bs.copy()
# today's date
now  = datetime.now()
# format date to month-day-year
df_India['Date'] = now.strftime("%m/%d/%Y") 

# add 'Date' column to dataframe
df_India['Date'] = pd.to_datetime(df_India['Date'], format='%m/%d/%Y')

# df_India.head(36)
# print(df_India)


# remove extra characters from 'Name of State/UT' column
# automatic # were added on data remove # 
df_India['Name of State / UT'] = df_India['Name of State / UT'].str.replace('#', '')
df_India['Deaths**'] = df_India['Deaths**'].str.replace('#', '')
df_India['Active Cases*'] = df_India['Active Cases*'].str.replace('#', '')
df_India['Cured/Discharged/Migrated*'] = df_India['Cured/Discharged/Migrated*'].str.replace('#', '')
print("*All # value Succesfully Removed From Data")
space()

#---------------------------- Add location of Each State and UT

# latitude and longitude information
# ==================================

# latitude of the states
lat = {'Delhi':28.7041, 'Haryana':29.0588, 'Kerala':10.8505, 'Rajasthan':27.0238,
       'Telengana':18.1124, 'Uttar Pradesh':26.8467, 'Ladakh':34.2996, 'Tamil Nadu':11.1271,
       'Jammu and Kashmir':33.7782, 'Punjab':31.1471, 'Karnataka':15.3173, 'Maharashtra':19.7515,
       'Andhra Pradesh':15.9129, 'Odisha':20.9517, 'Uttarakhand':30.0668, 'West Bengal':22.9868, 
       'Puducherry': 11.9416, 'Chandigarh': 30.7333, 'Chhattisgarh':21.2787, 'Gujarat': 22.2587, 
       'Himachal Pradesh': 31.1048, 'Madhya Pradesh': 22.9734, 'Bihar': 25.0961, 'Manipur':24.6637, 
       'Mizoram':23.1645, 'Goa': 15.2993, 'Andaman and Nicobar Islands': 11.7401, 'Assam' : 26.2006, 
       'Jharkhand': 23.6102, 'Arunachal Pradesh': 28.2180, 'Tripura': 23.9408, 'Nagaland': 26.1584, 
       'Meghalaya' : 25.4670, 'Dadar Nagar Haveli' : 20.1809, 'Sikkim': 27.5330}

# longitude of the states
long = {'Delhi':77.1025, 'Haryana':76.0856, 'Kerala':76.2711, 'Rajasthan':74.2179,
        'Telengana':79.0193, 'Uttar Pradesh':80.9462, 'Ladakh':78.2932, 'Tamil Nadu':78.6569,
        'Jammu and Kashmir':76.5762, 'Punjab':75.3412, 'Karnataka':75.7139, 'Maharashtra':75.7139,
        'Andhra Pradesh':79.7400, 'Odisha':85.0985, 'Uttarakhand':79.0193, 'West Bengal':87.8550, 
        'Puducherry': 79.8083, 'Chandigarh': 76.7794, 'Chhattisgarh':81.8661, 'Gujarat': 71.1924, 
        'Himachal Pradesh': 77.1734, 'Madhya Pradesh': 78.6569, 'Bihar': 85.3131, 'Manipur':93.9063, 
        'Mizoram':92.9376, 'Goa': 74.1240, 'Andaman and Nicobar Islands': 92.6586, 'Assam' : 92.9376, 
        'Jharkhand': 85.2799, 'Arunachal Pradesh': 94.7278, 'Tripura': 91.9882, 'Nagaland': 94.5624,
        'Meghalaya' : 91.3662, 'Dadar Nagar Haveli' : 73.0169, 'Sikkim': 88.5122}

# add latitude column based on 'Name of State / UT' column
df_India['Latitude'] = df_India['Name of State / UT'].map(lat)

# add longitude column based on 'Name of State / UT' column
df_India['Longitude'] = df_India['Name of State / UT'].map(long)

df_India.head(36)


# ---------------------------- Rename Column

# rename columns
# rename columns
    
df_India = df_India.rename(columns={'Total Confirmed cases*': 'Confirmed'})
df_India = df_India.rename(columns={'Cured/Discharged':'Cured'})
df_India = df_India.rename(columns={'Name of State / UT':'State/UnionTerritory'})
df_India = df_India.rename(columns={'Active Cases*':'Active Cases'})
df_India = df_India.rename(columns={'Cured/Discharged/Migrated*':'Cured'})
df_India = df_India.rename(columns={'Deaths**':'Deaths'})

df_India.head(36)

'''    
df_India = df_India.rename(columns={'Cured/Discharged/Migrated' :'Cured/Discharged', 
                                      'Total Confirmed cases *': 'Confirmed', 
                                      'Total Confirmed cases ': 'Confirmed', 
                                      'Total Confirmed cases* ': 'Confirmed'})
df_India = df_India.rename(columns={'Cured/Discharged':'Cured'})
df_India = df_India.rename(columns={'Name of State / UT':'State/UnionTerritory'})
df_India = df_India.rename(columns={'Name of State / UT':'State/UnionTerritory'})

df_India = df_India.rename(columns=lambda x: re.sub('Total Confirmed cases \(Including .* foreign Nationals\) ',
                                                      'Total Confirmed cases',x))
df_India = df_India.rename(columns={'Deaths ( more than 70% cases due to comorbidities )':'Deaths', 
                                      'Deaths**':'Deaths'})
df_India.head(36)
'''

# ------------------------------ set some parameter

# unique state names
df_India['State/UnionTerritory'].unique()

# number of missing values 
df_India.isna().sum()

# number of unique values 
df_India.nunique()


# -------------------------- change datetime type to datetime

# fix datatype
df_India['Date'] = pd.to_datetime(df_India['Date'])


#----------------------------make correction in some State Name

# rename state/UT names
df_India['State/UnionTerritory'].replace('Chattisgarh', 'Chhattisgarh', inplace=True)
df_India['State/UnionTerritory'].replace('Pondicherry', 'Puducherry', inplace=True)



# --------------------------------------- Saving data

# saving data txt file
# ===========

# file names as year-month-day.csv format
file_name = now.strftime("%Y_%m_%d")+' - COVID-19_India.txt'

# location for saving the file
file_loc = 'Data/'

# save file as a scv file
df_India.to_csv(file_loc + file_name , index=False)
space()
print("*data Succesfully saved on data.txt file on same folder")
# df_India.head(36)

# -------------- #

# saving data in .csv file
# ===========

# file names as year-month-day.csv format
file_name = now.strftime("%Y_%m_%d")+' - COVID-19_India_preprocessed.csv'

# location for saving the file
file_loc = "Data/"

# save file as a scv file
df_India.to_csv(file_loc + file_name, index=False)
print("*data Succesfully saved on COVID-19_India_preprocessed.csv file on same folder")
space()

# ------------------------- #

# ------------------read csv file if u have any issue

#Learn how to read a .csv file by creating a dataframe using pandas
# Reading the datasets
# pls recheck the file name before running the program
def read(file_name):
    file_loc = 'Data/'
    df= pd.read_csv(file_loc + file_name)
    df_con_india = df.copy()
    return df
    '''
    this is part of info
    '''

# ------------------------------ see data info
# complete data info
df_India.info()
space()


# --------------------------------------------------- #

# ------------------------ Analysing COVID19 cases in India

# print total case till date
# print total case till date
df = df_India.copy()
# -----------------------print total case till date
space()
today = now.strftime("%Y-%m-%d")

total_cases = df['Confirmed'].map(int).sum()
print('Total number of confirmed COVID19 cases across India till date ( ' +today+ ' ) : ', total_cases)

total_active = df['Active Cases'].map(int).sum()
print("Total Active Cases COVID19 cases as of "+today+" are: ",total_active)

total_cured = df['Cured'].map(int).sum()
print("Total people who were cured as of "+today+" are: ", total_cured)

total_death = df['Deaths'].map(int).sum()
print("Total people who died due to COVID19 as of "+today+" are: ",total_death)
space()

# ------------------------ how to change color of box in pandas

# Removing Date, Latitude and Longitude and other extra columns
df_temp = df.drop(['Latitude', 'Longitude', 'Date'], axis = 1)

# Learn how to highlight your dataframe
df_temp.style.background_gradient(cmap='Reds')

# Total Active  is the Total cases - (Number of death + Cured)
# total_active = df['Total Active'].sum()
print('Total number of active COVID19 cases across India:', total_active)
Tot_Cases = df.groupby('State/UnionTerritory')['Active Cases'].sum().sort_values(ascending=False).to_frame()
Tot_Cases.style.background_gradient(cmap='Reds')



# ---------------------------------------- fetch COVID19 data of other Countries

# these are the github sources
confirmed_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
deaths_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
recovered_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
latest_data = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/04-04-2020.csv')


# ---------------------------- timeSeries Graph using matplotlib

dates = list(confirmed_df.columns[4:])
dates = list(pd.to_datetime(dates))
dates_india = dates[8:]

# dates_india = dates[8:]
df1 = confirmed_df.groupby('Country/Region').sum().reset_index()
df2 = deaths_df.groupby('Country/Region').sum().reset_index()
df3 = recovered_df.groupby('Country/Region').sum().reset_index()

k = df1[df1['Country/Region']=='India'].loc[:,'1/30/20':]
india_confirmed = k.values.tolist()[0] 

k = df2[df2['Country/Region']=='India'].loc[:,'1/30/20':]
india_deaths = k.values.tolist()[0] 

k = df3[df3['Country/Region']=='India'].loc[:,'1/30/20':]
india_recovered = k.values.tolist()[0] 

plt.figure(figsize= (15,10))
plt.xticks(rotation = 90 ,fontsize = 11)
plt.yticks(fontsize = 10)
plt.xlabel("Dates",fontsize = 20)
plt.ylabel('Total cases',fontsize = 20)
plt.title("Total Confirmed, Active, Death in India" , fontsize = 20)

ax1 = plt.plot_date(y =  india_confirmed, x = dates_india,label = 'Confirmed',linestyle ='-',color = 'b')
ax2 = plt.plot_date(y = india_recovered, x = dates_india,label = 'Recovered',linestyle ='-',color = 'g')
ax3 = plt.plot_date(y = india_deaths, x = dates_india,label = 'Death',linestyle ='-',color = 'r')
plt.legend()
plt.show()
