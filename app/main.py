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
        raise HTTPException(status_code=404, detail="unsupported coin/token!")
    return connector.get_transaction(address)


@app.get("/price/{coin_token}/{epoc}")
def get_price(coin_token: str, epoc: int):
    if coin_token == "btc":
        closest_epoc_price = pg_connector.get_price(coin_token, epoc)
        return {"epoc": closest_epoc_price[0], "price": closest_epoc_price[1]}
    else:
        raise HTTPException(status_code=404, detail="unsupported coin/token for the Kucoin exchange!")