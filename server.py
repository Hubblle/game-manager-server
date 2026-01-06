from flask import Flask, request, session
import register
import logging
import login
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
        
    elif request.method == "DELETE":
        #Dé-authentifie l'utilisateur (marche aussi pour vider les cookies)
        
        for key in session.keys():
            session[key] == ""
        return "Successfully unlogged"


if __name__ == '__main__':
    print("done")
    app.run(host="0.0.0.0",port=5005)
    
