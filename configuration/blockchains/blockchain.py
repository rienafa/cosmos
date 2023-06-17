class Blockchains(__Blockchains__,Ibc,Banks):  
	# j'integre deux modules IBC et BANKS 
	instances_by_name = {}
	def __init__(self,*args):
		__Blockchains__.__init__(self,*args)
		Ibc.__init__(self,self)
		Banks.__init__(self,self)
		self.__class__.instances_by_name[self.name] = self