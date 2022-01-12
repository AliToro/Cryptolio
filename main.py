from fastapi import FastAPI
import util
import blockchain_explorer


app = FastAPI()


@app.post("/address/{coin}/{address}")
def get_address_transactions(coin: str, address: str):
    if coin == "Bitcoin":
        bci_explorer = blockchain_explorer.BlockchainInfoExplorer()
        return bci_explorer.get_transaction(address)
    elif coin == "Ethereum":
        ets_explorer = blockchain_explorer.EtherscanExplorer()
        return ets_explorer.get_transaction(address)
    else:
        return {"error": "Wrong input, please check your input!"}
