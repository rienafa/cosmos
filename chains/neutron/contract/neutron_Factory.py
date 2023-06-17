import asyncio
import subprocess

class factory(contract):
    # factory contract astroport neutron 
    def __init__(self,blockchain,adress):
        contract.__init__(self,blockchain,adress)
    
    def config(self):
        config_message = {"config": {}}
        return self.request(config_message)

    def pairs(self):
        # pour demander les différentes pairs et pouvoir instancier les pools. 
        request = {"pairs": {"limit": 1000}}
        return self.request(request)['data']['pairs']

factory_adress = "neutron1hptk0k5kng7hjy35vmh009qd5m6l33609nypgf2yc6nqnewduqasxplt4e"
NEUTRON_FACTORY = factory(NEUTRON,factory_adress)