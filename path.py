class Path:
    def __init__(self,chain):
        self.chain = chain

    def matrice(self):
        M = matrix(ZZ,2,2,[1,0,0,1])
        for k in range(len(self.chain)-1):
            asset_in        = self.chain[k]
            asset_out       = self.chain[k+1]
            blockchain_in   = asset_in.host_chain 
            blockchain_out  = asset_out.host_chain 
            if (blockchain_in == blockchain_out):
                M = blockchain_out.swap_matrix(asset_in,asset_out) * M 
        return M

    def __repr__(self):
        chain_repr = ", ".join(asset.__repr__() for asset in self.chain)
        return chain_repr

    def swap_data(self,amount):
        M = self.matrice()
        t = M.trace()
        de = M.det() 
        A,B = M 
        a,b = A 
        c,d = B
        if c ==0:
            return { 'amount' : amount, 'win' : 0} 
        else:
            x_opt = int((sqrt(de) - d)/c)
        if amount < x_opt:
            return {'amount' : amount, 'win' : int((a*amount+b) / (c*amount+d) - amount)}
        else:
            return { 'amount' : int(x_opt), 'win' : int((t- 2*sqrt(de) )/ c)} 


    def execute(self,amount): 
        for k in range(len(self.chain)-1):
            asset_in = self.chain[k]
            asset_out = self.chain[k+1]
            # ici je vais faire une balance local 
            balance_out = asset_out.balance()
            print(f"etape {k}")
            print(f"balance {asset_out} ::: {balance_out}")
            cosmic_swap(asset_in,asset_out,amount)
            if (asset_in.host_chain == asset_out.host_chain):
                new_balance_out = asset_out.balance()
                print(f"balance {asset_out} ::: {new_balance_out}")
                amount = int(new_balance_out) - int(balance_out)
        return False






