class Agoric(Blockchains):
    def __init__(self):
        Blockchains.__init__(self,"agoric")

    def __repr__(self):
        return f"The {self.name} blockchain controller"

    ### il faudrait integrer les liquidations et les vaults mais je ne sais pas comment faire. 
    
AGORIC = Agoric()
wallet.add_adress('agoric','agoric1f0g6v7ujqu579y0nkzx9wl63sclnq23nemted8')
### comment deriver les adresses ? 