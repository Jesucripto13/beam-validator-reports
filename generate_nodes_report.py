import requests
import json
import time
from datetime import datetime

# Configuration
URL = "http://127.0.0.1:9650/ext/bc/2tmrrBo1Lgt1mzzvPSFt73kkQKFas5d1AP88tv9cicwoFp8BSn/rpc"
HEADERS = {"Content-Type": "application/json"}
# Replace NODE_ID with the public node identifier provided by the project.
# This is not the actual node-id, but an identifier published in the transaction
# where the validator was registered and activated on the network.
NODE_ID = "INSERT_PUBLIC_NODE_IDENTIFIER_HERE"
LOG_FILE = "nodes_report.log"
JSON_FILE = "nodes_report.json"  # JSON file for node delegations

# Get the latest block
def get_latest_block():
    payload = {"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}
    response = requests.post(URL, headers=HEADERS, data=json.dumps(payload))
    return int(response.json()["result"], 16)

# Fetch logs
def get_logs(from_block, to_block="latest"):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getLogs",
        "params": [{
            "fromBlock": hex(from_block),
            "toBlock": to_block,
            "topics": [None, None, NODE_ID]
        }],
        "id": 1
    }
    response = requests.post(URL, headers=HEADERS, data=json.dumps(payload))
    return response.json().get("result", [])

# Get details of a transaction (for node delegations)
def get_node_delegation_details(tx_hash):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getTransactionReceipt",
        "params": [tx_hash],
        "id": 1
    }
    response = requests.post(URL, headers=HEADERS, data=json.dumps(payload))
    result = response.json().get("result")
    if not result:
        return []
    
    wallet = None
    token_ids = []
    for log in result["logs"]:
        # Extract the wallet from the delegation event
        if log["topics"][0] == "0xdf91f7709a30fda3fc5fc5dc97cb5d5b05e67e193dccaaef3cb332d23fda83d1":
            wallet = log["topics"][3][-40:]  # Wallet of the delegator
        # Extract token IDs from Transfer events
        if log["topics"][0] == "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef":
            token_id = int(log["topics"][3], 16)  # Token ID of the node
            token_ids.append(token_id)
    
    # If no wallet or token IDs were found, return an empty list
    if not wallet or not token_ids:
        return []
    
    # Return a list of (tx_hash, wallet, token_id) for each token ID
    return [(tx_hash, wallet, token_id) for token_id in token_ids]

# Hide addresses (wallets and transactions)
def hide_address(address):
    if len(address) < 10:  # Ensure the address is long enough
        return address
    return f"{address[:6]}...{address[-4:]}"

# Write to log file and console
def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    with open(LOG_FILE, "a") as f:
        f.write(full_message + "\n")

# Generate the report for node delegations
def generate_report(node_delegations):
    # Prepare data for the report
    node_data = {}
    for tx_hash, wallet, token_id in node_delegations:
        if wallet:
            if wallet not in node_data:
                node_data[wallet] = []
            if str(token_id) not in node_data[wallet]:  # Avoid duplicates
                node_data[wallet].append(str(token_id))
    
    # Structure the report
    report = {"nodes_per_wallet": [], "total_nodes": 0}
    total_nodes = 0
    for wallet, token_ids in node_data.items():
        entry = {
            "wallet": hide_address(f"0x{wallet}"),
            "nodes": token_ids,
            "total_nodes": len(token_ids)
        }
        report["nodes_per_wallet"].append(entry)
        total_nodes += len(token_ids)
    
    report["total_nodes"] = total_nodes

    # Print the report
    log_message("Node Delegations Report:")
    for entry in report["nodes_per_wallet"]:
        log_message(f"Wallet: {entry['wallet']}")
        log_message(f"Nodes: {', '.join(entry['nodes'])}")
        log_message(f"Total Nodes: {entry['total_nodes']}")
        log_message("---")
    log_message(f"Total Nodes (all wallets): {report['total_nodes']}")

    # Save to JSON file
    with open(JSON_FILE, "w") as f:
        json.dump(report, f, indent=4)
    
    log_message(f"Report saved to: {JSON_FILE}")

# Main
processed_txs = set()
last_block = 0
node_delegations = []  # List of (tx_hash, wallet, token_id)

log_message("Starting query for node delegations...")
latest_block = get_latest_block()
logs = get_logs(0, "latest")

for log in logs:
    tx_hash = log["transactionHash"]
    if tx_hash not in processed_txs:
        # Query node delegations
        delegations = get_node_delegation_details(tx_hash)
        for node_tx, node_wallet, token_id in delegations:
            node_delegations.append((node_tx, node_wallet, token_id))
            log_message(f"Node delegation - Transaction: {hide_address(node_tx)}, Wallet: {hide_address(f'0x{node_wallet}')}, Token ID: {token_id}")
        
        processed_txs.add(tx_hash)

# Generate the report
generate_report(node_delegations)
log_message(f"Last block processed: {latest_block}. Script completed.")
