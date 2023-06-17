class Juno(Blockchains):
    def __init__(self):
        Blockchains.__init__(self,"juno")

    def __repr__(self):
        return f"The {self.name} blockchain controller"
JUNO_bc = Juno()
wallet.add_adress('juno','YOUR_ADRESS')