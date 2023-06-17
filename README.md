# instructions :
* utilisation de python et de sagemaths (bibliothèque mathématique sous python) https://www.sagemath.org/fr/telecharger.html (j'utilise sagemaths pour avoir des fonctionnalités d'algébre, de theories des graphes etc ... et c'est juste que j'ai l'habitude de sage.  
* Récupération de chain-registry (que je n'arrive pas à inclure dans mon dossier) :  ``` git clone https://github.com/cosmos/chain-registry ``` et il faut que  le dossier ``` chain-registry ``` soit au même niveau que les autres sous-répertoire que les répertoires de ce dossier (rohhh la phrase de merde :)
* Dans le fichier : ``` importation.py ``` il y a une variable ``` BASE_FILE = "Cosmos2.0/" ``` il faut remplacer ```Cosmos2.0 ``` par le nom du dossier racine où le truc est installer. 
* Dans le fichier : ``` importation.py ``` il y a une variable ``` list_of_supported_chain ``` où l'on peut ajouter des chains cosmos. Je donne la démarche pour installer une chaine particulière.
  * ``` list_of_supported_chain = ['crescent'] ```
  * installation du logiciel de la chain : par exemple pour la chaine Crescent (regarder le github de crescent pour voir la préocédure que j'ai récopié ici : https://github.com/crescent-network/crescent. 
    ``` 
        git clone https://github.com/crescent-network/crescent.git
        cd crescent && git checkout release/v5.0.x
        make install 
    ```
  * création d'une adresse : ``` crescentd keys add wallet ```   (wallet c'est le nom du wallet) normalement il faut enregistrer un mot de passe pour l'accès à keyring et bien entendu (stoker) la seed phrase. 
  * Dans le fichier ```chains/crescent``` a la fin du fichier, il y a une ligne ``` wallet.add_adress('crescent','YOUR_ADRESS') ``` il faut remplacer ``` YOUR_ADRESS ``` par l'adresse ``` cre... ```
  *  Normalement la chain ```CRESCENT ``` est prète.
* Pour tester si tout va bien : dans un terminal ouvrir ``` sage ``` dans le répétoire où est installer le dossier ``` BASE_FILE ```  et ensuite ``` attach("NON_DE_BASE_FILE/importation.py") ```
* Si tout vas bien dans le terminal sage entrée ``` CRESCENT ```  ca doit retourner un truc du style ``` the crescent blockchain controller ```

