class Terra(Blockchains): 
	def __init__(self):
		Blockchains.__init__(self,"terra2")
		#self.cache_balance = self.balances()
		self.gas_adj = 2

	def __repr__(self):
		return f"The {self.name} blockchain controller"
TERRA = Terra()
wallet.add_adress('terra2','terra1e0995t30fuvx69w4kxu080xmhwf5d5m2r33vn0')