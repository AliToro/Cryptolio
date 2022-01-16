from fastapi import FastAPI
import util
import be_connector


app = FastAPI()


@app.post("/address/{coin}/{address}")
def get_address_transactions(coin: str, address: str):
    if coin == "Bitcoin":
        bci_connector = be_connector.BlockchainInfoConnector()
        return bci_connector.get_transaction(address)
    elif coin == "Ethereum":
        ets_connector = be_connector.EtherscanConnector()
        return ets_connector.get_transaction(address)
    else:
        return {"error": "Wrong input, please check your input!"}
