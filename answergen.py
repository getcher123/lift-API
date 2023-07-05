import pandas as pd
import os
import json
import numpy
import time
import math

from Morph.stopwords import TextProcessor
from Morph.textproc import text_processing
from compl import Customer
from address import check_address

class AnswerGenerator:
    def __init__(self, stages, textProcessor):
        self.stages = stages
        self.tp = textProcessor
        self.customers = {}

    def initCustomer(self, id_session):
        self.customers[id_session] = {"stage":0}
        print("new init")

    def get_answer(self, query, id_session):
        result = {"Win": 0}
        start_time = time.time()
        if not id_session in self.customers:
            self.initCustomer(id_session)
        cs = self.customers[id_session]
        
        if (os.environ['STOPWORDS'].lower() == 'да'):
            query = self.tp.remove_stop_words(query)

        crit = self.stages.at[cs["stage"], "Условие"]
        cs["answer"] = query
        next_stage_crit_satis = self.stages.at[cs["stage"], "Выполнено"]
        next_stage_crit_notf = self.stages.at[cs["stage"], "Не выполнено"]
        
        # print(f'{crit=} {next_stage_crit_satis =} {next_stage_crit_notf =}')
        if is_json_string(crit):
            findCrit = text_processing(crit, query)
            if len(list(findCrit.values())[0]):
                text = self.stages.at[int(next_stage_crit_satis)-2, "Текст"]
                cs["stage"] = int(next_stage_crit_satis)-2
            else:
                text = self.stages.at[int(next_stage_crit_notf)-2, "Текст"]
                cs["stage"] = int(next_stage_crit_notf)-2
        else:
            print("not json!")
            if(crit == "address"):
                print("check address")
                address = check_address(query)
                print("address is ", address)
                print("house:", address["house"])
                if address["house"] :
                    cs["address"] = replace_words(address['result'])
                    text = self.stages.at[int(next_stage_crit_satis)-2, "Текст"]
                    cs["stage"] = int(next_stage_crit_satis)-2
                else:
                    print("no house find!", int(next_stage_crit_notf)-1)
                    text = self.stages.at[int(next_stage_crit_notf)-2, "Текст"]
                    cs["stage"] = int(next_stage_crit_notf)-2
            else: 
                return
        
        if self.stages.at[cs["stage"], "Выполнено"] == 0: result["Win"]=True
        result["answer"] = text.format(**cs)
        return result


def is_json_string(value):
    try:
        json.loads(value)
        return True
    except ValueError:
        return False

def replace_words(text):
        dictionary = {
            "г": "город",
            "ул": "улица",
            "п": "поселение",
            "обл": "область",
            "пл.": "площадь",
            "р-н": "район",
            "б-р": "бульвар",
            "пос": "поселок",
            "ш": "шоссе",
            "д": "дом", 
            "пр-т": "проспект",
            "корп": "корпус",
            "пр": "проезд",
            "стр": "строение",
            "пер": "переулок",
            "наб": "набережная"
        }
        words = text.split()
        replaced_words = []
        for word in words:
            # Проверка, является ли слово отдельным
            if word.strip(".,!?") in dictionary:
                replaced_words.append(dictionary[word.strip(".,!?")])
            else:
                replaced_words.append(word)
        replaced_text = ' '.join(replaced_words)
        return replaced_text
    