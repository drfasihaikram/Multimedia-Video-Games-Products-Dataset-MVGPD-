# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 09:02:06 2021

@author: FasihaIkram
"""

import pandas as pd
import urllib.request
import PIL
from PIL import Image
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
result_users['genre'] = result_users[['genre', 'genreId',
                                      'detection_Classes_Name','Search_keyword',
                                      'title']].apply(lambda x: ' '.join(x), axis=1)

result_users['genre'] = result_users['genre'].str.split() 
result_users['genre'] = result_users['genre'].apply(lambda x: '|'.join(x))
#raise SystemExit
print(result_users['genre'][0])
result_users=result_users.drop(['detection_scores','detection_classes',
                                'detection_Path','Search_keyword','title',
                                'description','summary','screenshots',
                                'comments','genreId','reviewId',
                                'detection_Classes_Name','userImage','userName'], axis=1)
for col in result_users.columns:
    print(col)

result_users["id"] = result_users.index + 1
result_users['appId'] = result_users.appId.astype('category').cat.codes

result_users.to_json(r'games_action.json', orient='records', lines=True)