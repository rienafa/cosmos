class Cosmoshub(Blockchains): 
	def __init__(self):
		Blockchains.__init__(self,"cosmoshub")

	def __repr__(self):
		return f"The {self.name} blockchain controller"
		
COSMOSHUB = Cosmoshub()
wallet.add_adress('cosmoshub','cre1kg0w2utlkcsca62cq7f2ke477z442e0d00xxd5')