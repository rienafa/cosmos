class Protos:
    def __init__(self,blockchain):
        ### uniquement pour osmosis c'est bien pourri !
        self.blockchain = blockchain
        self.tx = {
                    'body': {
                            'messages': [],
                            'memo': '',
                            'timeout_height': '0',
                            'extension_options': [],
                            'non_critical_extension_options': []
                            },
                    'auth_info': {
                                'signer_infos': [],
                                'fee': {'amount': [{'denom': "uosmo", 'amount': "6250"}],
                                'gas_limit': '250000',
                                'payer': '',
                                'granter': ''}},
                    'signatures': []
                    }
        self.file = f"{BASE_FILE}file"
    def add_message(self,message):
        # message est au formet proto
        self.tx['body']["messages"].append(message["body"]["messages"][0])
        return true
    def sign(self,wallet = wallet):
        # ecriture du message contenu dans self dans le fichier
        with open(f"{BASE_FILE}/file/sign_message.json","w+") as file:
            json.dump(self.tx,file)
            file.close()
        b = self.blockchain.execute(f"tx sign  {BASE_FILE}/file/sign_message.json --from {wallet.name} --chain-id {self.blockchain.chain} --output-document {BASE_FILE}/file/signed_message.json --gas auto")
        return b 
    def sign_and_execute(self,wallet = wallet):
        a  =  self.sign(wallet)
        attempt = 0
        while attempt <2:
            try:
                a =self.blockchain.execute(f"tx broadcast {BASE_FILE}/file/signed_message.json --chain-id {self.blockchain.chain} --output json > {BASE_FILE}/file/reponse.json")
                return a
            except:
                attempt = attempt+1
                continue
        # analyse le log si besoin, ca peut etre bon mais chiant 
        print(result)
        return result