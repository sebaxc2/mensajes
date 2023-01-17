#envia mensajes para avisarte de algo en este caso tiempo
import os
from twilio.rest import Client
import time
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime

# armado URL
pais='Chile'

api_key='33e0f68d25c14fef8e5192311231001'

Url='http://api.weatherapi.com/v1/forecast.json?key='+api_key+'&q=+'+pais+'&days=1&aqi=no&alerts=no'

account_sid = "ACb75fcd0719fc71f65d290e9fd43aa5dc"

#response

response=requests.get(Url).json()




response = requests.get(Url).json()
#for key, value in response.items():
#    print(key.replace("-", "_"), value, sep=": ")
#    print()

print(response['forecast']['forecastday'][0].keys())

print(len(response['forecast']['forecastday'][0]['hour']))

print(int(response['forecast']['forecastday'][0]['hour'][1]['time'].split()[1].split(":")[0]))

condicion=response['forecast']['forecastday'][0]['hour'][0]['condition']['text']
temp=float(response['forecast']['forecastday'][0]['hour'][0]['temp_c'])
llovera=response['forecast']['forecastday'][0]['hour'][0]['will_it_rain']
probabilidad=response['forecast']['forecastday'][0]['hour'][0]['chance_of_rain']


#Dataframe

def get_forecast(response,i):
    
    Fecha=response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
    hora=int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(":")[0])
    condición=response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    tempe=float(response['forecast']['forecastday'][0]['hour'][i]['temp_c'])
    rain=response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    prob=response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']
    
    return Fecha,hora,condición,tempe,rain,prob

data=[]
for i in tqdm(range(len(response['forecast']['forecastday'][0]['hour']))):
    
    data.append(get_forecast(response,i))
    

col=['Fecha','hora','condición','tempe','rain','prob']
DF= pd.DataFrame(data,columns=col)
#print(DF.head())

#df_rain=DF[(DF['rain']==0 & (DF['hora']>6 & (DF['hora']<23)))]
# df_rain1=pd.DataFrame()
# df_rain=(DF['hora']>6) | (DF['hora']==0)
# #df_rain= (DF['condición'])
# df_rain = df_rain[~(df_rain==False)]
# df_rain1['Hora_condición']=df_rain
# df_rain=DF['rain']==1
# df_rain1['Llovera']=df_rain
# df_rain=DF['condición']
# df_rain1['Condición']=df_rain
df1=pd.DataFrame()
#df2=(DF['hora'])

#df1['Hora']=df2
df2=(DF['hora']>=6) | (DF['hora']==0)
df2=df2[~(df2==False)]
df1['Hora_condición']=df2
df1['Hora']=DF['hora']
df1['Llovera']=DF['rain']
df1['Condición']=DF['condición']
df1['Temperatura']=DF['tempe']
df_llovera = df1.loc[df1['Llovera'] == 1, ['Hora', 'Condición']]
#print(df_llovera)



if df1['Llovera'].any() == 1:
    aqui = 'llovera con una condición de ' + df1.loc[df1['Llovera'] == 1, 'Condición'].iloc[0] + ' y la hora es ' + str(df1.loc[df1['Llovera'] == 1, 'Hora'].iloc[0])
else:
    aqui = str(df1['Temperatura'].max()) + ' grados'


#print(df_rain1)
#df_rain=df_rain[['hora','condición']]
#df_rain.set_index('hora',inplace=True)
#print(df_rain)


TWILIO_ACCOUNT_SID='ACb75fcd0719fc71f65d290e9fd43aa5dc'
TWILIO_AUTH_TOKEN='18ff120ac55bcc7b5b44ccba708d320c'


current_time = datetime.now().time()
hora_m = datetime.now().strftime("%H:%M")
current_time= current_time.hour
#print(hora_m)


if current_time >= 0 and current_time< 12:
    current_time='Buenos dias '
elif current_time >= 12 and current_time < 18:
    current_time='Buenas tardes '
else:
    current_time="Buenas Noches "





client = Client(account_sid, TWILIO_AUTH_TOKEN)

message = client.messages \
                  .create(
                       body=current_time + 'el pronostico para el día '+ DF['Fecha'][0]+' con '+hora_m+ ' en '+pais+' es : \n'+ aqui,
                      from_='+19388888015',
                      to='+56968431809'
                  )

print('Mensaje Enviado'+ message.sid)





