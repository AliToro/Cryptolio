from datetime import datetime
from abc import ABC, abstractmethod
import traceback

from fastapi import HTTPException
import requests

import util


class BlockchainExplorerConnector(ABC):
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

    def be_non_200(self):
        raise HTTPException(status_code=503, detail="Non-200 output from the external blockchain explorer!")

    def be_exception(self):
        raise HTTPException(status_code=503,
                            detail="Exception in http request to the external blockchain explorer!")


class BlockchainInfoConnector(BlockchainExplorerConnector):
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
                self.be_non_200()
        except Exception as exp:
            self.be_exception()
        return output


class EtherscanConnector(BlockchainExplorerConnector):
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
                self.be_non_200()
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
                else:
                    self.be_non_200()
        except Exception as exp:
            print(exp)
            self.be_exception()
        return output


class BlockcypherConnector(BlockchainExplorerConnector):
    base_url = "https://api.blockcypher.com/v1/doge/main/addrs/"
    api_key = None

    def get_transaction(self, address):
        url = self.base_url + address
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                resp_json = resp.json()
                output = {"final_balance": util.satoshi_to_bitcoin(resp_json["final_balance"]), "transactions": []}
                for idx, tx in enumerate(resp_json["txrefs"]):
                    value_converted = util.satoshi_to_bitcoin(tx["value"])
                    output["transactions"].append(
                        {"id": idx
                            , "time": tx["confirmed"]
                            , "result": value_converted if tx["tx_output_n"] >= 0 else -1 * value_converted
                         })
            else:
                """
                print(resp.status_code)
                print(resp.text)
                """
                self.be_non_200()
        except Exception as exp:
            # traceback.print_exc()
            self.be_exception()
        return output
