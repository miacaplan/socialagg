import facebook
import requests

# import facebook
import secrets

URL = "https://graph.facebook.com/oauth/access_token"

r = requests.get(URL, {
    'client_id': secrets.APP_ID,
    'client_secret': secrets.APP_SECRET,
    'grant_type': 'client_credentials',
})

r.raise_for_status()

# print(r.text)

key, value = r.text.split("=")
assert key == "access_token"

# r = requests.get(URL, {
#     'client_id': secrets.APP_ID,
#     'client_secret': secrets.APP_SECRET,
#     'grant_type': 'fb_exchange_token',
#     'fb_exchange_token':value
# })
#
# r.raise_for_status()

# key, value = r.text.split("=")
# assert key == "access_token"

# graph = facebook.GraphAPI(access_token=value,version='2.5')
#
# token = graph.extend_access_token(secrets.APP_ID, secrets.APP_SECRET)

with open("TOKEN.txt", "w") as f:
    f.write(value)

graph = facebook.GraphAPI(access_token=value, version='2.5')
print("Connected to FB graph API")
