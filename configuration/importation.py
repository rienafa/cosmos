CONFIG = f"{BASE_FILE}configuration"


### gestion wallet 
attach(f"{CONFIG}/wallet/wallets.py")

### base blockchain
attach(f"{CONFIG}/blockchains/__blockchain__.py") 


#### modules 

### IBC
attach(f"{CONFIG}/ibc/IBC.py")
attach(f"{CONFIG}/ibc/ibc_tools.py")
attach(f"{CONFIG}/ibc/ibc.py")

### BANK 
attach(f"{CONFIG}/bank/bank.py")


### BLOCKCHAINS
attach(f"{CONFIG}/blockchains/blockchain.py")
attach(f"{CONFIG}/contract/contract.py")

### PROTO 
attach(f"{CONFIG}/proto/protos.py")


### ASSET 
attach(f"{CONFIG}/assets/ASSETS.py")

