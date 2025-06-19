# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 09:02:06 2021

@author: FasihaIkram
"""


datapath1="CleanData_ObjectDetection.xlsx"

import pandas as pd
import urllib.request
import PIL
from PIL import Image
import os
import webp
colData1=['Appid','detection_scores','detection_classes',
          'detection_Classes_Name','detection_Path']
df = pd.read_json (r'CleanData.json',lines=True)
df=df.drop(['level_0','index'], axis=1)
df.rename(columns={'Appid': 'appId'}, inplace=True)
df = df.drop(df[df.detection_scores < 0.50].index)
cleandf =df.groupby('appId', as_index=False).agg(lambda x: x.tolist())
df_raw = pd.read_json (r'raw_data.json', lines=True)

df_raw=df_raw.drop(['summaryHTML','installs','minInstalls','reviews','histogram',
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

#raise SystemExit
result = pd.merge(cleandf,
                 df_raw,
                 on='appId')
result.head()
