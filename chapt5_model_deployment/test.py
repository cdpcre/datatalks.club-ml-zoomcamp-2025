import requests

# url = 'https://mlzoomcamp-flask-uv.fly.dev/predict'

url = "http://127.0.0.1:8000/predict"
client = {
    "lead_source": "organic_search",
    "number_of_courses_viewed": 4,
    "annual_income": 80304.0
}
response = requests.post(url, json=client)

predictions = response.json()
print(predictions)

if predictions['subscription_probability'] >= 0.5:
    print('customer is likely to subscribe, send promo')
    print(predictions['subscription_probability'])
else:
    print('customer is not likely to subscribe')
    print(predictions['subscription_probability'])
