from fastapi import FastAPI, HTTPException

from . import log
from . import be_connector
from .database import pg_connector

app = FastAPI()


@app.get("/address/{coin_token}/{address}")
def get_address_transactions(coin_token: str, address: str):
    if coin_token == "bitcoin":
        connector = be_connector.BlockchainInfoConnector()
    elif coin_token == "ethereum":
        connector = be_connector.EtherscanConnector()
    elif coin_token == "dogecoin":
        connector = be_connector.BlockcypherConnector()
    else:
        raise HTTPException(status_code=404, detail="Wrong input, please check your coin/token name!")
    return connector.get_transaction(address)


@app.get("/price/{exchange}/{coin_token}")
def get_price(exchange: str, coin_token: str):
    pg_connector.get_data()
