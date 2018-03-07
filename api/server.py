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


# Getters + Setters for web3.eth.contract object
#print('Contract value: {}'.format(contract_instance.getGrid()))
#contract_instance.setGreeting('Nihao', transact={'from': w3.eth.accounts[0]})
#print('Setting value to: Nihao')
#print('Contract value: {}'.format(contract_instance.grid()))

app = Flask(__name__)


mapping_uid_to_room = dict()
mapping_tg_to_uid = dict()



@app.route('/gameover', methods=['POST'])
def get_over():
	print(request.data)
	req_json = json.loads(request.data.decode('utf8'))
	contract_address = req_json["address"]
	contract_instance = w3.eth.contract(contract_interface['abi'], contract_address, ContractFactoryClass=ConciseContract)
	tx_hash = contract_instance.getOver()
	#receipt = w3.eth.getTransactionReceipt(tx_hash)
	return jsonify(tx_hash)

@app.route('/getwinner', methods=['POST'])
def get_winner():
	print(request.data)
	req_json = json.loads(request.data.decode('utf8'))
	contract_address = req_json["address"]
	contract_instance = w3.eth.contract(contract_interface['abi'], contract_address, ContractFactoryClass=ConciseContract)
	tx_hash = contract_instance.getWinner()
	#receipt = w3.eth.getTransactionReceipt(tx_hash)

	return jsonify(tx_hash)


@app.route('/curraddress', methods=['GET'])
def return_current_adress():
	print("im here")
	print(w3.eth.accounts[0])
	return jsonify({"accounts_list":w3.eth.accounts})


@app.route('/init')
def initgame():

	contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
	# Get transaction hash from deployed contract
	tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0], 'gas': 4500000})
	# Get tx receipt to get contract address
	tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
	contract_address = tx_receipt['contractAddress']

	# Contract instance in concise mode
	contract_instance = w3.eth.contract(contract_interface['abi'], contract_address, ContractFactoryClass=ConciseContract)
	tx_hash = contract_instance.getGrid()
	print("tx_hash", tx_hash)
	receipt = w3.eth.getTransactionReceipt(tx_hash)
	print("receipt", receipt)
	contract_address = tx_receipt['contractAddress']

	return jsonify(contract_address)

@app.route('/step', methods=['POST'])
def step():
	print(request.data)
	req_json = json.loads(request.data.decode('utf8'))

	contract_address = req_json["address"]
	uid = req_json["uid"]
	x = int(req_json["x"])
	y = int(req_json["y"])
	contract_instance = w3.eth.contract(contract_interface['abi'], contract_address, ContractFactoryClass=ConciseContract)
	tx_hash = contract_instance.setStep(x,y, transact={'from': uid})
	receipt = w3.eth.getTransactionReceipt(tx_hash)
	tx_hash = contract_instance.getGrid()
	return jsonify(tx_hash)

@app.route('/')
def index():
    return "heello"

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
