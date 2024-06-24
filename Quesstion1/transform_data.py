import pandas as pd


input_file = 'input_data.csv'
df = pd.read_csv(input_file)


def transform_data(df):
    transformed_data = {}
    
    for sub_id in df['Subscription ID'].unique():
        sub_df = df[df['Subscription ID'] == sub_id]
        
        transformed_data[sub_id] = {'Subscription ID': sub_id}
        
        for i, row in enumerate(sub_df.itertuples(), 1):
            transformed_data[sub_id][f'Variant ID_{i}'] = row[2]
            transformed_data[sub_id][f'Line Quantity_{i}'] = row[3]
            transformed_data[sub_id][f'Line Discounted Price_{i}'] = row[4]
    
    transformed_df = pd.DataFrame.from_dict(transformed_data, orient='index')
    
    return transformed_df


transformed_df = transform_data(df)


output_file = 'transformed_data.csv' 
transformed_df.to_csv(output_file, index=False)


print(transformed_df.head())

