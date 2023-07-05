import os
import json
import openai
import time

import logging
from GoogleSheetDataFrame import GoogleSheetDataFrame
from EmbeddingSimilarity import EmbeddingSimilarity
from utils.downloadGD import download_google_drive_json_file

from init import initvars
from initconfig import initConfig
from Morph.stopwords import TextProcessor
from Morph.textproc import text_processing
from critanal import CriteriaAnalyzer
from answergen import AnswerGenerator
from speechsynth import synthesize
from address import check_address

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

initvars()
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
stages = GoogleSheetDataFrame(json_data, document_key, stages_sheet)
config = GoogleSheetDataFrame(json_data, document_key, config_sheet)
initConfig(config)

#text = 'Привет!'
#voice = 'filipp'

#audio_content = b''.join(synthesize(folder_id, voice, iam_token, text))
#print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@!!!!!!!!!",audio_content)

tp = TextProcessor() # class for removing stopwords from text

'''
if(os.environ['STOPWORDS'].lower()=='да'):
    stages[stages_col] = stages[stages_col].apply(tp.remove_stop_words)
    bads[bads_col] = bads[bads_col].apply(tp.remove_stop_words)
'''

#critAnal = CriteriaAnalyzer(morph)
#print(check_address("самуила маршака 4")["house"])

ag = AnswerGenerator(stages,tp) 
text = "нет"
print(ag.get_answer(text, '652323'))
text = "Мой адрес такой"
print(ag.get_answer(text, '652323'))
text = "Мой адрес такой самуила маршака 4"
print(ag.get_answer(text, '652323'))
time.sleep(1)
text = "Да"
print(ag.get_answer(text, '652323'))
time.sleep(1)
text = "Я застрял в лифте и мне нужна помощь, помогите пожалуйста"
print(ag.get_answer(text, '652323'))
time.sleep(1)
text = "Да"
print(ag.get_answer(text, '652323'))

'''
ag.get_answer(text, '652323')
text = "Я могу задать несколько вопросов?"
ag.get_answer(text, '652323')
text = "Как стать счастливым?"
ag.get_answer(text, '652323')
text = "Ваш возраст?"
ag.get_answer(text, '652323')

#most_similar = stages_embeddings.get_similarity(cleaned_query)
#most_similer_bad = bads_embeddings.get_similarity(cleaned_query)


# print the most similar Employee Question and the similarity score
'''