import os
import json
from flask import Flask, make_response, request, jsonify
from flask_cors import CORS
import openai
import time


import logging
from GoogleSheetDataFrame import GoogleSheetDataFrame
from EmbeddingSimilarity import EmbeddingSimilarity
from utils.downloadGD import download_google_drive_json_file

#from init import initvars
from initconfig import initConfig
from Morph.stopwords import TextProcessor
from Morph.textproc import text_processing
from critanal import CriteriaAnalyzer
from answergen import AnswerGenerator
from speechsynth import synthesize

app = Flask(__name__)
CORS(app)

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#initvars()


openai.api_key = os.environ['OPENAI_API_KEY']
creds_id_google_drive = os.environ['CREDS_ID_GD']
document_key = os.environ['DOCUMENT_KEY']
stages_sheet = os.environ['STAGES_SHEET']
config_sheet = os.environ['CONFIG_SHEET']
iam_token = os.environ.get('IAM_TOKEN')
folder_id = os.environ.get('FOLDER_ID')
yandex_passport_oauth_token = os.environ.get('YPOT') 

json_data = download_google_drive_json_file(creds_id_google_drive)

# define main classes for googsheets reading sheets


@app.route('/init', methods=['GET'])
def init():
    global stages, config, tp, ag
    stages = GoogleSheetDataFrame(json_data, document_key, stages_sheet)
    config = GoogleSheetDataFrame(json_data, document_key, config_sheet)
    initConfig(config)

    tp = TextProcessor() # class for removing stopwords from text

    ag = AnswerGenerator(stages, tp) 
    return 'Init complete!'


init()

# rename columns
if __name__ == '__main__':
    app.run()
    

@app.route('/getresponse', methods=['POST'])
def getresponse():
        request_data = request.get_json()
        query = request_data["query"]
        sission_id = request_data["session_id"]
        result = ag.get_answer(query, sission_id)
        result = jsonify(result)
        headers = {}
        headers['Content-Type'] = 'application/json'
        headers['Access-Control-Allow-Origin'] = '*'
        return result, 200, headers

@app.route('/initdata', methods=['GET'])
def initdata():
        result = {
              'firstfrase': os.environ['FIRST_PHRASE'],
              'instructions': os.environ['INSTRUCTION'],
              'gameover': os.environ['GAME_OVER'],
              'gamewin': os.environ['GAME_WIN']
        }
        result = jsonify(result)
        headers = {}
        headers['Content-Type'] = 'application/json'
        headers['Access-Control-Allow-Origin'] = '*'
        return result, 200, headers

@app.route("/synthesize", methods=["POST"])
def synthesize_text():
    start_time = time.time()
    data = request.get_json()
    text = data['text']
    voice = data['voice']

    audio_content = b''.join(synthesize(folder_id, voice, text))
    response = app.response_class(
        response=audio_content,
        content_type='audio/mp3'
    )

    end_time = time.time()
    response_time = end_time - start_time
    print(f"Voice syntheze time: {response_time:.2f} seconds")

    return response