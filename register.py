"""
Le module d'enregistrement
Est utilisé pour enregistrer des utilisateurs

"""
import json
import os
from hashlib import sha512

#### Basics
def open_json(path:str) -> dict:
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_json(data:dict, path:str) -> None:
    with open(path, "w") as f:
        return json.dump(data, f, indent=4)



#### Informations

"""
base user list :

{
    "user1":{
        "password":"pass hash",
        infos
    },
    
    "user2":{
        "password":"pass hash",
        infos
    }
}



"""


def get_all_user() -> dict:
    """Fonction qui renvoie tous les utilisateurs
    """
    data = open_json("./users.json")
    
    #initialiser la liste
    if data == None:
        save_json({}, "./users.json")
        data = {}
        
    return data

def user_exist(user:str) -> bool:
    return user in get_all_user().keys()




#### Créer les Exceptions

class UserExist(Exception):
    def __init__(self, *args):
        super().__init__(*args)




def register(user:str, password:str):
    """Fonction qui enregistre un utilisateur

    Args:
        user (str): Le nom d'utilisateur
        password (str): Le mot de passe non hashé

    Raises:
        UserExist: Si l'utilisateur existe déjà
    """
    
    #regarder si l'utilisateur existe
    if user_exist(user):
        raise UserExist

    #ajouter l'utilisateur à la liste
    user_list = get_all_user()
    
    user_list[user]={
        # est ce que sha512 est bien trop pour un simple stockage de mots de passes ? Oui, mais mon nombre favori c'est 512 donc tant pis.
        "password": sha512(password.encode("utf-8")).hexdigest()
    }
    
    save_json(user_list, "./users.json")
    