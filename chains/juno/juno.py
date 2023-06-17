class Juno(Blockchains):
    def __init__(self):
        Blockchains.__init__(self,"juno")

    def __repr__(self):
        return f"The {self.name} blockchain controller"
JUNO_bc = Juno()
wallet.add_adress('juno','juno1kg0w2utlkcsca62cq7f2ke477z442e0da4kcl9')