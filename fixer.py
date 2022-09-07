import json
import pandas as pd

def prepareData(path, flag):
    with open(path, 'r') as file:
        content = file.read()
        content = content.replace("{\"title\":", "\n{\"title\":")
        
        json_object = json.loads(content)
        for index, row in enumerate(json_object['articles']):
            row['Flag'] = flag
            records.append(row)
            if index+1 == 2000:
                break

if __name__=="__main__":
    records = list()
    feed_list = [["Dataset/source_1/scraped_articles.json", "credible"],
                 ["Dataset/source_7/scraped_articles.json", "uncredible"]
                 ]
    for element in feed_list:
        prepareData(element[0], element[1])

    df = pd.DataFrame.from_records(records)
    # df.to_csv('data.csv', index=False)