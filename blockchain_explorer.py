from datetime import datetime
from abc import ABC, abstractmethod

import requests

import util


class BlockchainExplorer(ABC):
    @property
    @abstractmethod
    def base_url(self):
        pass

    @property
    @abstractmethod
    def api_key(self):
        pass

    @abstractmethod
    def get_transaction(self, address):
        pass


class BlockchainInfoExplorer(BlockchainExplorer):
    base_url = "https://blockchain.info/rawaddr/"
    api_key = None

    def get_transaction(self, address):
        url = self.base_url + address
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                resp_json = resp.json()
                output = {"final_balance": util.satoshi_to_bitcoin(resp_json["final_balance"]), "transactions": []}
                for idx, tx in enumerate(resp_json["txs"]):
                    output["transactions"].append(
                        {"id": idx
                            , "time": datetime.fromtimestamp(tx["time"])
                            , "result": util.satoshi_to_bitcoin(tx["result"])
                         # , "balance": util.satoshi_to_bitcoin(tx["balance"])
                         })
            else:
                output = {"error": "Not 200 output from blockchain explorer!"}
        except Exception as exp:
            output = {"error": "Exception in http request to blockchain explorer!"}
        return output


class EtherscanExplorer(BlockchainExplorer):
    base_url = "https://api.etherscan.io/api?"
    api_key = "PU6UCT34K7Z9DKUYIGGQBFE37FUBQYXQFR"

    def get_transaction(self, address):
        try:
            successful_balance = False
            balance_url = self.base_url + "module=account" + "&action=balance" + "&address={address}" + \
                          "&tag=latest" + "&apikey={api_key}"
            balance_url = balance_url.format(address=address, api_key=self.api_key)
            resp = requests.get(balance_url)
            if resp.status_code == 200:
                resp_json = resp.json()
                output = {"final_balance": util.wei_to_eth(int(resp_json["result"])), "transactions": []}
                successful_balance = True
            else:
                output = {"error": "Not 200 output from blockchain explorer!"}
            if successful_balance:
                transactions_url = self.base_url + "module=account" + "&action=txlist" + "&address={address}" + \
                                   "&startblock=0" + "&endblock=99999999" + "&sort=desc" + \
                                   "&apikey={api_key}"  # + "&page=0" + "&offset=0"
                transactions_url = transactions_url.format(address=address, api_key=self.api_key)
                resp = requests.get(transactions_url)
                if resp.status_code == 200:
                    resp_json = resp.json()
                    for idx, tx in enumerate(resp_json["result"]):
                        output["transactions"].append(
                            {"id": idx, "time": datetime.fromtimestamp(int(tx["timeStamp"]))
                                , "result": util.wei_to_eth(int(tx["value"]))
                             })
        except Exception as exp:
            print(exp)
            output = {"error": "Exception in http request to blockchain explorer!"}
        return output
