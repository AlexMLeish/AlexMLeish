import time
from web3 import Web3
from decimal import Decimal

rpc_url = 'https://bsc-testnet-dataseed.bnbchain.org'
web3 = Web3(Web3.HTTPProvider(rpc_url))

if not web3.is_connected():
    raise Exception("Failed to connect to the Ethereum network")

wallet_address = '0x100F83587768381F6bE244585E18B4A791f74BC3'
private_key = '86f56ebd7a984e4f1ef87b47bc9096b449dc2796d564a8c2efc53a221f12e856' 

recipient_address = '0x4A943a4790eE1d75cf154039697a4Fe287b0EEE1'

gas_limit = 21000
gas_price = web3.to_wei('50', 'gwei')

def get_balance(address):
    balance = web3.eth.get_balance(address)
    return web3.from_wei(balance, 'ether')

def send_eth(from_address, to_address, amount, private_key):
    try:
        amount_in_wei = web3.to_wei(amount, 'ether')
        
        nonce = web3.eth.get_transaction_count(from_address)
        
        tx = {
            'nonce': nonce,
            'to': to_address,
            'value': amount_in_wei,
            'gas': gas_limit,
            'gasPrice': gas_price,
            'chainId': 97
        }
        
        total_tx_cost = amount_in_wei + (gas_limit * gas_price)
        
        if total_tx_cost > web3.eth.get_balance(from_address):
            raise Exception(f"Insufficient funds: Total transaction cost is {web3.from_wei(total_tx_cost, 'ether')} ETH")
        
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        return tx_hash
    except Exception as e:
        print(f"Error sending transaction: {e}")
        return None

buffer = Decimal('0.000001')  # Buffer amount in Ether to ensure there's enough balance for transaction fees

while True:
    balance = get_balance(wallet_address)
    print(f"Current balance: {balance} ETH")
    
    max_amount_to_send = balance - web3.from_wei(gas_limit * gas_price, 'ether') - buffer
    
    if max_amount_to_send > Decimal('0.000002'):  # Ensures there is enough balance to cover the transaction fee
        print(f"Transferring {max_amount_to_send} ETH...")
        
        tx_hash = send_eth(wallet_address, recipient_address, max_amount_to_send, private_key)
        
        if tx_hash:
            print(f"Transaction sent with hash: {tx_hash.hex()}")
        else:
            print("Transaction failed")
    
    time.sleep(5)
