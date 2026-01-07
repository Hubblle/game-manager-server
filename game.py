"""
Module utilisé pour la gestion des parties de jeu

"""

from flask import session
from uuid import uuid4
import original_game

#### Exceptions
class GameAlreadyExist(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        
class GameDontExist(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class GameFull(Exception):
    def __init__(self, *args):
        super().__init__(*args)


#### Game class

class Game():
    def __init__(self, creator, uuid):
        
        self.uuid = uuid
        self.full = False
        self.turn = 0 #Variable utilisée pour compter le nombres de tours d'une partie
        self.next_turn = creator #Variable qui contiendra le prochain joueur
        self.win = [False]
        
        self.creator = {
                "name":creator,
                "ship" : [],
                "hit" : [],
                "sank_ship": [],
                "score" : 0
                    }
        
        
        self.opponent =  {
                "name":"",
                "ship" : [],
                "hit" : [],
                "sank_ship": [],
                "score" : 0
                    }
        
        
    def play(self, infos:dict, creator=False)->str:
        """Fonction qui permet de jouer un tour d'une partie, elle va calculer ce qu'il faut et retourner les informations à transmettre au clients

        Args:
            infos (dict): Les informations envoyées par le client
            creator (bool, optional): Si l'utilisateur est le créateur. False par défaut.
        """
        
        if self.turn < 2:
            if creator:
                self.creator["ship"] = infos.get("ship", [])
                self.turn += 1
                return ""
            
            
            else:
                self.opponent["ship"] = infos.get("ship", [])
                self.turn += 1
                return ""
                
        if self.next_turn != session.get("username", "") or infos["name"] != session.get("username", ""):
            return ""
        
        shot = infos["shot"]
        user = self.creator if creator else self.opponent
        opponent = self.creator if not creator else self.opponent
        
        
        if original_game.eval_shot(opponent["ship"], user, shot):
            shot[0] = True
            user["hit"].append(shot)
            
            #Actualiser le score
            user["score"] = original_game.get_score(opponent["ship"],user["hit"])
            
            if original_game.has_win(opponent["ship"],user["hit"]):
                self.win = [True, user]
                return "win"
            
            elif original_game.eval_sank_ships(opponent["ship"], user):
                return "sank"
            
            else:
                return "touched"
            
            
        else:
            shot[0] = False
            user["hit"].append(shot)
            self.turn += 1
            self.next_turn = opponent
            return "miss"
        
            
        

    def is_creator(self):
        """Fonction qui utilise les données de la session pour renvoyer si l’utilisateur actuel est le créateur de la partie
        """
        #Récupérer le pseudo dans la session
        username = session.get("username", "")
        
        if not username:
            return False
        
        return self.creator["name"] == username
        



# Variables

#Le dictionnaire qui contiens toutes les parties
games = {}



def create_game():
    """Cette fonction est utilisée pour créer une partie
    """
    #Verifier que l'utilisateur n'a pas déjà une partie en cours, si oui, on ferme la partie si elle n'est pas pleine
    idx = ""
    for id, game in games.items():
        if game.creator == session.get("username", None):
            if game.full:
                raise GameAlreadyExist
            idx = id     
    
    if idx:
       games.pop(idx)
                
    
    
    #Donner un id à la partie
    game_id = str(uuid4())
    
    game_creator = session.get("username", None)
    
    if game_creator == None:
        return
    
    #créer la partie
    game = Game(game_creator, game_id)
    
    games[game_id] = game
    session["game_id"] = game_id
    return game
    
    
def list_games()->dict:
    """Une fonction pour lister toutes les parties en cours 

    Returns:
        dict: Un dict qui peut être envoyée au client
    """
    liste = {}
    
    
    for game in games.keys():
        if not games[game].full:
            liste[game] = games[game].creator["name"]
    
    return liste
    
    
def get_status(game_id:str):
    """Cette fonction renvoie le status générale d'une partie
    """
    
    #Regardez si la partie existe
    game = games.get(game_id, None)
    
    if game == None:
        return {}
    
    game_status={
        "full":game.full,
        "creator":game.creator["name"],
        "opponent":game.opponent["name"]
    }
    
    return game_status
    

def get_infos(game_id:str):
    """Cette fonction renvoie les infos de jeu d'une partie
    """
    
    #Regardez si la partie existe
    game :Game = games.get(game_id, None)
    
    if game == None:
        return {}


    game_infos = {
        game.creator["name"]: game.creator,
        game.opponent["name"]: game.opponent,
        "next_turn": game.next_turn,
        "turn":game.turn,
        "win":game.win
    }
    
    return game_infos


def join_game(game_id:str):
    """Fonction qui permet à un utilisateur de rejoindre une partie
    """
    
    username = session.get("username", None)
    
    if username == None:
        return
    
    #regarder si la partie existe
    game = games.get(game_id, None)
    
    if game == None:
        raise GameDontExist
    
    if game.full == True:
        raise GameFull
    
    session["game_id"] = game_id
    game.opponent["name"] = username
    game.full = True