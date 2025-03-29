```
# Beam Validator Reports

Scripts to generate node delegation and BEAM stake reports for validators on the Beam network.

## 📢 Mr. Beam: 50% BEAM Rewards Shared! 100% Uptime, Top-Ranked 💰

Delegate to **Mr. Beam**—a top validator on the @Beam network with 100% uptime! 🚀 Earn more with 50% of validator profits shared, low 1% fees, and full transparency.

**Why Choose Mr. Beam?**  
🟦 **Top Reliability:** 100% uptime, ranked among the best validators.  
🟥 **Higher Earnings:** 50% of validator profits in BEAM shared with delegators.  
🟨 **Low Fees:** Only 1% commission on rewards.  
🟩 **Full Transparency:** Clear tracking of delegations and payouts.

**How It Works:**  
Delegate to Mr. Beam and receive 1 BEAM within 24 hours to confirm eligibility for extra rewards. Enjoy standard rewards + 50% of my BEAM profits, distributed transparently.

🔍 **Find Us:** Search "Mr. Beam" or use NodeID: `GvYGeH3hZrX751Ppzzaee5YiqM1EcJhxT`  
📲 **Telegram:** [t.me/beamvalidator](https://t.me/beamvalidator)  
🐦 **X:** [x.com/JesucryptoX](https://x.com/JesucryptoX)  
📩 **Contact:** [t.me/JesucryptoX](https://t.me/JesucryptoX)

---

## Overview

These scripts allow you to generate reports for node delegations and BEAM stakes for your validator on the Avalanche network. They are designed to run manually, print the results to the console, and save the data to JSON files (`nodes_report.json` and `stakes_report.json`).

- `generate_nodes_report.py`: Generates a report of node delegations.
- `generate_stakes_report.py`: Generates a report of BEAM stakes.

## Prerequisites

- Python 3 installed on your system.
- The `requests` library installed (`pip install requests`).
- Access to an Avalanche node running on `http://127.0.0.1:9650/ext/bc/2tmrrBo1Lgt1mzzvPSFt73kkQKFas5d1AP88tv9cicwoFp8BSn/rpc`.

## 📋 How to Use the Scripts

### 1. Download the Scripts
Download `generate_nodes_report.py` and `generate_stakes_report.py` from this repository.

### 2. Configure the Scripts
To use the scripts, you need to set the `NODE_ID` with your validator's hexadecimal identifier. Follow these steps to obtain it:

4. Update the Instructions in README.md

The info.getNodeID method provides a more direct way to obtain the public key and derive the NODE_ID, so let’s update the instructions in README.md to prioritize this method. We will also keep the other options as alternatives.

⸻

Updated Section of README.md (English Version)

2. Configure the Scripts

To use the scripts, you need to configure the NODE_ID with your validator’s hexadecimal identifier (a 32-byte hexadecimal value). This identifier is derived from your node’s public key. Follow these steps to obtain it:

⸻

Step 2.1: Obtain Your Node’s Public Key

1. Use the info.getNodeID Method (Recommended Method)
	•	Use the info.getNodeID method to obtain the nodeID and your node’s public key:

curl -X POST --data '{ "jsonrpc":"2.0", "id":1, "method":"info.getNodeID", "params":{}}' \
-H 'Content-Type: application/json' 127.0.0.1:9650/ext/info

The response will include the nodeID and publicKey, for example:

{
    "jsonrpc": "2.0",
    "result": {
        "nodeID": "NodeID-GvYGeH3hZrX751Ppzzaee5YiqM1EcJhxT",
        "nodePOP": {
            "publicKey": "0xab88a86...2860e6c0756ea7355b2ceaf",
            "proofOfPossession": "..."
        }
    },
    "id": 1
}



⸻

Step 2.2: Derive the NODE_ID from the Public Key

Use the following Python script to compute the SHA-256 hash of the public key:

import hashlib

# Instructions: Replace with your public key (without the 0x prefix)
public_key_hex = "INSERT_YOUR_PUBLIC_KEY_HERE"
public_key_bytes = bytes.fromhex(public_key_hex)
node_id = hashlib.sha256(public_key_bytes).hexdigest()
print(f"Hexadecimal value to use in the scripts: 0x{node_id}")

The result will be a 32-byte hexadecimal value (e.g., 0x571ac781c64ab162b8c2c22ba49cb3dbe62e7be62d1e78f274346bd3a7dbb856).

#### Step 2.3: Set the `NODE_ID` in the Scripts
1. Open the scripts `generate_nodes_report.py` and `generate_stakes_report.py` in a text editor.
2. Find the line:
   ```python
   NODE_ID = "INSERT_PUBLIC_NODE_IDENTIFIER_HERE"
   ```
3. Replace it with the hexadecimal value you obtained, for example:
   ```python
   NODE_ID = "0x571ac781c64ab162b8c2c22ba49cb3dbe62e7be62d1e78f274346bd3a7dbb856"
   ```
4. (Optional) In `generate_stakes_report.py`, set `VALIDATOR_STAKE` to the amount of BEAM staked by your validator. If left as 0, the total BEAM will only include delegated stakes.

### 3. Run the Scripts
- Run the node delegations report:
  ```bash
  python3 generate_nodes_report.py
  ```
- Run the BEAM stakes report:
  ```bash
  python3 generate_stakes_report.py
  ```

### 4. View the Results
- The scripts will print the results to the console.
- Two JSON files will be generated: `nodes_report.json` (node delegations) and `stakes_report.json` (BEAM stakes).

### 5. Share the Reports
- Share the generated JSON files with your community by uploading them to a file-sharing service (e.g., Google Drive, Dropbox) and sharing the links.

## Notes
- The scripts hide wallet addresses and transaction hashes for privacy (showing only the first 6 and last 4 characters).
- The scripts run once and terminate, making them suitable for manual execution.
- Ensure your Avalanche node is running and accessible at the specified URL.
- This process does not require your validator server to be public or to install anything on it.
- If you have trouble running the Python script, ensure you have Python 3 installed on your local machine (`python3 --version`) and that you have installed the `base58` library.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
