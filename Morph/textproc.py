import json
import pymorphy2
import re
import time

def normalize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def text_processing(json_data, text):

    """
    Обработка текста в соответствии с заданными критериями в JSON-формате.

    :param json_data: критерии обработки в формате JSON
    :param text: текст для обработки
    :return: результат обработки текста в виде словаря
    """
    start_time = time.time()
    
    morph = pymorphy2.MorphAnalyzer()
    result = {}
    json_data = json.loads(json_data)
    text = normalize(text)
    for key, value in json_data.items():
        if "tag:" in value:
            # Поиск слов с заданными тегами
            words = []
            pronouns_tags = value[4:].split("|")
            for word in text.split():
                parsed_word = morph.parse(word)[0]
                word_tag = str(parsed_word.tag)

                for tag in pronouns_tags:

                    if all(t in word_tag for t in tag.split("&")):
                        words.append(word)

            result[key] = words

        else:
            # Поиск заданных слов
            specified_words = []
            value_list = value.split(",")
            for word in text.split():
                normal_word = morph.parse(word)[0].normal_form
                if normal_word in value_list:
                    specified_words.append(word)
            result[key] = specified_words
    end_time = time.time()
    response_time = end_time - start_time
    print(f"Function text_processing time: {response_time:.2f} seconds")
    return result
