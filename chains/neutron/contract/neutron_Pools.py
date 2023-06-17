class neutron_pools(contract):
    # la pool est un contrat spécifique
    instances =[]
    instances_by_name = {}
    def __init__(self,blockchain,data):
        contract.__init__(self,blockchain,data['contract_addr'])
        self.data = data
        self.__class__.instances.append(self)
        self.base = data['asset_infos'][0]['native_token']['denom']
        self.quote = data['asset_infos'][1]['native_token']['denom']
        self.name  = self.base+"__"+self.quote
        self.__class__.instances_by_name[self.name] = self
        
    def info(self):
        message = {"info"  :{}}
        return self.request(message)

    def liquidity(self):
        # ici je ne sais pas trop le asyncio run
        message = {"pool": {}}
        result = self.request(message)
        return result

    def swap(self,asset_in,amount):
        tx = {"swap":{
                     "offer_asset": {
                        "info": {"native_token": {"denom": asset_in.denom()}},
                        "amount": str(amount)
                        }
                    }
            }
        self.execute(tx,str(amount)+asset_in.denom())

    async def async_liquidity(self):
        message = {"pool": {}}
        request =  f"query wasm contract-state smart {self.adress} '{json.dumps(message)}'"
        ### ici je veux dans NEUTRON
        return  await self.blockchain.async_request(request)

NEUTRON_PAIRS  = NEUTRON_FACTORY.pairs()
for p in NEUTRON_PAIRS:
    neutron_pools(NEUTRON,p)