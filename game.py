"""
Module utilisé pour la gestion des parties de jeu

"""

from flask import session
from uuid import uuid4

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
        self.creator = creator
        self.uuid = uuid
        self.full = False
        self.opponent = ""




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
    retrn = {}
    
    
    for game in games.keys():
        if not games[game].full:
            retrn[game] = games[game].creator
    
    return retrn
    
    
def get_status(game_id:str):
    """Cette fonction renvoie le status générale d'une partie
    """
    
    #Regardez si la partie existe
    game = games.get(game_id, None)
    
    if game == None:
        return {}
    
    game_status={
        "full":game.full,
        "creator":game.creator,
        "opponent":game.opponent
    }
    
    return game_status
    

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
    game.opponent = username
    game.full = True