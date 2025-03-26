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
LOG_FILE = "stakes_report.log"
JSON_FILE = "stakes_report.json"  # JSON file for BEAM stakes
# Set VALIDATOR_STAKE to the amount of BEAM staked by the validator.
# This is optional; if not set (i.e., 0), the total BEAM will only include delegated stakes.
# If provided, the total BEAM will reflect the correct amount staked by the node.
VALIDATOR_STAKE = 0

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

# Get details of a transaction (for BEAM stakes)
def get_beam_stake_details(tx_hash):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getTransactionReceipt",
        "params": [tx_hash],
        "id": 1
    }
    response = requests.post(URL, headers=HEADERS, data=json.dumps(payload))
    result = response.json().get("result")
    if not result:
        return None, None, None
    
    wallet = None
    amount = 0
    is_stake_event = False

    # Check if the transaction has the BEAM staking event
    for log in result["logs"]:
        if log["topics"][0] == "0x6e350dd49b060d87f297206fd309234ed43156d890ced0f139ecf704310481d3":
            is_stake_event = True
            break
    
    if not is_stake_event:
        return None, None, None

    # If it's a BEAM staking transaction, extract the amount
    for log in result["logs"]:
        if log["topics"][0] == "0xdf91f7709a30fda3fc5fc5dc97cb5d5b05e67e193dccaaef3cb332d23fda83d1":
            wallet = log["topics"][3][-40:]  # Wallet of the delegator
            if len(log["data"]) >= 194:
                amount_hex = log["data"][130:194]  # Third value (bytes 128 to 192)
                amount = int(amount_hex, 16)  # Convert to decimal
            break
    
    return tx_hash, wallet, amount

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

# Generate the report for BEAM stakes
def generate_report(beam_stakes):
    # Prepare data for the report
    stake_data = {}
    for tx_hash, wallet, amount in beam_stakes:
        if wallet:
            if wallet not in stake_data:
                stake_data[wallet] = []
            stake_data[wallet].append({"transaction": hide_address(tx_hash), "amount": amount})
    
    # Structure the report
    report = {
        "stakes_per_wallet": [],
        "validator_stake": VALIDATOR_STAKE,
        "total_beam": 0
    }
    total_beam = 0
    for wallet, stakes in stake_data.items():
        total = sum(stake["amount"] for stake in stakes)
        entry = {
            "wallet": hide_address(f"0x{wallet}"),
            "stakes": stakes,
            "total_beam": total
        }
        report["stakes_per_wallet"].append(entry)
        total_beam += total
    
    # Add the validator's BEAM (if provided)
    total_beam += VALIDATOR_STAKE
    report["total_beam"] = total_beam

    # Print the report
    log_message("BEAM Stakes Report:")
    for entry in report["stakes_per_wallet"]:
        log_message(f"Wallet: {entry['wallet']}")
        for stake in entry["stakes"]:
            log_message(f"Transaction: {stake['transaction']}, BEAM: {stake['amount']}")
        log_message(f"Total BEAM: {entry['total_beam']}")
        log_message("---")
    if VALIDATOR_STAKE > 0:
        log_message(f"Validator Stake: {VALIDATOR_STAKE} BEAM")
        log_message(f"Total BEAM (including validator): {report['total_beam']}")
    else:
        log_message(f"Validator Stake: Not provided")
        log_message(f"Total BEAM (delegated stakes only): {report['total_beam']}")

    # Save to JSON file
    with open(JSON_FILE, "w") as f:
        json.dump(report, f, indent=4)
    
    log_message(f"Report saved to: {JSON_FILE}")

# Main
processed_txs = set()
last_block = 0
beam_stakes = []  # List of (tx_hash, wallet, amount)

log_message("Starting query for BEAM stakes...")
latest_block = get_latest_block()
logs = get_logs(0, "latest")

for log in logs:
    tx_hash = log["transactionHash"]
    if tx_hash not in processed_txs:
        # Query BEAM stakes
        stake_tx, stake_wallet, amount = get_beam_stake_details(tx_hash)
        if stake_wallet and amount > 0:
            beam_stakes.append((stake_tx, stake_wallet, amount))
            log_message(f"BEAM stake - Transaction: {hide_address(stake_tx)}, Wallet: {hide_address(f'0x{stake_wallet}')}, BEAM: {amount}")
        
        processed_txs.add(tx_hash)

# Generate the report
generate_report(beam_stakes)
log_message(f"Last block processed: {latest_block}. Script completed.")
