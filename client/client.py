#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import web3
from flask import Flask, render_template, request, make_response, jsonify


from web3 import Web3, HTTPProvider
from solc import compile_source
from web3.contract import ConciseContract

# Solidity source code
with open('Tictactoe.sol', 'rb') as f:
    compiled_sol = compile_source(f.read())




contract_interface = compiled_sol['<stdin>:Tictactoe']

# web3.py instance
w3 = Web3(HTTPProvider("http://ganache:8545"))

print("hello")
# Instantiate and deploy contract
contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Get transaction hash from deployed contract
tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0], 'gas': 4500000})

# Get tx receipt to get contract address
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
contract_address = tx_receipt['contractAddress']

# Contract instance in concise mode
contract_instance = w3.eth.contract(contract_interface['abi'], contract_address, ContractFactoryClass=ConciseContract)

# Getters + Setters for web3.eth.contract object
print('Contract value: {}'.format(contract_instance.getGrid()))
#contract_instance.setGreeting('Nihao', transact={'from': w3.eth.accounts[0]})
#print('Setting value to: Nihao')
#print('Contract value: {}'.format(contract_instance.grid()))

app = Flask(__name__)


@app.route('/')
def index():
    return "heello"
