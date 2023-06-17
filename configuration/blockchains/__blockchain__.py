class __Blockchains__:
    def __init__(self,name):
        self.name           = name
        self.filepath       = f"{BASE_FILE}/chain-registry/{self.name}/chain.json"
        with open(self.filepath, 'r') as f:
            data = json.load(f)
            self.gas_price = data['fees']['fee_tokens'][0]['average_gas_price']
            self.fee_token = data['fees']['fee_tokens'][0]['denom']
            self.command     = data['daemon_name']
            nodes       = data['apis']['rpc']
            for node_ in nodes:
                if 'Lavender' in node_['provider']:
                    other_node = node_['address']
                if node_['provider'] == 'Polkachu':
                    self.node = " --node " + node_['address']
            if not hasattr(self, 'node'):
                self.node = " --node "+ other_node
            self.chain    = data['chain_id']
            self.token    = list(ASSET[name].keys())
        self.gas_adj      = 1.2
        self.prefix       = ""
    
    # ici je peux gérer la logique des requests si besoin

    def request(self,request):
        return json.loads(os.popen(f"{self.command} {request} {self.node} --chain-id {self.chain} -o json").read())

    
    def execute(self,tx):
        message = f"echo {password} | {self.command} {tx}  {self.node} --chain-id {self.chain} --gas auto --gas-adjustment {self.gas_adj} --gas-prices {self.gas_price}{self.fee_token} --broadcast-mode block"
        a = os.popen(f"{message} -y").read()
        return a