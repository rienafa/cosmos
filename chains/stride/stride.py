class Stride(Blockchains): 
	def __init__(self):
		Blockchains.__init__(self,"stride")

	def __repr__(self):
		return f"The {self.name} blockchain controller"

	def redemption_rate(self):
		query = "q stakeibc list-host-zone"
		return self.request(((query)))['host_zone']

STRIDE = Stride()
wallet.add_adress('stride','stride1kg0w2utlkcsca62cq7f2ke477z442e0dgv4lv4')