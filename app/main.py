import logging

from fastapi import FastAPI, HTTPException

from app import be_connector

app = FastAPI()
logging.basicConfig(filename='logs/cryptolio.log', level=logging.INFO)


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