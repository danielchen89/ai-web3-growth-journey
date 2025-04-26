from web3 import Web3

# 1. 配置参数
rpc_url = "https://eth-sepolia.api.onfinality.io/public"
private_key = ""  # 切勿泄露主网私钥
account_address = ""
contract_address = ""

# ====== 2. ABI ======
contract_abi = [
    {
        "inputs": [
            {"internalType": "address", "name": "player", "type": "address"},
            {"internalType": "string", "name": "tokenURI", "type": "string"}
        ],
        "name": "awardItem",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# ====== 3. 初始化Web3和合约对象 ======
w3 = Web3(Web3.HTTPProvider(rpc_url))
if not w3.is_connected():
    print("无法连接到以太坊节点，请检查RPC地址")
    exit(1)

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# ====== 4. 构造交易 ======
nonce = w3.eth.get_transaction_count(account_address, 'pending')  # 获取pending nonce，防止冲突
token_uri = "nft.json"  # NFT元数据链接，可自定义
print(nonce)
print(token_uri)

tx = contract.functions.awardItem(account_address, token_uri).build_transaction({
    'from': account_address,
    'nonce': nonce,
    'gas': 300000,
    'gasPrice': w3.to_wei('30000', 'gwei')  # 提高gasPrice
})

# ====== 5. 签名并发送交易 ======
signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
print("交易已发送，哈希:", w3.to_hex(tx_hash))

# ====== 6. 等待交易确认 ======
try:
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)  # 等待更长时间
    print("Mint成功，区块号:", receipt.blockNumber)
except Exception as e:
    print("等待交易确认超时或失败:", e)