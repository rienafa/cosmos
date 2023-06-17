class  Neutron(Blockchains): 
    def __init__(self):
        Blockchains.__init__(self,"neutron")

    def __repr__(self):
        return f"The {self.name} blockchain controller"
    ### dans blockchain !

    async def async_request(self,request):
        process   = await asyncio.create_subprocess_shell(f"{self.command}  {request}  {self.node} --chain-id {self.chain} -o json", stdout=subprocess.PIPE)
        output, _ = await process.communicate()
        try:
            a = json.loads(output.decode().strip())
        except:
            a = {}
        return a

    ### fonctionnalité de dex 

    def liquidity(self):
        # ce n'est pas très propre  
        async def _liquidity():
            resultats = {}
            tasks = []
            pools = neutron_pools.instances
            for pool in pools:
                task = asyncio.create_task(pool.async_liquidity())
                tasks.append(task)
            for task in asyncio.as_completed(tasks):   
                resultat = await task
                resultat = resultat
                if resultat != {}:
                    # algo de formation de la pool 
                    resultat = resultat['data']['assets']
                    base, quote = resultat
                    base_name   = base['info']['native_token']['denom']
                    quote_name  = quote['info']['native_token']['denom']
                    resultats[base_name+"__"+quote_name] = {base_name : int(base['amount']),
                    quote_name : int(quote['amount'])}
            return resultats
        D = asyncio.run(_liquidity())
        with open(f"{BASE_FILE}chains/{self.name}/liquidity.json","w+") as file:
            json.dump(D,file)
    
    def read_liquidity(self):
        with open(f"{BASE_FILE}chains/{self.name}/liquidity.json","r+") as file:
            a =  json.loads(file.read())
            return a

    def swap(self,asset_in,asset_out,amount):
        # pour swap. 
        # il faut recupérer la pool associée
        D = self.read_liquidity()
        try:
            name = asset_in.denom()+"__"+asset_out.denom()
            pool = neutron_pools.instances_by_name[name]
        except:
            try:
                name = asset_out.denom()+"__"+asset_in.denom()
                pool = neutron_pools.instances_by_name[name]
            except:
                return "NO"
        pool.swap(asset_in,amount)
        return False


    def swap_matrix(self,asset_in,asset_out):
        D = self.read_liquidity()
        try:
            name = asset_in.denom()+"__"+asset_out.denom()
            l = D[name]
        except:
            try:
                name = asset_out.denom()+"__"+asset_in.denom()
                l = D[name]
            except:
                assert 0 == 1
        l_in  = int(l[asset_in.denom()] * 1.003)
        l_out = l[asset_out.denom()]
        return matrix(ZZ,2,2,[l_out,0,1,l_in])  

### deux pools sur astroport neutron ! 

NEUTRON = Neutron()
wallet.add_adress('neutron','YOUR_ADRESS')