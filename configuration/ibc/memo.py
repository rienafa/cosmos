class Forward:
    # forward et un memo  

    def __init__(self,current_chain,next_chain):
        self.message         = { "forward" : {}}
        self.next_chain      = next_chain
        self.current_chain   = current_chain

    def get_memo(self):
        self.message["forward"] = {
            "receiver" : wallet.adress[self.next_chain.name],
            "port"     : "transfer",
            "channel"  : IBC[self.current_chain.name][self.next_chain.name]
        }
        return self.message

"""
{
                "forward" : {
                        "receiver" : wallet.adress[asset_out.host_chain.name],
                        "port"     : "transfer",
                        "channel"  : IBC[asset_out.native_chain.name][asset_out.host_chain.name]
                    }
                }
"""


