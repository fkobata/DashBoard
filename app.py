from flask import Flask, render_template, request, flash, redirect
import json
import requests
from config import Usernameconfig, Contrasenha

app = Flask(__name__)
app.secret_key = 'D@shB0ard'

logado = False
username = ""

log_access = {
    "Configusername": Usernameconfig,
    "ConfigPassword": Contrasenha
}

app.config.update(log_access)


@app.route("/")
def HomeLand():
    return render_template("index.html")

@app.route("/Home", methods=["GET","POST"])
def Home():
        global logado

        login = request.form.get("lgin")
        Pass  = request.form.get("senha")

        if login == app.config.get("Configusername") and Pass == app.config.get("ConfigPassword"):
            return render_template("/administrator.html")
        
        else:
            with open('usuarios.json') as usuariosTemp:
             usuarios = json.load(usuariosTemp)
            
            cont = 0       

            for usuario in usuarios:
        
             cont += 1

            if usuario['username'] == login and usuario['txtsenha'] == Pass:
                username = login
                return render_template("home.html")
            
            if cont >= len(usuarios):
                flash("NÃO AUTORIZADO")
                return redirect("/")

@app.route("/profile")
def profile():
    global logado

    cont = 0

    with open('usuarios.json', encoding='utf-8') as userList:
        ListUser = json.load(userList)
        
        for Lista in ListUser:
            cont += 1
            nList = Lista["username"]
     
    return render_template("profile.html",ListUser=nList)

   
@app.route("/profileCad", methods=["GET","POST"])
def profCad():
    global logado

    profile = []
    firstName = request.form.get("name")
    ult_name = request.form.get("lastName")
    email = request.form.get("mail")
    dateCad  = request.form.get("datetimeCad")
    cpf  = request.form.get("docNum")
    logName  = request.form.get("username")
    passwd  = request.form.get("txtsenha")
    pais  = request.form.get("Country")
    estado  = request.form.get("state")
    cidade  = request.form.get("city")
    Cep  = request.form.get("CEP")
    enderec  = request.form.get("Adress")
    num  = request.form.get("numberAdress")
    phon = request.form.get("phone")

    profile  = [
        {
        "name": firstName,
        "lastName": ult_name,
        "mail": email,
        "datetimeCad": dateCad,
        "docNum": cpf,
        "username": logName,
        "txtsenha": passwd,
        "Country": pais,
        "state": estado,
        "city": cidade,
        "CEP": Cep,
        "Adress": enderec,
        "numberAdress": num,
        "phone": phon
        }
    ]
    newuser = []
    newuser = [
        {
             "username": logName,
             "txtsenha": passwd
        }
    ]
    with open('profile.json') as profileTemp:
        profiles = json.load(profileTemp)

        newProfile = profiles + profile

    with open('profile.json', 'w') as recordTemp:
        json.dump(newProfile,recordTemp, indent=16)


    with open('usuarios.json') as userTemp:
        NewUser = json.load(userTemp)

        newCadUser = newuser + NewUser

    with open('usuarios.json','w') as gravarUser:
        json.dump(newCadUser, gravarUser, indent=4)

        flash("Profile Created!")
    return redirect("/profile")

@app.route("/adm")
def adm():
    if logado == True:
         return render_template("administrador.html")
    if logado == False:        
        return redirect("/")

@app.route("/HomeAdmin",methods=["GET","POST"])
def homeAdmin():
        global logado
        user = []
        Login = request.form.get("lgin")
        Passw = request.form.get("senha")
        user = [
            {
                "username": Login,
                "txtsenha": Passw
            }
        ]
        with open('usuarios.json') as usuariosTemp:
         usuarios = json.load(usuariosTemp)
  
        usuarioNovo = usuarios + user
                
        with open('usuarios.json','w') as gravarTemp:
            json.dump(usuarioNovo, gravarTemp, indent=4)
    
            flash("Success!")
        return redirect("/adm")




if __name__ == "__main__":
    app.run(debug=True)

