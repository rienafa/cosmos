class Ibc:
	def __init__(self,blockchain):
		# possède les denom_traces ! 
		self.blockchain  	= blockchain
		self.denom_traces  	= self.info()


	def channels(self):
		request = f"query ibc channel channels --output json "
		a =  self.blockchain.request(request)
		return a 

	def info(self):
		# je modifie le fichier ! 
		request = f"query ibc-transfer denom-traces --output json --limit 10000"
		denom_traces = self.blockchain.request(request)['denom_traces']
		#result = {b: [{'ibc_denom': ibc_denom(d), **d} for d in denom_traces if d['base_denom'] == b] for b in set(d['base_denom'] for d in denom_traces)}
		result =  {ibc_denom(d): d for d in denom_traces}
		return result
	
	def __ibc_transfer(self,to_blockchain,amout):
		denom = amount['denom']
		amount = amount['amount']
		channel = IBC[self.name][to_blockchain.name]
		adress = wallet.adress[f'{to_blockchain.name}']
		request = f" tx ibc-transfer transfer  transfer {channel} {adress} {amount}{denom} --from {wallet.name} " 
		# je peux envoyer un memo 
		print(f"IBC transfer {self.blockchain.name} ===> {to_blockchain.name}")
		balance_asset_out = self(to_blockchain).balance()
		self.blockchain.execute(tx)
		received = False
		while not received:
			time.sleep(6)
			new_balance_asset_out = self(to_blockchain).balance()
			if new_balance_asset_out == balance_asset_out:
				received = True
		return False
	
	def wait(self,to_blockchain):
		return False 
	

	def ibc_transfer(self,to_blockchain,amount,memo = ""):
		# ici amount 
		# ici je veux un plus gros type de message 
		# amount {'amount': amount, 'denom' : denom}
		denom = amount['denom']
		amount = amount['amount']
		channel = IBC[self.name][to_blockchain.name]
		adress = wallet.adress[f'{to_blockchain.name}']
		request = f" tx ibc-transfer transfer  transfer {channel} {adress} {amount}{denom} --from {wallet.name} " 
		print(f"IBC transfer {self.blockchain.name} ===> {to_blockchain.name}")
		# ici je veux identifier l'asset de retour c'est asset(to_blockchain)
		if denom in self.blockchain.token:
			channel 	= IBC[to_blockchain.name][self.blockchain.name]
			path    	= {'path' : f"transfer/{channel}", 'base_denom': denom }
			new_denom 	= ibc_denom(path)
		else:
			new_denom = self.blockchain.denom_traces[denom]['base_denom']
		try:
			transfer_asset_amount = {b['denom'] : b['amount'] for b in to_blockchain.balances()}[new_denom]
		except:
			transfer_asset_amount = 0
		# request est un tx ! pas une demande
		request = f"{request} --memo '{json.dumps(memo)}' "
		self.blockchain.execute(request)
		received = false
		# c'est ici que le temps est ! 
		while not received:
			print(f"query {to_blockchain.name}")
			time.sleep(10)
			try:
				new_taa = {b['denom'] : b['amount'] for b in to_blockchain.balances()}[new_denom]
			except:
				new_taa = 0
			if int(new_taa) - int(transfer_asset_amount) == int(amount):
				print("transfer received")
				received = true
				return False

				amount = {'denom' : new_denom,'amount' : amount}
				bc = to_blockchain
				to_blockchain = input("nouveau transfer des fonds ? ")
				if to_blockchain not in Blockchains.instances_by_name.keys():
					return False
				to_blockchain = Blockchains.instances_by_name[to_blockchain]
				bc.ibc_transfer(to_blockchain,amount)
		return False  
	    # pour retrouver l'ibc du token 
	    # IBC['osmosis']['comdex']   87 
	    # c'est dans le cas où denom est native de la bc de départ  
	    # ibc_denom({'path' : 'transfer/channel-87','denom' : 'ucmdx'})
	