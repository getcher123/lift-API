import os
import requests
import json

def synthesize(folder_id, voice, text):
    yandex_passport_oauth_token = os.environ.get('YPOT') 
    iam_token = os.environ['IAM_TOKEN']
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers = {
        'Authorization': 'Bearer ' + iam_token,
    }

    data = {
        'text': text,
        'lang': 'ru-RU',
        'voice': voice,
        'folderId': folder_id,
        'format': 'mp3',
        'sampleRateHertz': 16000,
    }

    with requests.post(url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code == 401:
            # IAM token has expired, request a new one
            print("IAM token has expired, request a new one")
            iam_url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
            iam_data = {'yandexPassportOauthToken': yandex_passport_oauth_token}

            iam_resp = requests.post(iam_url, data=json.dumps(iam_data))
            if iam_resp.status_code == 200:
                iam_token = iam_resp.json()['iamToken']
                os.environ['IAM_TOKEN'] = iam_token
                headers['Authorization'] = 'Bearer ' + iam_token

                # Retry the request with the new IAM token
                resp = requests.post(url, headers=headers, data=data, stream=True)
                if resp.status_code != 200:
                    raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))
            else:
                raise RuntimeError("Failed to get new IAM token: code: %d, message: %s" % (iam_resp.status_code, iam_resp.text))
        elif resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

        for chunk in resp.iter_content(chunk_size=None):
            yield chunk
