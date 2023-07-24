import requests
import json
from web3 import Web3

node_url = "https://bsc-dataseed2.ninicoin.io"
privateKey = "Walelt private key"
w3 = Web3(Web3.HTTPProvider(node_url))
account = w3.eth.account.from_key(privateKey)
token = "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82"


class EnsoFinance:
    base_url: str = "https://api.enso.finance/api/v1"
    key: str = "1e02632d-6feb-4a75-a157-documentation"
    url: str = "https://api.enso.finance/api/v1/shortcuts/bundle"

    def __init__(self):
        pass

    def approve(self, chain_id, _from, token_address, amount):
        params = {
            "chainId": chain_id,
            "fromAddress": _from,
            "tokenAddress": token_address,
            "amount": amount,
        }
        url = self.base_url + "/wallet/approve"
        res = requests.get(url, params=params)
        # print(res.url)
        trx = res.json()["tx"]
        trx["value"] = int(trx.get("value", 0))
        trx["gas"] = 1000000
        trx["gasPrice"] = w3.to_wei("5", "gwei")
        nonce = w3.eth.get_transaction_count(account.address)
        trx["nonce"] = nonce
        tnx = w3.eth.account.sign_transaction(trx, privateKey)
        res = w3.eth.send_raw_transaction(tnx.rawTransaction)
        print(res.hex())

    def swap_one(self):
        url = "https://api.enso.finance/api/v1/shortcuts/route"
        params = {
            "chainId": 137,
            "fromAddress": account.address,
            "priceImpact": False,
            "toEao": True,
            "amountIn": 1000000000000000000,
            "slippage": 300,
            "tokenIn": token,
            "tokenOut": "0xae7ab96520de3a18e5e111b5eaab095312d7fe84",
        }
        res = requests.get(
            url,
            params=params,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.key}",
            },
        )
        print(res.json())

    def swap(self):
        in_ = Web3.to_checksum_address("0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82")
        out = Web3.to_checksum_address("0x1D2F0da169ceB9fC7B3144628dB156f3F6c60dBE")
        data = [
            {
                "protocol": "uniswap-v2",
                "action": "swap",
                "args": {
                    "tokenIn": in_,
                    "tokenOut": out,
                    "amountIn": 2154695,
                    "slippage": 5,
                    "primaryAddress": "0x10ED43C718714eb63d5aA57B78B54704E256024E",
                },
            },
        ]
        # url = self.base_url + "/actions/swap"
        params = {"chainId": 56, "fromAddress": account.address, "toEoa": True}
        res = requests.post(
            self.url,
            params=params,
            data=json.dumps(data),
            headers={
                "Authorization": f"Bearer {self.key}",
                "Content-Type": "application/json",
            },
        )
        trx = res.json()["tx"]
        trx["value"] = int(trx["value"])
        trx["gas"] = 1000000
        trx["gasPrice"] = w3.to_wei("5", "gwei")
        nonce = w3.eth.get_transaction_count(account.address)
        trx["nonce"] = nonce
        # print(trx)

        tnx = w3.eth.account.sign_transaction(trx, privateKey)
        res = w3.eth.send_raw_transaction(tnx.rawTransaction)
        print(res.hex())


enso = EnsoFinance()
print(account.address)
# enso.swap_one()
# enso.swap_one()
# enso.approve(56, account.address, token, 10000000000000000000)


# curl -X GET \
#   -H "Content-Type: application/json" \
#   -H "Authorization: Bearer 1e02632d-6feb-4a75-a157-documentation" \
#   "https://api.enso.finance/api/v1/shortcuts/route?chainId=1&fromAddress=0xD6A4217CF6A3587B4E33e9a59C52BF57469e713a&priceImpact=false&toEoa=false&amountIn=1000000000000000000&slippage=300&tokenIn=&tokenOut=0xae7ab96520de3a18e5e111b5eaab095312d7fe84"


# print(res.json())
# print(account.address)
# enso.swap()
# enso.approve(
#     56,
#     account.address,
#     token,
#     1000000000000000000000000000,
# )
# chainId = 1
# fromAddress = "0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80"
# url = f"https://api.enso.finance/api/v1/wallet?chainId={chainId}&fromAddress={fromAddress}"
# res = requests.get(url)
# print(res.json())
