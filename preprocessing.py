import pandas as pd
import urllib.request
import PIL
from PIL import Image
import os
import webp
#df = pd.read_excel (r'raw_data.xlsx')
df=  pd.read_json( r'raw_data.json', lines=True)



index_names = df[ (df['genreId'] != 'GAME_ACTION')].index 
df.drop(index_names, inplace = True)
df.reset_index(inplace=True)
df = df[df['screenshots'].notnull()]
# data=df.drop(['description_html','developer','developer_address','developer_email',
#          'developer_id','developer_url','editors_choice','histogram',
#          'free','histogram','iap','icon','installs','price','recent_changes',
#          'recent_changes','required_android_version','reviews','size','updated',
#          'video','current_version','interactive_elements'], axis=1)

data=df.drop(['summaryHTML','installs','minInstalls','reviews','histogram',
              'price','free','currency','sale','saleTime','originalPrice',
              'saleText',
              'offersIAP','inAppProductPrice','size','androidVersion',
              'androidVersionText',
              'developer','developerId','developerEmail',
              'developerWebsite','developerAddress',
              'privacyPolicy','developerInternalID','descriptionHTML'
              
              ,'videoImage','contentRating','contentRatingDescription',
              'adSupported',
              'containsAds','released','updated','version',
              'recentChanges','recentChangesHTML','icon','headerImage','video',
              'url'
              
              ], axis=1)
#imagedf=data.drop([])
print (len(df['screenshots']))
#raise SystemExit
imgpaths = []

def DownloadImages():
    
    df_images = pd.read_json (r'paths.json', lines=True)
    for index, row in data.iterrows():
        
        if(len(df_images.loc[df_images['appId'] ==  row['appId']])>=1):
                 print("duplicate\t" + row['appId'])
                 continue
        urls=row['screenshots']
        #.replace('[','').replace(']','').replace("'",'').split(",")
        imageleng=len(urls)/5
        
        for j in range(int(imageleng)): 
            print(str(j)+" "+ str( index)+"/"+str(len(data)))
            path=row['appId'].replace(".", "")+"_"+str( j)+".webp";
            df_images = df_images.append({"appId":row['appId'] 
                                          ,"Path":  path },
                                          ignore_index=True)
            urllib.request.urlretrieve(urls[j], path)
    return df_images
def ConvertWEbpTojpg(Frompath):
  for file in os.listdir(Frompath):
    if file.endswith(".webp"):
        print(file)
        #img = webp.load_image(Frompath+'/'+file, 'RGBA')
        rgb_im = Image.open(file).convert("RGB")
        print(Frompath+"/"+file)
        rgb_im.save(file.replace('webp', 'jpg'),"jpeg")

def ImagesdownloadandConver():
    df_images=DownloadImages()
    ConvertWEbpTojpg("C:/Users/FasihaIkram/IntemItem/Games/Paper_First")
    df_images.to_json(r'paths.json', orient='records', lines=True)
ImagesdownloadandConver()

   