#!/usr/bin/python
import time
import requests
import pandas as pd
from datetime import datetime

url_list = pd.read_excel('/mnt/c/Users/jassim/Desktop/python/pagespeed_automation/urls.xlsx')
device = 'mobile' #Select here device it can be mobile or desktop
category = 'performance'
today = datetime.now().strftime('%m-%d-%Y')
testtime = datetime.now().strftime('%H')
month = datetime.now().strftime('%m')
year = datetime.now().strftime('%Y')


def webtest(url_list,device,category,today,testtime):
    df_list = []
    for url in url_list['URL']:
        print("Preparing " + url)

# =============================================================================
#         #Call pagespeed API
# =============================================================================
        
        #Lighthouse API
        pagespeed_url = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
        params = {
            'url': url,
            'strategy': device,
            'category': category,
            'key': 'AIzaSyC5kROaGDXh4P58ewt6Iad5Waw0KOPFQ1Q'
        }   
        #making api call for URL
        response = requests.get(pagespeed_url, params=params)
        
        print('Running URL #',url)
        #saving response as json
        data = response.json()
        #setting values for data dump. check line 63
        test = url
        date = today
        
# =============================================================================
#         #Get score from results
# =============================================================================
        
        try:   
            data = data['lighthouseResult']
        except KeyError:
            print('Test Failed')
            data = 'Test Failed'
        pass
        
        try:
            #score
            score = data['categories']['performance']['score']
        #TypeError & KeyError
        except (TypeError, KeyError):
            score = 'Test Failed'
            pass
            
        #list with all values
        values = [test,score,date,testtime,month,year]
        
        # create DataFrame using from score list 
        df_score = pd.DataFrame( values )
        
        #transpose so its columns
        df_score = df_score.transpose()
        
        #appending scores to empty df outside for loop
        df_list.append(df_score)
        #wait 2 seconds before next URL to avoid API limit
        time.sleep(2)

    #concatinating list of dataframe into one
    df = pd.concat(df_list)
    
    #naming columns
    df.columns = ['URL','Score','Date','Time','Month','Year']
    
    CSV(df)
    
## CSV Generator
    
def CSV(df):
    df.to_csv('/mnt/c/Users/jassim/Desktop/python/pagespeed_automation/results.csv', mode='a', header=False)
    

webtest(url_list, device, category, today, testtime)