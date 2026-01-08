# Informations
Ceci est le programme coté serveur pour le jeu de [bataille-navale](https://github.com/Hubblle/bataille-navale).

## Architecture
Le programme est divisé en plusieurs fichiers organisés de cette manière:

```
.
├── game.py # Fonction de management des
│
├── login.py # Authentification des utilisateurs
│
├── original_game.py # Jeu original pour les fonctions
│
├── register.py # Enregistrement des utilisateurs
│
├── server.py # Fichier principale du serveur
│
└── users.json # Dictionnaire des utilisateurs
```

Le serveur tourne sur le port `5005/TCP` sur toutes les ip (`0.0.0.0` dans la config), le port est ouvert en écoute avec un serveur http fournie par l’application Flask (il n'est en théorie pas recommandé pour de la production d'utiliser le serveur intégré à Flask, mais cela est bien suffisant pour les besoins de ce projet)

Le serveur joue un role de REST-API (Representational State Transfer).

## Endpoints
Voici une liste de tous les endpoint ouvert sur l'API et leur action;

| Endpoint                	| Methods    	| Role                                                                           	|
|-------------------------	|------------	|--------------------------------------------------------------------------------	|
| `/users`                  	| `GET` + `POST` 	| `GET`: Retourne le nom de l'utilisateur connecté / `POST`: Création d'utilisateur  	|
| `/login `                 	| `GET` + `POST` 	| `GET`: Retourne si l'utilisateur est connecté / `POST`: Demande d'authentification 	|
| `/games`                  	| `GET` + `POST` 	| `GET`: Retourne la liste des parties / `POST`: Création de partie                  	|
| `/game/<string:game_id>`  	| `GET`        	| Retourne le status général de la partie spécifiée                              	|
| `/infos/<string:game_id>` 	| `GET`        	| Retourne les informations d'une partie et de ses utilisateurs                  	|
| `/join/<string:game_id> ` 	| `GET`        	| Rejoin la partie spécifiée                                                     	|
| `/play/<string:game_id>`  	| `POST`       	| Reçois les données de jeu pour les traiter                                     	|

# Hébergement "officiel"

Le lien utilisé dans le code est `https://api.nsi.quark-dev.com/` en effet, c'est une instance du serveur hébergée sur mes serveur, elle tourne derrière un reverse proxy Caddy (bon management des certificats ssl automatiquement à partir du fournisseur "Let's encrypt"), c'est donc la raison pour la quel cet URL ci est en https, sur le port 443, et aussi la raison de la présence des headers `"X-Real-IP"` (le code ne va pas fonctionner sur une machine sans cela à moins de modifier les partie du code qui en dépendes)