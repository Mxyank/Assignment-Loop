import requests
import pandas as pd
import time
import json


API_URL = "https://api.cratejoy.com/v1/subscriptions/"
API_KEY = "74c7a3cb93e22d4d1b06b5b45a4581f5"  


def cancel_subscription(subscription_id):
    url = f"{API_URL}{subscription_id}/cancel"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers)
        response_json = response.json()
        return response.status_code, response_json
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None, {"error": str(e)}


input_file = 'subscriptions_Ids.csv'
output_file = 'output.csv'
df = pd.read_csv(input_file)

# Validate input
if 'platform_subscription_id' not in df.columns:
    raise ValueError("Input CSV must have a 'platform_subscription_id' column")


output_df = pd.DataFrame(columns=['platform_subscription_id', 'response_code', 'response_json'])

# Rate limiting parameters
RATE_LIMIT = 60  # max requests per minute
RATE_LIMIT_INTERVAL = 60 

# Process each subscription ID
for index, row in df.iterrows():
    subscription_id = row['platform_subscription_id']

    if pd.isna(subscription_id) or subscription_id == "":
        print(f"Skipping empty subscription ID at row {index}")
        continue

    # Cancel subscription
    response_code, response_json = cancel_subscription(subscription_id)
    

    new_row = pd.DataFrame({
        'platform_subscription_id': [subscription_id],
        'response_code': [response_code],
        'response_json': [json.dumps(response_json)]
    })
    output_df = pd.concat([output_df, new_row], ignore_index=True)

    # Respect rate limiting
    if (index + 1) % RATE_LIMIT == 0:
        print(f"Rate limit reached, sleeping for {RATE_LIMIT_INTERVAL} seconds")
        time.sleep(RATE_LIMIT_INTERVAL)


output_df.to_csv(output_file, index=False)
print(f"Responses saved to {output_file}")

