class Axelar(Blockchains):
    def __init__(self):
        Blockchains.__init__(self,"axelar")
        self.prefix = "AXL"

    def __repr__(self):
        return f"The {self.name} blockchain controller"
    ### blockchain centrale dans l'univers mais juste comme ibc transporteur 
    ### est-ce que je peux faire des forwards ? 


AXELAR = Axelar()
wallet.add_adress('axelar','axelar1kg0w2utlkcsca62cq7f2ke477z442e0d0frtnc')