def cosmic_swap(asset_in,asset_out,amount_in):
    # validation  
    blockchain_in    = asset_in.host_chain
    blockchain_out   = asset_out.host_chain 
    if blockchain_in == blockchain_out:
        print(f'swap {asset_in.symbol} for {asset_out.symbol} in {blockchain_in.name}')
        return blockchain_in.swap(asset_in,asset_out,amount_in)
    else:
        amount = {'amount' : amount_in,'denom' : asset_in.denom()}
        return blockchain_in.ibc_transfer(blockchain_out,amount)

