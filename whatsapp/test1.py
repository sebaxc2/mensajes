import requests

api_url = "https://script.google.com/macros/s/AKfycbyoBhxuklU5D3LTguTcYAS85klwFINHxxd-FroauC4CmFVvS0ua/exec"

token='GA230122200022' 

payload = {"op": "registermessage", "token_qr": token, "mensajes": [
                {"numero": "56968431809","mensaje": "Trota!!!"},
             ]}

response = requests.post(api_url, json=payload)
print(response.json())

