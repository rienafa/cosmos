class Wallets:
	def __init__(self,name):
		self.name   = name
		self.adress = {}
	def add_adress(self,name,adress):
		# faire plus automatique 
		self.adress[name] = adress
wallet = Wallets("wallet")
