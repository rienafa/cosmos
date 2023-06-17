class Gravitybridge(Blockchains): 
	def __init__(self):
		Blockchains.__init__(self,"gravitybridge")
		self.prefix = "G"

	def __repr__(self):
		return f"The {self.name} blockchain controller"

### sur gravity on peut vendre les rewards 

GRAVITY = Gravitybridge()
wallet.add_adress('gravitybridge','YOUR_ADRESS')