import json
import sys
import api as api_f
import pandas as pd


filename = sys.argv[-1]
json_filename='transactions_out.json'

        
if __name__ == '__main__':
    #enrich the original json file (`transactions.json`) and enrich it with the data provided by the API ->city and status
    #in this case I've decided to not overwrite the transaction.json but to create a new one (transactions_out.json), 
    #in this way I will maintein a copy of the original file. 
    api_f.enrich_json(filename)
    #from json_file to dataframe: in this way I can use pandas library, which provides groupby operations.
    with open('transactions_out.json','r') as data_file: 
        data = json.load(data_file)
        df = pd.DataFrame(data)
        print(df)
        #output: sum of `product_price`, grouped by user_status and city.
        result=df.groupby(['status', 'city'])['product_price'].agg('sum')
        print(result)