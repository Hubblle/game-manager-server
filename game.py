"""
Module utilisé pour la gestion des parties de jeu

"""

from flask import session
from uuid import uuid4

#### Exceptions

#### Game class

class Game():
    def __init__(self, creator, uuid):
        self.creator = creator
        self.uuid = uuid
        self.full = False




# Variables

#Le dictionnaire qui contiens toutes les parties
games = {}



def create_game():
    """Cette fonction est utilisée pour créer une partie
    """
    
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
    