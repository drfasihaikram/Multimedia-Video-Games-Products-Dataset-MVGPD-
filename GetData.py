#This script automates the collection of app metadata and user reviews from the Google Play Store, focusing on games related to various #search keywords (e.g., "action", "battleground", "gun shooter"). It leverages the third-party libraries google_play_scraper and #play_scraper to:

#Generate search suggestions for game-related queries.

#Search apps based on these suggestions.

#Extract detailed app metadata (e.g., title, genre, rating, installs, etc.).

#Extract user reviews for each app, categorized by review score (1 to 5 stars).

#Store results into two JSON files:

#raw_data.json – for app metadata

#rawReviews.json – for user reviews

#The script avoids duplication by checking if an app ID already exists in the saved dataset. It is optimized to continue where it left off #by skipping already processed search terms.



from google_play_scraper import app
from google_play_scraper import Sort, reviews
import play_scraper
import pandas as pd
import time

# starting time
start = time.time()
def getappdetails(a,search_keyword):
#    rawdata = pd.read_excel (r'raw_data.xlsx')
    global rawdata
    rawdata=  pd.read_json('raw_data.json', lines=True)
    #print("raw data size\t"+str(len(rawdata)))
    for x in a:
    #    print(x['app_id'])
        if(len(rawdata.loc[rawdata['appId'] ==  x['app_id']])>=1):
                 #print("duplicate\t" + x['app_id'])
                 continue
        result = app(
        x['app_id'],
        lang='en', # defaults to 'en'
        country='us')
        df=pd.DataFrame.from_dict(result, orient='index').transpose()
        df.insert(0, 'Search_keyword', search_keyword)
        
    
        if (len(df)>=1):
            rawdata= rawdata.append(df)
            
   # rawdata.drop_duplicates( "appId" , keep='first')
   # rawdata.to_excel("raw_data.xlsx",index=False)
    rawdata.to_json(r'raw_data.json', orient='records', lines=True)
    print("raw data size\t"+str(len(rawdata)))
    #print(rawdata[1])


def getUSerReviews(a):
       
#    rawreviews = pd.read_excel (r'rawReviews.xlsx')
    global  rawreviews
    rawreviews=pd.read_json('rawReviews.json', lines=True)
  #  print("rawReviews size \t "+str(len(rawreviews)))
    for index in range(1, 6):
        #print(str(index))
        #if(i<=2):
         #   continue
        for x in a:
            #print(x['app_id'])
            if(len(rawreviews.loc[rawreviews['appId'] ==  x['app_id']])>=1):
            #     print("duplicate\t" + x['app_id'])
                 continue
            result, continuation_token = reviews(
            x['app_id'],
            lang='en',  
            sort=Sort.MOST_RELEVANT,  
            count=100,  filter_score_with=index   )
            #global df
            df=pd.DataFrame(result)
            df.insert(0, 'appId', x['app_id'])
            if (len(df)>=1):
               rawreviews= rawreviews.append(df)
   # rawreviews.to_excel("rawReviews.xlsx", index=False)
    rawreviews.to_json('rawReviews.json', orient='records', lines=True)  
    print("rawReviews size \t "+str(len(rawreviews)))


#raise SystemExit()


#suggestions=play_scraper.suggestions('first person')
search=['first person','action','fighting','battleground','battlegrounds',
        'battles','deathmatch','MASSIVE BATTLE MAPS','Third-Person Shooter',
        'weapons','Gun Shooter','Shooter ','Mafia','Gangster','violent',
        'war','kill','strike','violence']

suggestions=[]
for i in range(len(search)):
    #if (i==0):
        temp=search[i]+" "+ " games"
        suggestions.extend(play_scraper.suggestions(temp))
suggestions = list(dict.fromkeys(suggestions))
count=0
#raise SystemExit()
for  x in suggestions:
        count=count+1
        if(count<=76):
         continue
        print("SEARCHING=="+x)
        a=play_scraper.search(x)
        getappdetails(a,x)
        print("User Reviews=="+x)
        getUSerReviews(a)
    #     break
end = time.time()

# total time taken
print(f"Runtime of the program is {end - start}")
raise SystemExit