# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 09:02:06 2021

@author: FasihaIkram
"""

import pandas as pd
import urllib.request
from collections import OrderedDict

df = pd.read_json (r'CleanData.json',lines=True)
df=df.drop(['level_0','index'], axis=1)
df.rename(columns={'Appid': 'appId'}, inplace=True)
df = df.drop(df[df.detection_scores < 0.50].index)
cleandf =df.groupby('appId', as_index=False).agg(lambda x: x.tolist())

df_raw = pd.read_json (r'raw_data.json', lines=True)
df_raw_reviews=pd.read_json(r'rawReviews.json',lines=True)



df_raw_reviews=df_raw_reviews.drop(['reviewCreatedVersion','at','replyContent',
                                    'repliedAt','content','thumbsUpCount',
                                    ], axis=1)

df_raw=df_raw.drop(['summaryHTML','installs','minInstalls','reviews',
                    'histogram','price','free','currency','sale',
                    'saleTime','originalPrice','saleText','offersIAP',
                    'inAppProductPrice','size','androidVersion',
                    'androidVersionText','developer','developerId',
                    'developerEmail','developerWebsite','developerAddress',
                    'privacyPolicy','developerInternalID','descriptionHTML',
                    'videoImage','contentRating','contentRatingDescription',
                    'adSupported','containsAds','released','updated',
                    'version','recentChanges','recentChangesHTML',
                    'icon','headerImage','video','url','ratings','score'], axis=1)

#raise SystemExit
result = pd.merge(cleandf,
                 df_raw,
                 on='appId')

result_users= pd.merge(result,
                 df_raw_reviews,
                 on='appId')


result_users['detection_Classes_Name'] = result_users['detection_Classes_Name'].apply(lambda x: ' '.join(x))

#result_users['detection'] = result_users['detection_Classes_Name'].str.replace(r'\b(\w+)(\s+\1)+\b', r'\1')


#raise SystemExit
#result_users['genre'] = result_users[['genre', 'genreId']].apply(lambda x: ' '.join(x), axis=1)



result_users['genre'] = result_users[['genre', 'genreId',
                                      'detection_Classes_Name','Search_keyword',
                                      'title']].apply(lambda x: ' '.join(x), axis=1)
result_users['genre']=result_users['genre'].map(lambda x: x if type(x)!=str else x.lower())

result_users['genre']=result_users['genre'].str.split(" ").map(set).str.join(" ")

#result_users['detection'] = (result_users['detection_Classes_Name'].str.split().apply(lambda x: OrderedDict.fromkeys(x).keys()).str.join(' '))


pattern = '|'.join(['-','2021','2020','&','3d','-','us',
                    ':','gm','so','the','games','free','to','dday','of','ops','4','sim'])

result_users['genre'] = result_users['genre'].str.replace(pattern, '')

result_users['genre'] = result_users['genre'].str.split()

result_users['genre'] = result_users['genre'].apply(lambda x: '|'.join(x))
result_users[["genre1", "genre2", "genre3", "genre4", "genre5", "genre6", "genre7",
              "genre8", "genre9", "genre10", "genre11", "genre12", "genre13",
              "genre14", "genre15", "genre16", "genre17"]] = result_users["genre"].str.split(pat="|", expand=True)

#raise SystemExit
# for i in range(len(result_users)):
#  if i==0:
#        min=len(result_users['genre'][i])
#  if(min>len(result_users['genre'][i])):
#         min=len(result_users['genre'][i])
#         print(result_users['genre'][i])
 
#raise SystemExit

result_users=result_users.drop(['detection_scores','detection_classes',
                                'detection_Path','Search_keyword','title',
                                'description','summary','screenshots',
                                'comments','genreId','reviewId','genre',
                                'detection_Classes_Name','userImage','userName'], axis=1)


result_users["id"] = result_users.index + 1
result_users['appId'] = result_users.appId.astype('category').cat.codes

result_users.to_json(r'games_action_genreasrow.json', orient='records', lines=True)