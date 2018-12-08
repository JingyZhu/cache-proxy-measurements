import json
import base64

url = "https://www.facebook.com/images/groups/sell/chat-to-buy.png"

im = open('cmd', 'rb')

strr = base64.b64encode(im.read())

print(len(strr))