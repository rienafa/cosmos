class Banks:
	def __init__(self,blockchain):
		self.blockchain 	 		= blockchain
	

	def send_(self,to_adress,amount,wallet = wallet):
		request = f" tx bank send {wallet.name} {to_adress} {amount['amount']}{amount['denom']} "
		result = self.blockchain.execute(request)
		return result


	def balances(self, wallet = wallet):
		blockchain_adress = wallet.adress[self.blockchain.name]
		request =f"  query bank balances {blockchain_adress} --output json "
		balances = self.blockchain.request(request)
		return balances['balances']

	def balance(self,wallet = wallet):
		b = self.balances()
		balance = {}
		for a in b:
			balance[a['denom']] = a['amount']
		return balance