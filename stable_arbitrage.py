# construction du graphe stable. 

stable      = [IST,CMST,AXLUSDC,GUSDC]
blockchains = [AGORIC,AXELAR,CRESCENT,COMDEX,GRAVITY]

graph_of_stable = DiGraph()
for asset in stable:
    graph_of_stable.add_vertex(asset.denom())
    for blockchain in blockchains:
        if not asset.host_chain == blockchain:
            graph_of_stable.add_vertex(asset(blockchain).denom())
            graph_of_stable.add_edge(asset.denom(),asset(blockchain).denom(),'ibc')
            graph_of_stable.add_edge(asset(blockchain).denom(),asset.denom(),'ibc')
    for asset_out in stable:
        if not asset == asset_out and CRESCENT.pool_exist(asset(CRESCENT),asset_out(CRESCENT)):
            graph_of_stable.add_edge(asset(CRESCENT).denom(),asset_out(CRESCENT).denom(),'POOL')
for asset in stable: 
    if not( asset(COMDEX) == CMST) and not (asset(COMDEX) == IST(COMDEX) ):
        graph_of_stable.add_edge(asset(COMDEX).denom(),CMST.denom(),"VAULT")
        graph_of_stable.add_edge(CMST.denom(),asset(COMDEX).denom(),"VAULT")

# ici si je pouvais inclure IST VAULT 

pi = graph_of_stable.all_paths_iterator(
            starting_vertices=[CMST.denom()], 
            ending_vertices=[CMST.denom()], 
            report_edges=True, 
            simple=True,
            max_length =15 ,
            labels=True)
PATH = list(pi)

def to_path(data):
    R = []
    for p in data:
        a,b,c = p
        R.append(Asset.instances_by_denom[a])
    a,b,c = data[len(data)-1]
    R.append(Asset.instances_by_denom[b])
    return Path(R) 


def is_valide(T):
    for i in range(len(T) - 2):
        if T[i] == T[i + 2]:
            return False
    return True
LIST_OF_PATH = []
for _path in PATH:
    path = to_path(_path)
    if is_valide(path.chain):
        LIST_OF_PATH.append(path)
def running(_amount):
    CRESCENT.liquidity()
    amount = 0
    win    = 0 
    path   = 0 
    for _path in LIST_OF_PATH:
        data  = _path.swap_data(_amount)
        if data['amount'] > 0 and data['win'] > win:
            amount = data['amount']
            win    = data['win']
            path   = _path
    print(float(win / 10**6))
    return {'path' : path, 'amount' : amount, 'win' : win }



### il faut améliorer le liquidateur comdex, en mode war 