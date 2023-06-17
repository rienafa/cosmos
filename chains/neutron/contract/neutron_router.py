import copy
class neutron_router(contract):
	
	def __init__(self,blockchain,adress):
		contract.__init__(self,blockchain,adress)
		self.operation_message = {
        						"astro_swap": {
          							"offer_asset_info": {
            								"native_token": {"denom": ""}},
          							"ask_asset_info": {
          							         "native_token": {"denom": ""}}
        									  }
      							}
		self.message = {
  				"execute_swap_operations": {
    					"operations": [
    					],
    					"minimum_receive": "5518149"
  						}
				}

	def operation_management(self,asset_in,asset_out):
		operation = copy.deepcopy(self.operation_message)
		operation['astro_swap']['offer_asset_info']['native_token']['denom'] = asset_in.denom()
		operation['astro_swap']['ask_asset_info']['native_token']['denom'] = asset_out.denom()
		return operation

	def swap(self,asset_in,asset_out,amount):
		# TODO gestion du min_receive 
		operation1 = self.operation_management(asset_in,NTRN)
		operation2 = self.operation_management(NTRN,asset_out)
		message = copy.deepcopy(self.message)
		message["execute_swap_operations"]['operations'] = [operation1,operation2]
		return message

neutron_router_adress = "neutron1eeyntmsq448c68ez06jsy6h2mtjke5tpuplnwtjfwcdznqmw72kswnlmm0"
NEUTRON_ROUTER = neutron_router(NEUTRON,neutron_router_adress)


