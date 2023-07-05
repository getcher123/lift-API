import pandas as pd
import numpy as np
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import logging

class GoogleSheetDataFrame(pd.DataFrame):
    def __init__(self, creds_json, document_key, sheet_name):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
        gc = gspread.authorize(credentials)
        sh = gc.open_by_key(document_key)
        worksheet = sh.worksheet(sheet_name)
        records = worksheet.get_all_records()
        super().__init__(records)
        self.replace("", np.nan, inplace=True)
        self.fillna(method='ffill', inplace=True)
