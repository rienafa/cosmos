Pour la création d'une chaine. 
Le principe est un peu chiant et je ne sais pas comment automatiser le truc.  La procédure est à faire une seul fois mais c'est un peu chiant ... 
* installation du logiciel de la chaine ```chain``` dont le logiciel s'appelle ```chaind``` ... faut aller voir dans le github de la chain en question (je donne les instructions pour la chaine ``` crescent ``` dans le readme global.  
* importation de la seed dans le keyring du logiciel dans un terminal  entrée ``` chaind keys add wallet --recover ```  le flag --recover veut dire qu'on va importer une seed phrase déjà créer, si on veux une nouvelle seed phrase on peut enlever ```--recover ```.  
* entrer la seed phrase et le mot de passe (le même pour toutes les chaines) d'accès à keyring.
* créer un répertoire ```chain```
* créer des fichiers ```importations``` et ```chain``` comme dans les différents modèle en remplacant ```YOUR_ADRESS``` par l'adresse associé à la seed phrase.
* modifier dans le fichier ``` importation.py ``` à la base du répertoire ``` list_of_supported_chain ``` pour y ajouter la nouvelle chaine.

Ensuite il faut ouvrir un terminal ```sage ``` en entrant sage dans un terminal. Et lancer l'importation ``` attach("NON_DU REPERTOIRE_INSTALLATION/importation.py") ``` 
* tout ça va créer une variable ``` CHAIN ``` (si la chaine s'appelle ``` alphonse ``` une variable ``` ALPHONSE ``` est créer pour accéder à la chaîne avec certaines méthode générique implémenter, ``` CHAIN.balances() ``` ou encore ```CHAIN.ibc_tranfer ... ```
* Ca va également créer un nom de variables pour les différents token de la chain.

```
defi@penguin:~$ PATH="/home/defi/axelar-core/bin/:$PATH"   ### faire gaffe aux variables d'environnement  
defi@penguin:~$ sage
┌────────────────────────────────────────────────────────────────────┐
│ SageMath version 9.2, Release Date: 2020-10-24                     │
│ Using Python 3.9.2. Type "help()" for help.                        │
└────────────────────────────────────────────────────────────────────┘
sage: attach("Cosmos2.0/importation.py")  ### ca prend un peu de temps car il y a des requètes RPC 
sage: CRESCENT
The crescent blockchain controller
sage: AXELAR
The axelar blockchain controller
sage: OSMOSIS
The osmosis blockchain controller
sage: COMDEX
The comdex blockchain controller
```
