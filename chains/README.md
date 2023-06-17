Pour la création d'une chaine. 
Le principe est un peu chiant et je ne sais pas comment automatiser le truc.  La procédure est à faire une seul fois mais c'est un peu chiant ... 
* installation du logiciel de la chaine ```chain``` dont le logiciel s'appelle ```chaind``` ... faut aller voir dans le github de la chain en question (je donne les instructions pour la chaine ``` crescent ``` dans le readme global.  
* importation de la seed dans le keyring du logiciel dans un terminal  entrée ``` chaind keys add wallet --recover ```
* entrer la seed phrase et le mot de passe (le même pour toute les chaines) d'accès à keyring.
* créer un répertoire ```chain```
* créer des fichiers ```importations``` et ```chain``` comme dans les différents modèle en remplacant ```YOUR_ADRESS``` par l'adresse associé à la seed phrase.
* modifier dans le fichier ``` importation.py ``` à la base du répertoire ``` list_of_supported_chain ``` pour y ajouter la nouvelle chaine.

* tout ça va créer une variable ``` CHAIN ``` (si la chaine s'appelle ``` alphonse ``` une variable ``` ALPHONSE ``` est créer pour accéder à la chaîne avec certaines méthode générique implémenter, ``` CHAIN.balances() ``` ou encore ```CHAIN.ibc_tranfer ... ```
* Ca va également créer un nom de variables pour les différents token de la chain.
* 
