class contract:
	def __init__(self,blockchain,adress):
		self.blockchain = blockchain
		self.adress 	= adress 
		# self.name   	= name

	def get_adress(self):
		return self.adress 
	
	#def get_name(self):
	#	return self.name
	
	def request(self,message):
		# message au format json
		request = f"query wasm contract-state smart {self.adress} '{json.dumps(message)}'"
		result = self.blockchain.request(request)
		return result

	def execute(self,transaction,amount):
		transaction = f"tx wasm execute {self.adress} '{json.dumps(transaction)}' --amount {amount} --from wallet"
		return self.blockchain.execute(transaction)