import json
import ssl

import bitstamp.client
import websocket

import credenciais

def cliente():
    return bitstamp.client.Trading(username=credenciais.USERNAME, key=credenciais.KEY, secret=credenciais.SECRET)

def ao_abrir(ws):
    print('Abriu a conexão')
    
    json_subscribe = '''
{ "event": "bts:subscribe", "data": { "channel": "live_trades_btcusd" } }
'''
    ws.send(json_subscribe)

def ao_fechar(ws):
    print('fechou a conexão')

def erro(ws, erro):
    print(erro)


def ao_receber_mensagem(ws, mensagem):
    message = json.loads(mensagem)
    price = message['data']['price']
    print(int(price))
    
    if int(price) > 9000:
        vender()
    elif int(price) < 8000:
        comprar()
    else:
        print('Aguardando.')
    
    
def comprar(quantidade):    
    trading_client = cliente()
    trading_client.buy_market_order(quantidade)

def vender(quantidade):
    trading_client = cliente()
    trading_client.sell_market_order(quantidade)
    
if __name__ == '__main__':
    ws = websocket.WebSocketApp("wss://ws.bitstamp.net",
                                on_open=ao_abrir,
                                on_close=ao_fechar,
                                on_message=ao_receber_mensagem,
                                on_error=erro)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
#master
