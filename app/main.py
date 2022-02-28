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
    if coin_token in ['Aave', 'Algorand', 'Avalanche', 'Axie_Infinity', 'Binance_Coin', 'Binance_USD', 'BitTorrent',
                      'Bitcoin', 'Bitcoin_BEP2', 'Bitcoin_Cash', 'Bitcoin_SV', 'Cardano', 'Chainlink', 'Cosmos',
                      'Crypto.com_Coin', 'Dai', 'Dash', 'Dogecoin', 'EOS', 'Elrond', 'Ethereum', 'Ethereum_Classic',
                      'FTX_Token', 'Filecoin', 'GRT', 'ICP', 'IOTA', 'Klaytn', 'Kusama', 'LEO', 'Litecoin', 'Maker',
                      'Monero', 'Neo', 'PncakeSwap', 'Polkadot', 'Polygon', 'SHIBA_INU', 'Solana', 'Stellar', 'THETA',
                      'Tether', 'Tezos', 'Tron', 'USD_Coin', 'Uniswap', 'VeChain', 'WBTC', 'Waves', 'XRP']:
        closest_epoc_price = pg_connector.get_price(coin_token, epoc)
        return {"epoc": closest_epoc_price[0], "price": closest_epoc_price[1]}
    else:
        raise HTTPException(status_code=503, detail="unsupported coin/token!")
