import pandas as pd
import time

class CriteriaAnalyzer:
    def __init__(self, df):
        self.df = df
        
    def get_criteria_by_stage(self, stage_number):
        start_time = time.time()
        # filter the rows based on the condition
        filtered_rows = self.df[self.df["Этапы"].astype(str).str.contains(str(stage_number)) ]
    
        # get the values of Критерий for the filtered rows
        # criteria_list = filtered_rows["Критерий"].tolist()
    
        # return the criteria list
        end_time = time.time()
        response_time = end_time - start_time
        print(f"Function get_criteria_by_stage time: {response_time:.2f} seconds")
        return filtered_rows