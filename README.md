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

## Steps to Use

1. **Download the Scripts:**
   - Download `generate_nodes_report.py` and `generate_stakes_report.py` from this repository.

2. **Configure the Scripts:**
   - In both scripts, replace `INSERT_PUBLIC_NODE_IDENTIFIER_HERE` with your validator's public node identifier (a hex string like `0x...` that was published in the transaction where the validator was registered).

## 📋 How to Obtain the PUBLIC_NODE_IDENTIFIER for the Scripts

To use the scripts `generate_nodes_report.py` and `generate_stakes_report.py`, you need to set the `NODE_ID` with your validator's hexadecimal identifier. Follow these steps to obtain it:

### Step 1: Obtain Your `validationID`
2.1. On your server where your Avalanche node is running, execute the following command in the terminal, replacing `INSERT_YOUR_NODE_ID_HERE` with your `nodeID` (e.g., `NodeID-GvY...hxT`):
   
   curl -X POST --data '{"jsonrpc": "2.0", "method": "validators.getCurrentValidators", "params": {"nodeIDs": ["INSERT_YOUR_NODE_ID_HERE"]}, "id": 1}' -H 'content-type:application/json;' 127.0.0.1:9650/ext/bc/2tmrrBo1Lgt1mzzvPSFt73kkQKFas5d1AP88tv9cicwoFp8BSn/validators

In the response, look for the validationID value. For example:
"validationID": "fMyGzmMY...UYEeme"
Copy this value.

Step 2: Convert the validationID to Hexadecimal
Create a file named decode_validation_id.py with the following code:

import base58

# Instructions: Replace the value of validation_id with the validationID you obtained from the curl command
validation_id = "INSERT_YOUR_VALIDATION_ID_HERE"

# Decode Base58 to bytes
decoded = base58.b58decode(validation_id)

# Extract the payload (the 32 bytes after the prefix and before the checksum)
payload = decoded[12:-4].hex()

# Print the hexadecimal value to use in the scripts
print(f"Hex value to use in the scripts: 0x{payload}")

Install the base58 library:

pip install base58

Open the decode_validation_id.py file and replace INSERT_YOUR_VALIDATION_ID_HERE with the validationID you obtained (e.g., fMyGzmMY...UYEeme).
Run the script:

python3 decode_validation_id.py

The output will be the hexadecimal value to use in the scripts. For example:

Hex value to use in the scripts: 0x571ac...dbb856

Set the NODE_ID in the Scripts
Open the scripts generate_nodes_report.py and generate_stakes_report.py in a text editor.
Find the line:
NODE_ID = "INSERT_PUBLIC_NODE_IDENTIFIER_HERE"

Replace it with the hexadecimal value you obtained, for example:
NODE_ID = "0x571ac...dbb856"


   - In `generate_stakes_report.py`, optionally set `VALIDATOR_STAKE` to the amount of BEAM staked by your validator. If left as 0, the total BEAM will only include delegated stakes.

3. **Run the Scripts:**
   - Run the node delegations report:
     python3 generate_nodes_report.py
     
   - Run the BEAM stakes report:
     python3 generate_stakes_report.py

4. **View the Results:**
- The scripts will print the results to the console.
- Two JSON files will be generated: `nodes_report.json` (node delegations) and `stakes_report.json` (BEAM stakes).

5. **Share the Reports:**
- Share the generated JSON files with your community by uploading them to a file-sharing service (e.g., Google Drive, Dropbox) and sharing the links.

## Notes

- The scripts hide wallet addresses and transaction hashes for privacy (showing only the first 6 and last 4 characters).
- The scripts run once and terminate, making them suitable for manual execution.
- Ensure your Avalanche node is running and accessible at the specified URL.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
