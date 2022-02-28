from fastapi import FastAPI, HTTPException

from . import log
from . import be_connector
from .database import pg_connector

app = FastAPI()


@app.get("/address/{currency}/{address}")
def get_address_transactions(currency: str, address: str):
    if currency == "bitcoin":
        connector = be_connector.BlockchainInfoConnector()
    elif currency == "ethereum":
        connector = be_connector.EtherscanConnector()
    elif currency == "dogecoin":
        connector = be_connector.BlockcypherConnector()
    else:
        raise HTTPException(status_code=404, detail="unsupported coin/token!")
    return connector.get_transaction(address)


@app.get("/price/{currency}/{epoc}")
def get_price(currency: str, epoc: int):
    full_currency_names = ['Aave', 'Algorand', 'Avalanche', 'Axie_Infinity', 'Binance_Coin', 'Binance_USD',
                           'BitTorrent', 'Bitcoin', 'Bitcoin_BEP2', 'Bitcoin_Cash', 'Bitcoin_SV', 'Cardano',
                           'Chainlink', 'Cosmos', 'Crypto.com_Coin', 'Dai', 'Dash', 'Dogecoin', 'EOS', 'Elrond',
                           'Ethereum', 'Ethereum_Classic', 'FTX_Token', 'Filecoin', 'GRT', 'ICP', 'IOTA', 'Klaytn',
                           'Kusama', 'LEO', 'Litecoin', 'Maker', 'Monero', 'Neo', 'PncakeSwap', 'Polkadot', 'Polygon',
                           'SHIBA_INU', 'Solana', 'Stellar', 'THETA', 'Tether', 'Tezos', 'Tron', 'USD_Coin', 'Uniswap',
                           'VeChain', 'WBTC', 'Waves', 'XRP']
    short_currency_names = ['AAVE', 'ALGO', 'AVAX', 'AXS', 'BNB', 'BUSD',
                            'BTT', 'BTC', 'BTCB', 'BCH', 'BSV', 'ADA',
                            'LINK', 'ATOM', 'Crypto.com_Coin', 'DAI', 'DASH', 'DOGE', 'EOS', 'EGLD',
                            'ETH', 'ETC', 'FTT', 'FIL', 'GRT', 'ICP', 'IOTA', 'KLAY',
                            'KSM', 'LEO', 'LTC', 'MKR', 'XMR', 'NEO', 'CAKE', 'DOT', 'MATIC',
                            'SHIB', 'SOL', 'XLM', 'THETA', 'USDT', 'XTZ', 'TRX', 'USDC', 'UNI',
                            'VET', 'WBTC', 'WAVES', 'XRP']
    if currency in full_currency_names + short_currency_names:
        if currency in short_currency_names:
            currency = full_currency_names[short_currency_names.index(currency)]
        closest_epoc_price = pg_connector.get_price(currency, epoc)
        return {"epoc": closest_epoc_price[0], "price": closest_epoc_price[1]}
    else:
        raise HTTPException(status_code=503, detail="unsupported coin/token!")
