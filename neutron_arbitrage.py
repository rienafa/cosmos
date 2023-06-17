graph_of_asset = DiGraph()
assets = [AXLUSDC,ATOM,NTRN]
chains = [NEUTRON,ATOM,OSMOSIS,AXELAR]

# FONCTION DE CREATION DES CHANNELS IBC 

def ibc_graph_of_assets(assets,chains):
	graph_of_asset = DiGraph()
	for asset in assets:
    	graph_of_stable.add_vertex(asset.denom())
    	for blockchain in chains:
        	if not asset.host_chain == blockchain and blockchain in IBC[asset.host_chain].keys(): 
            	graph_of_asset.add_vertex(asset(blockchain).denom())
            	graph_of_asset.add_edge(asset.denom(),asset(blockchain).denom(),'ibc')
            	graph_of_asset.add_edge(asset(blockchain).denom(),asset.denom(),'ibc')
    return graph_of_asset
