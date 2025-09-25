import pandas as pd
import json

def get_project_df():

    with open("./src/projects_personal.json", "r") as file:
        data3 = json.load(file)
        df3 = pd.DataFrame.from_dict(data3, orient='index')
        df3.reset_index(level=0, inplace=True)
        df3["project_type"] = "Personal"

    with open("./src/projects_freelance.json", "r") as file:
        data2 = json.load(file)
        df2 = pd.DataFrame.from_dict(data2, orient='index')
        df2.reset_index(level=0, inplace=True)
        df2["project_type"] = "Freelance"

    with open("./src/projects.json", "r") as file:
        data1 = json.load(file)
        df1 = pd.DataFrame.from_dict(data1, orient='index')
        df1.reset_index(level=0, inplace=True)
        df1["project_type"] = "Professional"

    df = pd.concat([df1, df2, df3])
    df.reset_index(inplace = True) 
    
    return df

