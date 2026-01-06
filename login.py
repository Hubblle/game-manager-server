"""
Le module de login
Permet de manager l'authentification des utilisateurs
"""

import json
import os
from flask import session, request
from register import user_exist
from hashlib import sha512



#### Basics
def open_json(path:str) -> dict|None:
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_json(data:dict, path:str) -> None:
    with open(path, "w") as f:
        return json.dump(data, f, indent=4)
    
## Exceptions

class UserDontExist(Exception):
    def __init__(self, *args):
        super().__init__(*args)
    
class WrongPassword(Exception):
    def __init__(self, *args):
        super().__init__(*args)
    
    

def login(username:str, password:str):
    """Fonction qui permet de login un utilisateur

    Args:
        username (str): Le nom d'utilisateur
        password (str): Le mot de passe non hashé 

    Raises:
        UserDontExist: Le nom d'utilisateur ne correspond à aucun utilisateur enregistré
        WrongPassword: Le mot de passe est incorrect
    """
    # l'utilisateur existe ?
    if not user_exist(username):
        raise UserDontExist
    
    user_data = open_json("./users.json")[username]
    
    
    #verifier le mot de passe:
    hash = sha512(password.encode("utf-8")).hexdigest()
    
    
    if not user_data.get("password", "") == hash:
        raise WrongPassword
    
    else:
        #faire la session
        
        #Anti token-grab
        session["ip"] = request.headers.get_all("X-Real-IP")[0].split(":")[0] #Get only the ip not the port
        
        #Ajout du nom d'utilisateur dans le cookie
        session["username"] = username
        
        session["is_active"] = True
        

def is_logged_in() -> bool:
    """Fonction qui verifie si l'utilisateur est authentifié à partir du cookie de session

    Returns:
        bool: Si l'utilisateur est authentifié
    """
    
    #regarder l'ip:
    ip = session.get("ip", None)
    
    #seulement si l'ip existe
    if ip != None:
        if ip != request.headers.get_all("X-Real-IP")[0].split(":")[0]:
            session["is_active"] = False
            return False
    
    #regarder si la session est active
    return session.get("is_active", False)
        
    