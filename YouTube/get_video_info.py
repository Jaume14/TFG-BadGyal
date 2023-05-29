import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
import numpy as np
from pyasn1.compat.octets import null

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
llista_dfs = []
channels = ['UC2ypBaYnDvnlbzyAH8w2jsw', 'UCOmtuk6Mp66DRFcg81kr3eQ']


def main():
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret_tfg(2).json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)

    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    count = 0
    df_inicial = pd.read_csv("yt_videos_list(2).csv", header=0)
    print(df_inicial)
    # carrega bé el fitxer

    for song in df_inicial['id.videoId']:
        # print(song)
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=song
        )
        response = request.execute()
        # print(response)
        responseo = response['items'][0]
        response = response['items'][0]['snippet']
        #print(responseo)

        if response.get('tags') == None:
            df = pd.DataFrame({
                'title': response['title'],
                'id': responseo['id'],
                'publishedAt': response['publishedAt'],
                'channelId': response['channelId'],
                'description': response['description'],
                'channelTitle': response['channelTitle'],
                'tags': "None",
                'categoryId': response['categoryId'],
                'liveBroadcastContent': response['liveBroadcastContent'],
                'duration': responseo['contentDetails']['duration'],
                'caption': responseo['contentDetails']['caption'],
                'licensedContent': responseo['contentDetails']['licensedContent'],
                'contentRating': responseo['contentDetails']['contentRating'],
                'projection': responseo['contentDetails']['projection'],
                'viewCount': responseo['statistics']['viewCount'],
                'likeCount': responseo['statistics']['likeCount'],
                # 'favoriteCount': responseo['statistics']['favoriteCount'],
                'commentCount': responseo['statistics']['commentCount']
            }, index=[0])
        else:
            df = pd.DataFrame({
                'title': response['title'],
                'id': responseo['id'],
                'publishedAt': response['publishedAt'],
                'channelId': response['channelId'],
                'description': response['description'],
                'channelTitle': response['channelTitle'],
                'tags': ",".join(response['tags']),
                'categoryId': response['categoryId'],
                'liveBroadcastContent': response['liveBroadcastContent'],
                'duration': responseo['contentDetails']['duration'],
                'caption': responseo['contentDetails']['caption'],
                'licensedContent': responseo['contentDetails']['licensedContent'],
                'contentRating': responseo['contentDetails']['contentRating'],
                'projection': responseo['contentDetails']['projection'],
                'viewCount': responseo['statistics']['viewCount'],
                'likeCount': responseo['statistics']['likeCount'],
                # 'favoriteCount': responseo['statistics']['favoriteCount'],
                'commentCount': responseo['statistics']['commentCount']
            }, index=[0])
        # print(df)
        llista_dfs.append(df)
        count += 1
        print(count)

        # print(llista_dfs)
    final_df = pd.concat(llista_dfs)
    #final_df.to_csv('export(4).csv', index=False)
    #no funciona:    #np.savetxt('export(4).csv', final_df, delimiter=':::')
    #probem amb json
    with open('export(4).json', 'w') as f:
        f.write(final_df.to_json(orient='records', lines=True))

if __name__ == "__main__":
    main()
