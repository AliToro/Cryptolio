from fastapi import FastAPI
import util
import be_connector


app = FastAPI()


@app.post("/address/{coin_token}/{address}")
def get_address_transactions(coin_token: str, address: str):
    if coin_token == "bitcoin":
        bci_connector = be_connector.BlockchainInfoConnector()
        return bci_connector.get_transaction(address)
    elif coin_token == "ethereum":
        ets_connector = be_connector.EtherscanConnector()
        return ets_connector.get_transaction(address)
    elif coin_token == "dogecoin":
        bc_connector = be_connector.BlockcypherConnector()
        return bc_connector.get_transaction(address)
    else:
        return {"error": "Wrong input, please check your coin/token name!"}
