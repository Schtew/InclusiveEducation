import pandas as pd
import numpy as np
import json

# Load the data as a pandas dataframe

class DataCleaning:
    
    def __init__(self):
        self.data = pd.read_csv('data/data.csv').astype(str)
    
    def stringify(self, group):
        tempUnMod = group['Course Name'].iloc[0] + " Originals"
        tempMod = group['Course Name'].iloc[0] + " Adaptations"
        for index, row in group.iterrows():
            tempUnMod = (tempUnMod + ", "+ row['Original Assignment Type'] + ": ("  + row['Assignment Title'] + ": " + str(row['Original %']) + ", " +
                        "Original Expectation: " + row['Original Expectation'] + ")"
                        )
            if row['Modified Title'] == '' or row['Modified Title'] == 'N/A' or row['Modification 1'] == "REM: Removal of a class assignment/expectation":
                tempMod = (tempMod + ", " + row['Original Assignment Type'] + ": (" + "Removed" + ")")
            else:
                tempMod = (tempMod + ", " + row['Original Assignment Type'] + ": (" + row['Modified Title'] + ": " + str(row['Adapted %']) + ", " +
                        "Adapted Expectation: " + row['Adapted Expectation']
                       )
                if row['Modification 1'] != 'not selected':
                    tempMod = tempMod + ", " + "Modifications: " + row['Modification 1']
                    if row['Modification 2'] != 'not selected':
                        tempMod = tempMod + ", " + row['Modification 2']
                    if row['Modification 3'] != 'not selected':
                        tempMod = tempMod + ", " + row['Modification 3']
                tempMod = tempMod + ")"
        return [tempUnMod.replace('\n', ''), tempMod.replace('\n', '')]
        
    def gouper(self):
        # Group the data by the file name
        strings = {}
        grouped = self.data.groupby('File Name')
        for name, group in grouped:
            # print(f"File Name: {name}")
            # print(f"Group:\n{group}\n")
            strings[group['Course Name'].iloc[0]] = self.stringify(group)
        return strings

    def jsonify(self, dict):
        json_list = []
        for course_name, content in dict.items():
            # Construct JSON structure
            json_data = {
                "messages": [
                    #Prompt messages should be adapted to the circumstance of the user. 
                    {"role": "system", "content": "You are an instructor for " + course_name + ". Your task is to adapt a given syllabus to be more acessible for a neurodivergent audience. These individuals may have an intellectual or developmental disability."},
                    {"role": "user", "content": "Given the following syllabus content, adapt it to be more accessible: " + content[0]},
                    {"role": "assistant", "content": "Here's an adapted version: " + content[1]}
                ]
            }
            json_list.append(json_data)
        with open("data/cleandata.json", "w") as json_file:
            json.dump(json_list, json_file, indent=4)

main = DataCleaning()
main.jsonify(main.gouper())
