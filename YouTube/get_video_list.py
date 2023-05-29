import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
from pyasn1.compat.octets import null

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
llista_dfs = []
channels = ['UC2ypBaYnDvnlbzyAH8w2jsw', 'UCOmtuk6Mp66DRFcg81kr3eQ']


def get_video_list_in_dataframe() -> (pd.DataFrame, google_auth_oauthlib.flow.InstalledAppFlow):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret_tfg(2).json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)

    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    for channel in channels:
        request = youtube.search().list(
            part="snippet",
            channelId=channel,
            type='video',
            maxResults=50
        )
        response = request.execute()
        llista_dfs.append(pd.json_normalize(response['items']))
        print(response)

        try:
            hasNextPage = response['nextPageToken']
        except:
            hasNextPage = null

        while hasNextPage:
            request = youtube.search().list(
                part="snippet",
                channelId=channel,
                pageToken=response['nextPageToken'],
                maxResults = 50,
                type="video"
            )
            response = request.execute()
            llista_dfs.append(pd.json_normalize(response['items']))
            print(response)
            try:
                hasNextPage = response['nextPageToken']
            except:
                hasNextPage = null

    # Creem el df a partir de la llista
    df_final = pd.concat(llista_dfs)
    print(df_final)
    df_final.to_csv('yt_videos_list(2).csv', index=False)
    return (df_final, youtube)

    # print(response)
    # df = pd.json_normalize(response)
    # print(df)
    # Exportem el df a un arxiu .csv



if __name__ == "__main__":
    get_video_list_in_dataframe()
