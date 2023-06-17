class Gravitybridge(Blockchains): 
	def __init__(self):
		Blockchains.__init__(self,"gravitybridge")
		self.prefix = "G"

	def __repr__(self):
		return f"The {self.name} blockchain controller"

### sur gravity on peut vendre les rewards 

GRAVITY = Gravitybridge()
wallet.add_adress('gravitybridge','gravity1kg0w2utlkcsca62cq7f2ke477z442e0d0h8ma3')