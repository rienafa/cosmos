class Crescent(Blockchains): 
	def __init__(self):
		Blockchains.__init__(self,"crescent")
		self.POOLS   =  self.pools()

	def __repr__(self):
		return f"The {self.name} blockchain controller"

	def pools(self):
		# il faut raffiner le truc !
		request = "q liquidity pools --limit 1000"
		list_of_pool = self.request(request)['pools']
		### on va manager 
		pools = {}
		for p in list_of_pool:  # il faut controler mieux que ça faire une classe CrescentPools 
			if p['id'] in ['29','28']:
				continue
			name = p['balances']['base_coin']['denom'] +"__"+p['balances']['quote_coin']['denom']
			if name in pools.keys():
				if int(p['balances']['base_coin']['amount']) > int(pools[name]['balances']['base_coin']['amount']):
					pools[name] = p 
			else:
				pools[name] = p
		return pools

	def pool_exist(self,asset,asset_out):
		pool ,DIRECTION = self.assets_to_pool(asset,asset_out)
		return not pool == {}


	def liquidity(self):
		D = self.pools()
		with open(f"{BASE_FILE}chains/{self.name}/liquidity.json","w+") as file:
			json.dump(D,file)
		return False


	def read_liquidity(self):
		with open(f"{BASE_FILE}chains/{self.name}/liquidity.json","r+") as file:
			a =  json.loads(file.read())
			return a


	
	def assets_to_pool(self,asset_in,asset_out):
		D 	 = self.read_liquidity()
		try:
			name = asset_in.denom()+"__"+asset_out.denom()
			pool = D[name]
			DIRECTION = "SELL"
		except:
			try:
				name = asset_out.denom()+"__"+asset_in.denom()
				pool = D[name]
				DIRECTION = "BUY"
			except:
				DIRECTION = "NO POOL"
				pool      = {}
		return pool, DIRECTION



	def swap_matrix(self,asset_in,asset_out):
		try:
			name = asset_in.denom()+"__"+asset_out.denom()
			D = self.read_liquidity()
			pool = D[name]
			DIRECTION = "SELL"
		except:
			try:
				name = asset_out.denom()+"__"+asset_in.denom()
				pool = D[name]
				DIRECTION = "BUY"
			except:
				DIRECTION ="NO"
				return 1 
		Lq = int(pool['balances']['quote_coin']['amount'])
		Lb = int(pool['balances']['base_coin']['amount'])
		if pool['type'] == 'POOL_TYPE_RANGED':
			p  = float(pool['price'])
			min_price = float(pool['min_price'])
			L = float(Lq / (sqrt(p) -sqrt(min_price)))
			l_in =  int(L * sqrt(p)) 
			l_out = int(L / sqrt(p))
		else:
			l_in 	= Lq 
			l_out 	= Lb 
		if DIRECTION == "SELL":
			return matrix(ZZ,2,2,[l_in,0,1,l_out])
		if DIRECTION =="BUY":
			return matrix(ZZ,2,2,[l_out,0,1,l_in])


	"""
		Là c'est pour les pools concentrées uniquement. 
		faire pareil pour les pools classiques ! 

		price et amount c'est toujours par rapport à base 
	"""

	def swap(self,asset_in, asset_out,amount):
		#### il faut tester le produit !!! 
		pool, DIRECTION  = self.assets_to_pool(asset_in,asset_out)
		asset_in_denom  = asset_in.denom()
		asset_out_denom = asset_out.denom()
		a_sell = amount 
		# amount = int(amount / 1.0035)
		M = self.swap_matrix(asset_in,asset_out)
		a , b = M * vector([amount,1])
		amount_out = int(a / b) 
		# le price est le prix en sorti du truc !  
		# pas le prix moyen ! 
		L = float(sqrt(det(M)))
		if DIRECTION =="BUY":
			# amount_in = (p_t - p) * L 
			# p = pool.price 
			# p_t = amount_in / L + p 
			price = float(pool['price'])
			price =  (float(amount / L + sqrt(price)))**2 *1.002  ### ici 
			_price = float(amount / amount_out)
			amount_out = int(amount /  price)
			# ici ça force à avoir un peu plus donc pas bon !
			#amount = int(1.0035 * amount)
			# comdex tx liquidity limit-order [app-id] [pair-id] [direction] [offer-coin] [demand-coin-denom] [price] [amount] [flags]
			tx = f' tx liquidity limit-order {pool["pair_id"]} {DIRECTION} {amount}{asset_in_denom} {asset_out_denom} '
			price = '{:.15f}'.format(price)
			tx = tx + f"{price} {int(amount_out)} --from wallet"
		if DIRECTION == "SELL":
			price = float(pool['price'])
			amount = a_sell
			# le nouveau prix de la pool 
			price = (float(amount / L + 1/sqrt(price)))**(-2) 
			tx = f' tx liquidity limit-order {pool["pair_id"]} {DIRECTION} {int(amount)}{asset_in_denom} {asset_out_denom} '
			price = '{:.15f}'.format(price)
			tx = tx + f"{price } {amount} --from wallet"
		return self.execute(tx),tx


	def stable_pools(self):
		stable_pools = []
		pools = self.pools()
		for p in pools:
			try:
				# attention bug potentiel instance_by_denom n'est pas bijective 
				base  =  Asset.instances_by_denom[p['balances']['base_coin']['denom']]
				quote =  Asset.instances_by_denom[p['balances']['quote_coin']['denom']]
			except:
				continue
				# dans la classe asset attribut stable
			if base.stable and quote.stable:
				print(base)
				print(quote)
				stable_pools.append(p)
		return stable_pools

	def information(self):
		P = self.stable_pools()
		information = ""
		for p in P:
			base  =  Asset.instances_by_denom[p['balances']['base_coin']['denom']]
			quote =  Asset.instances_by_denom[p['balances']['quote_coin']['denom']]
			information = information + f" {base.nickname} / {quote.nickname} : {p['price']} \n"
		return information


CRESCENT = Crescent()
wallet.add_adress('crescent','cre1kg0w2utlkcsca62cq7f2ke477z442e0d00xxd5')