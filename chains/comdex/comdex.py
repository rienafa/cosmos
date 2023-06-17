class Comdex(Blockchains): 
	def __init__(self):
		Blockchains.__init__(self,"comdex")
		self.vaults  = self.Vaults()

	def __repr__(self):
		return f"The {self.name} blockchain controller"

	### comdex est un dex donc fonction de swap et matrice de génération
	### fonction liquidity() et read liquidity

	def pools(self):
		request = "query liquidity pools 1 -o json"
		# modification pour avoir une unique pool ? 
		list_of_pool = self.request(request)['pools']
		pools = {}
		for p in list_of_pool:
			if  (p['type'] ==  'POOL_TYPE_BASIC'):
				name = p['balances']['base_coin']['denom'] +"__"+p['balances']['quote_coin']['denom']
				pools[name] = p
		return pools

	def Vaults(self):
		### vraiment de la merde !!! 
		request = "query asset extended-pair-data-stable-vault-wise 2"
		vaults =  self.request(request)['extended_pair']
		### modification 
		d = {'1' : '1', '8' : "2", '21' : '3', '28' : '4'}
		name_to_denom = {
			'AXL-USDC-CMST' : "ibc/E1616E7C19EA474C565737709A628D6F8A23FF9D3E9A7A6871306CF5E0A5341E",
			'AXL-DAI-CMST'  : "ibc/54DEF693B7C4BF171E7FFF3ABFE2B54D6A3B8A047A32BAAE9F1417A378594EC6",
			'GRAV-USDC-CMST': "ibc/50EF138042B553362774A8A9DE967F610E52CAEB3BA864881C9A1436DED98075",
			'GRAV-DAI-CMST' : "ibc/109DD45CF4093BEB472784A0C5B5F4643140900020B74B102B842A4BE2AE45DA"
		}
		_vaults = {}
		for vault in vaults:
			vault['stable_id'] = d[vault['id']]
			_vaults[name_to_denom[vault['pair_name']]] = vault 
		return _vaults

	def liquidity(self):
		D = self.pools()
		with open(f"{BASE_FILE}chains/{self.name}/liquidity.json","w+") as file:
			json.dump(D,file)
		return False


	def read_liquidity(self):
		with open(f"{BASE_FILE}chains/{self.name}/liquidity.json","r+") as file:
			a =  json.loads(file.read())
			return a 

	def price(self,asset):
		D = self.read_liquidity()
		if asset == CMDX:
			name = CMDX.denom()+"__"+CMST.denom()
			return float(D[name]['price'])
		if asset == CMST:
			return 1 
		else:
			try: 
				name = CMST.denom()+"__"+asset.denom()
				return 1 / float(D[name]['price'])
			except:
				name = name = CMDX.denom()+"__"+asset.denom()
				p_cmdx = float(D[name]['price'])
				return self.price(CMDX) / p_cmdx



	def swap_matrix(self,asset_in,asset_out):
		# etre plus soigneux sur les fonctions de swap 
		try:
			name = asset_in.denom() +"__"+ asset_out.denom()
			pool = self.read_liquidity()[name]
			l_in 	= int(1.003 * int(pool['balances']['base_coin']['amount']))
			l_out 	= int(pool['balances']['quote_coin']['amount'])
			return matrix(ZZ,2,2,[l_out,0,1,l_in])
		except:
			try:
				name = asset_out.denom()+"__"+asset_in.denom()
				pool = self.read_liquidity()[name]
				l_in 	= int(1.003 * int(pool['balances']['quote_coin']['amount']))
				l_out 	= int(pool['balances']['base_coin']['amount'])
				return matrix(ZZ,2,2,[l_out,0,1,l_in])
			except:
				DIRECTION = "VAULT"
				### y'a un petit imperfection ici 
				return matrix(ZZ,2,2,[999,0,0,1000])

	def limite_buy_test(self,asset_in,asset_out,amount_in):
		try:
			name = asset_out.denom()+"__"+asset_in.denom()
			D = self.read_liquidity()
			pool = D[name]
			DIRECTION = "BUY"
			price = float(pool['price'])
			L_in  = int(pool['balances']['quote_coin']['amount'])
			price_ = price
			amount_in = int(amount_in / 1.0035)
			alpha = 1 + amount_in /  L_in
			price =   price  * alpha**2 * 1.001
			B = int(pool['balances']['base_coin']['amount'])
			amount = int(B* (1-1/alpha) )
			# amount = f'{int(amount_in / (1.0031 *  price_))}'
			tx = f' tx liquidity limit-order 1 {pool["pair_id"]} {DIRECTION} {int(1.0035*amount_in)}{asset_in.denom()} {asset_out.denom()} '
			price = '{:.15f}'.format(price)
			tx = tx + f"{price} {int(amount/1.001)} --from wallet"
			return self.execute(tx)
		except:
			print("que passa")
			return False

	def swap(self,asset_in,asset_out,amount_in):
		### je pense que c'est pas bon 
		# comprendre la logique 
		### Pour la dircetion BUY  ex  CMST ---> CMDX
		### Le price c'est le price de CMDX / CMST, mon ordre va faire monter le prix !
		###  soit alpha tel que alpha B = B + b' où b' = (amount_in /1.003) 
		### alors price = alpha**2 * price
		try:
			name = asset_in.denom() +"__"+ asset_out.denom()
			pool = self.read_liquidity()[name]
			DIRECTION = "SELL"
			amount = int(amount_in / 1.0031)-1
			price = float(pool['price'])
			s = 1-0.05
			price = s * price 
			tx = f" tx liquidity limit-order 1 {pool['pair_id']} {DIRECTION} {amount_in}{asset_in.denom()} {asset_out.denom()}"
			price = '{:.15f}'.format(price)
			tx = tx +f" {price} {amount} --from wallet "
			# "[app-id] [pair-id] [direction] [offer-coin] [demand-coin-denom] [amount]"
			return self.execute(tx)
		except:
			try:
				name = asset_out.denom()+"__"+asset_in.denom()
				D = self.read_liquidity()
				pool = D[name]
				DIRECTION = "BUY"
				### control du prix ? 
				price = float(pool['price'])
				# c'est puant ça, vraiment !
				# je dois pouvoir faire un truc très clean exact 
				s = 1 + 0.05
				price = float(s * price)
				amount = f'{int(amount_in / (1.004*price))}'
				# comdex tx liquidity limit-order [app-id] [pair-id] [direction] [offer-coin] [demand-coin-denom] [price] [amount] [flags]
				tx = f' tx liquidity limit-order 1 {pool["pair_id"]} {DIRECTION} {amount_in}{asset_in.denom()} {asset_out.denom()} '
				price = '{:.15f}'.format(price)
				tx = tx + f"{price} {amount} --from wallet"
				return self.execute(tx)
			except:
				# faut être un peu plus precis
				# le problème c'est s'il n'y a plus de machin ! 
				DIRECTION = "VAULT"
				amount_in = max(amount_in,10**6)
				if (asset_in == CMST(COMDEX)):
					action = "withdraw-stable-mint"
					vault  = self.vaults[asset_out.denom()]
				else:
					action =  "deposit-stable-mint"
					vault = self.vaults[asset_in.denom()]
				tx = f" tx vault {action} 2 {vault['id']} {amount_in} {vault['stable_id']} --from wallet "
				return self.execute(tx)



COMDEX = Comdex()

###  enregistrement de l'adresse 
wallet.add_adress("comdex",'YOUR_ADRESS')

