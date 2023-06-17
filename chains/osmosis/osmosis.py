class Osmosis(Blockchains): 

    def __init__(self):
        Blockchains.__init__(self,"osmosis")
        self.static_pools   = self.pools()

    def __repr__(self):
        return f"The {self.name} blockchain controller"

    def create_pool(self,asset_in,asset_out):
        # ici on va créer une pool virtuelle échangeant asset_in et asset_out en passant par osmo 
        all_pools = ASSET_OSMO
        pool_1 = ASSET_OSMO[asset_in.denom()]
        pool_2 = ASSET_OSMO[asset_out.denom()]
        l_in    = 1 
        l_out   =1
        fee     = 1
        return false
    async def async_liquidity(self):
        await self.liquidity()
    def price(self,asset):
        if asset == OSMO:
            return "not implemented" 
        else:
            return self.swap_estimate(asset,axelar_USDCuusdc(OSMOSIS),1)


    def swap_estimate(self,asset_in,asset_out,amount):
        M = self.swap_matrix(asset_in,asset_out)
        a, b = M * vector([amount,1])
        print("attention a la non gestion des decimals pour l'affichage")
        return float(a/b)


    def pools(self):
        request = "query gamm pools -o json --limit 2000 "
        return self.request(request)['pools']
    
    def pool_matrix(self,asset,_in):
        ### attention  pas mis à jour 
        # ici ça va bug lorsque asset = OSMO
        D = self.read_liquidity()
        a, b = D[asset.denom()]['pool_assets']
        if _in:
            l_in  =  floor(1.003 * int (a['token']['amount']))  
            l_out = int(b['token']['amount'])
        else:
            l_in  = floor(1.003 * int (b['token']['amount']))   
            l_out = int(a['token']['amount'])
        return matrix(ZZ,2,2,[l_out,0,1,l_in])


    def swap_matrix(self,asset_in,asset_out):
        return  self.pool_matrix(asset_out,False) * self.pool_matrix(asset_in,True)



    def ASSET_OSMO(self):
        ASSET_OSMO = {}
        P = OSMOSIS.pools()
        for p in P:
            if p['@type'] == '/osmosis.gamm.v1beta1.Pool':
                pool_liquidity = p['pool_assets']
                if pool_liquidity[1]['token']['denom'] == "uosmo":
                    denom = pool_liquidity[0]['token']['denom']
                    if denom in ASSET_OSMO.keys():
                        old_pool = ASSET_OSMO[denom]
                        old_pool_liquidity =  old_pool['pool_assets']
                        if int((old_pool_liquidity[1]['token']['amount'])) < int(pool_liquidity[1]['token']['amount']):
                            ASSET_OSMO[denom] = p 
                    else:
                        ASSET_OSMO[denom] = p
        return ASSET_OSMO


    def cross_chain_swap(self,asset_in,asset_out,amount):
        # EVMOS(COMDEX)  ---->  USDC(COMDEX)
        if asset_in.is_native:
            channel = IBC[f'{asset_in.host_chain.name}']['osmosis']
            adress = 'osmo1uwk8xc6q0s6t5qcpr6rht3sczu6du83xq8pwxjua0hfj5hzcnh3sqxwvxs'
            tx = f"tx ibc-transfer transfer  transfer {channel} {adress} {amount}{asset_in.denom()} --from {wallet.name} "
            memo = {} 
            wasm = {}
            wasm['contract'] =  'osmo1uwk8xc6q0s6t5qcpr6rht3sczu6du83xq8pwxjua0hfj5hzcnh3sqxwvxs'
            msg =  { 

                    'osmosis_swap': 
                     {
                        'output_denom': f'{asset_out(OSMOSIS).denom()}',
                        'slippage': {'twap': {'slippage_percentage': '20', 'window_seconds': 10}},
                        'receiver': wallet.adress[asset_out.native_chain.name],
                        'on_failed_delivery': 'do_nothing'
                    }
                    }
            if not asset_out.is_native():
                channel = IBC[asset_out.native_chain.name][asset_out.host_chain.name]
                next_memo = {
                                "forward": {
                                "receiver": wallet.adress[asset_out.host_chain.name],
                                "port": "transfer",
                                "channel": channel  
                                }
                            }
                msg['osmosis_swap']['next_memo'] = next_memo
            wasm['msg'] = msg
            memo['wasm'] = wasm
            tx = tx + f" --memo '{json.dumps(memo)}' " 
            return asset_in.host_chain.execute(tx)
        else:
            return "not implemented"
            



    def liquidity(self):
        D = self.ASSET_OSMO()
        with open(f"{BASE_FILE}chains/{self.name}/liquidity.json","w+") as file:
            json.dump(D,file)
        return False


    def read_liquidity(self):
        with open(f"{BASE_FILE}chains/{self.name}/liquidity.json","r+") as file:
            a =  json.loads(file.read())
            return a

    def swap(self,asset_in,asset_out,amount_in):
        # c'est bof bof ! 
        # calcul de amount_out
        # calcul precis et splipage
        amount_out = '1'  # plus sérieux ! 
        _in  = asset_in(self)
        _out = asset_out(self)
        ### routes = 
        routes = []
        routes.append(
            {
                "poolId" : ASSET_OSMO[_in.denom()]['id'],
                "tokenOutDenom": "uosmo"
            })
        routes.append(
            {
                "poolId" : ASSET_OSMO[_out.denom()]['id'],
                "tokenOutDenom": f"{_out.denom()}"  
            })
        tokenIn = {
                "denom": _in.denom(),
                "amount": str(amount_in)
            }
        tokenOutMinAmount = str(amount_out)
        message = osmosis_swap()
        message.set_message(routes,tokenIn,tokenOutMinAmount)
        proto = Protos(self)
        proto.tx['body']['messages'] = [message.message]
        return proto.sign_and_execute()

OSMOSIS = Osmosis()
# dictionnaire avec osmo pool. 

P = OSMOSIS.static_pools

# non car il peut y en avoir plusieurs 
# ASSET_OSMO = { pool['pool_liquidity'][0]['denom'] : pool for pool in P if pool['pool_liquidity'][1]['denom'] == 'uosmo'}

ASSET_OSMO = {}
### dictionnaire des pools
### enregistrer en dur l'id ? 




for p in P:
    if p['@type'] == '/osmosis.gamm.v1beta1.Pool':
        pool_liquidity = p['pool_assets']
        if pool_liquidity[1]['token']['denom'] == "uosmo":
            denom = pool_liquidity[0]['token']['denom']
            if denom in ASSET_OSMO.keys():
                old_pool = ASSET_OSMO[denom]
                old_pool_liquidity =  old_pool['pool_assets']
                if int((old_pool_liquidity[1]['token']['amount'])) < int(pool_liquidity[1]['token']['amount']):
                    ASSET_OSMO[denom] = p 
            else:
                ASSET_OSMO[denom] = p


### vérouillage du truc ??? fee control ? 
###  WHITE LISTING  
#WHITE_LIST_ASSET_OSMO = {denom : pool for denom,pool in ASSET_OSMO.items() if Asset.instances_by_denom[denom] in WHITE_LIST}


wallet.add_adress("osmosis",'osmo1kg0w2utlkcsca62cq7f2ke477z442e0druxnwt')


### mettre dans un autre dossier
def  pool_matrix(A,B,f_A):
    return matrix(ZZ,2,2,[B,0,1,int(f_A * A)])