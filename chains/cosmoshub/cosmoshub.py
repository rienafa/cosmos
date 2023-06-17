class Cosmoshub(Blockchains): 
	def __init__(self):
		Blockchains.__init__(self,"cosmoshub")

	def __repr__(self):
		return f"The {self.name} blockchain controller"
		
COSMOSHUB = Cosmoshub()
wallet.add_adress('cosmoshub','YOUR_ADRESS')