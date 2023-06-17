import json 
import time 
import os

### variables pour les dossiers

BASE_FILE = "Cosmos2.0/"
CONFIG    = f"{BASE_FILE}/configuration"
CHAINS    = f"{BASE_FILE}/chains"

# initialisation 

attach(f"{CONFIG}/importation.py")

# installation des chaines

list_of_supported_chain = ["osmosis","axelar","neutron","cosmoshub","comdex","gravity","crescent","agoric"]

for chain in list_of_supported_chain:
	attach(f"{CHAINS}/{chain}/importation.py")

### configuration des assets 

attach(f"{CONFIG}/assets/assets.py")
attach(f"{BASE_FILE}app/swap.py")

