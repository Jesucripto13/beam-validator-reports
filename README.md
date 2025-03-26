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
