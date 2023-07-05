import openai
import os

def initConfig(config):
    for index, row in config.iterrows():
        system_var_name = row['Системное название']
        name = row['Переменная']
        os.environ[system_var_name] = str(config.loc[config['Переменная'] == name]['Значение'].iloc[0])






