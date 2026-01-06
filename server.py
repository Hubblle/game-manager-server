from flask import Flask, request, session
import register
import logging
import login
import game
import dotenv
import os


#Charge le contenu de ./.env dans les variables d’environnement
dotenv.load_dotenv()

#Créer la clée privée pour le cryptage des cookies
key = bytes(os.getenv("SECRET-KEY"), "utf-8") # Transformation en bytes (c'est le type de data demandé par app.secret_key)

#Créer une instance du serveur en lui donnant le nom "__main__" (par convention on met __name__ comme nom)
app = Flask(__name__)

app.secret_key = key


## Mettre en place les logs
file_logger = logging.FileHandler("./server.log")
## L'ajouter au logger du serveur par défaut
app.logger.addHandler(file_logger)

###### partie gestion utilisateur


@app.route('/users', methods=['POST','GET'])
def user():
    if request.method == "POST":
        #Méthode pour enregistrer un utilisateur
        data = request.form
        username = data.get("username", None)
        password = data.get("password", None)
        if username == None or password == None:
            app.logger.warning(f"[{request.headers.get_all("X-Real-IP")[0]}]: Used a wrong request format !")
            return "wrong input json format, or empty body !"

        try:
            register.register(username, password)
        except register.UserExist:
            app.logger.warning(f"[{request.headers.get_all("X-Real-IP")[0]}]: Tried to register an user wich already exist !")
            return "user already exist !"
        else:
            app.logger.info(f"[{request.headers.get_all("X-Real-IP")[0]}]: Registered a new user ({username})")
            return "user sucessfully added !"
        
    if request.method == "GET":
        #Méthode pour retourner le nom d'utilisateur du cookie de session
        if login.is_logged_in():
            return session.get("username", "")
        else:
            return ""
        
        
        
@app.route("/login", methods=["GET", "POST", "DELETE"])
def route_login():
    if request.method == "GET":
        return str(login.is_logged_in())
    
   
    elif request.method == "POST":
        # Essaye d'authentifier l'utilisateur 
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        try:
            login.login(username, password)
            return "User logged in !"
        except login.UserDontExist:
            app.logger.warning(f"[{request.headers.get_all("X-Real-IP")[0]}]: Tried to login a user who don't exist !")
            return "This user do not exist !"
        except login.WrongPassword:
            app.logger.warning(f"[{request.headers.get_all("X-Real-IP")[0]}]: Used wrong login credentials !")
            return "Wrong login credentials !"


###### partie jeu
@app.route("/games", methods=["GET","POST"])
def games():
    if request.method == "GET":
        return game.list_games()
    
    if request.method == "POST":
        #Essayer de créer une partie
        #Regarder si il y a une connexion valide
        if not login.is_logged_in():
            return "You are not connected !"
        
        try:
            uuid = game.create_game().uuid
        except game.GameAlreadyExist:
            return "A game is already running with your account !"
        return uuid
    
@app.route("/game/<string:game_id>")
def game_endpoint(game_id:str):
    #Retourne le status général de la partie
    return game.get_status(game_id)

@app.route("/join/<string:game_id>")
def join_endpoint(game_id:str):
    if not login.is_logged_in():
        return "You are not connected !"
    
    try:
        game.join_game(game_id)
    except game.GameDontExist:
        return "This game do not exist"
    except game.GameFull:
        return "This game is full"
    
    return "Successfully joined the game !"


if __name__ == '__main__':
    print("done")
    app.run(host="0.0.0.0",port=5005)
    
