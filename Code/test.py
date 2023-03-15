import requests


api_url = "https://aae-t.phillips66.net/v1/authentication"
body = {
    "username" : "phillips66\\botrpa01",
    "apiKey" : "zpZDeJ]7uV!c/w`}Wws.T\"!Z[>KhBP8*E:MGXc;\""
    }

headers = {}

response = requests.post(api_url, json=body, headers=headers)
print(response.json())
