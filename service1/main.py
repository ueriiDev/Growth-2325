from web3 import Web3, HTTPProvider
import json
from web3.utils.address import to_checksum_address
import mysql.connector
import myFunction

with open('config.json', 'r') as f:
    config = json.load(f)

polygon_network = config['polygon_network']
polygon_alchemy_key = config['polygon_alchemy_key']
contract_address_polygon = config['contract_address_polygon']
ethereum_network = config['ethereum_network']
ethereum_alchemy_key = config['ethereum_alchemy_key']
contract_address_ethereum = config['contract_address_ethereum']

w3_polygon = Web3(HTTPProvider(polygon_network + polygon_alchemy_key))
w3_ethereum = Web3(HTTPProvider(ethereum_network + ethereum_alchemy_key))

with open('0xfC6_abi.json', 'r') as f:
    polygon_abi = json.load(f)

with open('0xb5D_abi.json', 'r') as f:
    ethereum_abi = json.load(f)

polygon_contract = w3_polygon.eth.contract(address=contract_address_polygon, abi=polygon_abi)
ethereum_contract = w3_ethereum.eth.contract(address=contract_address_ethereum, abi=ethereum_abi)

# connessione al database
mydb = mysql.connector.connect(
    host=config['host'],
    user=config['user'],
    password=config['password'],
    database=config['database']
)


holders = myFunction.load_holder(mydb)
i = 0
for x in holders:
    i += 1
    """ For each holder, check the balance on the blockchain and update it """
    wallet_address2 = x.wallet
    wallet_address = to_checksum_address(wallet_address2)
    polygon_balance = polygon_contract.functions.balanceOf(wallet_address).call()
    ethereum_balance = ethereum_contract.functions.balanceOf(wallet_address).call()
    x.update_token_polygon(polygon_balance)
    x.update_token_ethereum(ethereum_balance)
    # print(f" wallet {wallet_address} polygon: {myFunction.enter_period_amount(polygon_balance)}")
    # print(f" wallet {wallet_address} ethereum: {myFunction.enter_period_amount(ethereum_balance)}")
    myFunction.update_holder(mydb, x)
    """ This is used to break out of the loop early """
    if i == 5:
        break

""" Update the aggregated token field """
myFunction.adjust_token_aggregated(mydb)




