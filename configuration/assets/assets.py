class Asset:
    
    instances_by_id = {}
    instances_by_denom = {}

    """
    principe : un asset a une blockchain native et une blockchain host (par exemple OSMO on COMDEX)
    ========
               On dispose de variable OSMO etc pour les assets, et également COMDEX pour les blockchains
               OSMO(COMDEX) représente l'asset OSMO sur la blockchain COMDEX.

               l'id represente un ajout  de l'ibc denom qui va permettre d'identifier chaque asset de manière 
               unique. 
               pour les noms d'asset il me reste un problème avec les assets d'axelar qui amène de 
               l'ucdc d'avalanche. drop du fichier ?!? 

    """


    def __init__(self,name,host_chain,native_chain,symbol):
        self.name           = name
        self.host_chain     = host_chain
        self.native_chain   = native_chain
        self.symbol         = symbol
        self.nickname       = self.native_chain.prefix + self.symbol
        if self.is_native():
            self.id = self.name 
        else:
            denom = self.denom()
            ibc,denom = denom.split("/")
            ibc = self.host_chain.name 
            self.id  = ibc+"/"+denom
        self.__class__.instances_by_id[self.id] = self
        self.__class__.instances_by_denom[self.denom()] = self


    def __repr__(self):
        return self.nickname + f"({self.host_chain.name.upper()})"


    def is_native(self):
        return self.host_chain.name == self.native_chain.name

    def balance(self):
        try:
            return self.host_chain.balance()[self.denom()]
        except:
            return '0'

            
    def denom(self):
        if self.is_native():
            return self.name
        path = {'path' : "transfer/"+IBC[self.host_chain.name][self.native_chain.name] , 'base_denom' : self.name }
        return ibc_denom(path)


    def transfer(self,to_chain):
        if to_chain == self.native_chain:
            return self.instances_by_id[self.name]
        channel = IBC[to_chain.name][self.native_chain.name]
        path = {
            'path' : "transfer/"+channel, 'base_denom' : self.name 
        }
        ibc = ibc_denom(path)
        ibc = ibc.replace('ibc/',f'{to_chain.name}/')
        return self.instances_by_id[ibc]


    def __call__(self,to_chain):
        return self.transfer(to_chain)



for native in Blockchains.instances_by_name.values():
    for asset in ASSET[native.name].keys():
        for host in Blockchains.instances_by_name.values():
            pre     = native.prefix
            symbol  =  ASSET[native.name][asset]['symbol']
            print(symbol)
            print(asset)
            if (native.name == host.name):
                locals()[pre+symbol] = Asset(asset,host,native,symbol)
            else:
                try:
                    Asset(asset,host,native,symbol)
                except:
                    continue