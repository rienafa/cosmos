class Agoric(Blockchains):
    def __init__(self):
        Blockchains.__init__(self,"agoric")

    def __repr__(self):
        return f"The {self.name} blockchain controller"

    ### il faudrait integrer les liquidations et les vaults mais je ne sais pas comment faire. 
    
AGORIC = Agoric()
wallet.add_adress('agoric',"YOUR_ADRESS")