import app.IA
import os

from app import app, db, lm
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user

from app.models.forms import LoginForm, RegisterForm, DeleteForm, ReadForm, UpdateForm, RegisterFormReleased, ReadFormReleased, DeleteFormReleased, UpdateFormReleased
from app.models.tables import User, Released
from app.IA import reconhecedor_fisherfaces, captura, treinamento


@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route("/index/<user>", methods=['GET']) #limita os metodos da pagina
@app.route("/index", defaults={"user":None})
@app.route("/", defaults={"user":None})
def index(user):
    return render_template('index.html',
                            user=user) #por padrao busca na pasta "templates"

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash("Logged in!")
            return redirect(url_for("index"))
        else:
            flash("Invalid login!")
    return render_template('login.html',
                            form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))



@app.route("/register", methods=['GET','POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user != None:
            flash("User already exists!")
            return redirect(url_for("index"))
        else:
            #INSERT
            i = User(form.username.data, form.password.data, form.name.data, form.email.data)
            db.session.add(i)
            db.session.commit()
            flash("Registered user!")
            return redirect(url_for("index"))
            
    return render_template('register.html',
                            form=form)

@app.route("/delete", methods=['GET','POST'])
def delete():

    form = DeleteForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user == None:
            flash("User does not exist!")
            return redirect(url_for("index"))
        else:
            #DELETE
            r = User.query.filter_by(username=form.username.data).first()
            released = Released.query.filter_by(user_id=r.id).first()

            while released != None:
                db.session.delete(released)
                released = Released.query.filter_by(user_id=r.id).first()

            db.session.delete(r)
            db.session.commit()
            flash("Deleted user!")
            return redirect(url_for("index"))
            
    return render_template('delete.html',
                            form=form)

@app.route("/update/<user>", methods=['GET', 'POST']) #limita os metodos da pagina
@app.route("/update", defaults={"user":None}, methods=['GET', 'POST'])
def update(user):

    
    if user != None:

        form = UpdateForm()
        #form.username.data = user.username
        if form.validate_on_submit():
            userMod = User.query.filter_by(username=user).first()
            print (user)
            #UPDATE
            userMod.name = form.name.data
            userMod.email = form.email.data
            userMod.password = form.password.data

            db.session.add(userMod)
            db.session.commit()
            flash("User updated!")
            return redirect(url_for("index"))

        return render_template('update.html',
                                form=form)
    else:


        form = ReadForm()
        #form = UpdateForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user == None:
                flash("User does not exist!")
                return redirect(url_for("index"))
            else:
                return redirect(url_for("update", user=user.username))
                
        return render_template('read.html',
                                form=form)
    

@app.route("/read", methods=['GET', 'POST'])
def read():

    form = ReadForm()       

    if form.validate_on_submit():
        
        user = User.query.filter_by(username=form.username.data).first()
        if user == None:
            flash("User does not exist!")
        else:
            
            #READ
            r = User.query.filter_by(username=form.username.data)
            
            return render_template('readAll.html',
                            lista=r)

    return render_template('read.html',
                            form=form)

@app.route("/readAll", methods=['GET', 'POST'])
def readAll():
    lista = User.query.all()
           

    return render_template('readAll.html',
                            lista=lista)
                
@app.route("/monitorar", methods=['GET', 'POST'])
def monitorar():

    #executar o reconhecedor como Thread
    
    reconhecedor_fisherfaces.reconhecedorFisherFaces()

    return redirect(url_for("index"))


@app.route("/whitelist", methods=['GET', 'POST'])
def whitelist():

    print("whitelist")

    return render_template('whitelist.html')

@app.route("/registerReleased/<username>", methods=['GET', 'POST'])
@app.route("/registerReleased", methods=['GET', 'POST'])
def registerReleased(username):

    form = RegisterFormReleased()

    user = User.query.filter_by(username=username).first()

    if form.validate_on_submit():
        released = Released.query.filter_by(cpf=form.cpf.data).first()
        if released != None:
            flash("People already exists!")
            return redirect(url_for("index"))
        else:
            #INSERT
            i = Released(form.name.data, form.cpf.data, user.id)
            db.session.add(i)
            db.session.commit()
            
            released = Released.query.filter_by(cpf=form.cpf.data).first()

            print(released.id)

            statusCaptura = captura.captura(released.id)

            if statusCaptura == "ok":
                treinamento.treinamento()
                flash("Registered people!")
                return redirect(url_for("index"))
            else:
                db.session.delete(released)
                db.session.commit()
                flash("Record interrupted!")
                return redirect(url_for("index"))

    return render_template('registerReleased.html', 
                            form=form)
    
@app.route("/readReleased/<username>", methods=['GET', 'POST'])
@app.route("/readReleased", methods=['GET', 'POST'])
def readReleased(username):

    form = ReadFormReleased()  

    user = User.query.filter_by(username=username).first()     

    if form.validate_on_submit():
        
        released = Released.query.filter_by(cpf=form.cpf.data).first()
        if released == None or released.user_id != user.id:
            flash("People does not exist!")
        else:
            
            #READ
            r = Released.query.filter_by(cpf=form.cpf.data)
            
            return render_template('readAllReleased.html',
                            lista=r)

    return render_template('readReleased.html',
                            form=form)

@app.route("/readAllReleased/<username>", methods=['GET', 'POST'])
@app.route("/readAllReleased", methods=['GET', 'POST'])
def readAllReleased(username):

    user = User.query.filter_by(username=username).first()  

    lista = Released.query.filter_by(user_id=user.id)
           

    return render_template('readAllReleased.html',
                            lista=lista)

@app.route("/deleteReleased/<username>", methods=['GET', 'POST'])
@app.route("/deleteRelesead", methods=['GET','POST'])
def deleteReleased(username):

    form = DeleteFormReleased()

    user = User.query.filter_by(username=username).first()

    if form.validate_on_submit():
        released = Released.query.filter_by(cpf=form.cpf.data).first()
        if released == None:
            flash("People does not exist!")
            return redirect(url_for("index"))
        else:
            #DELETE
            #r = Released.query.filter_by(cpf=form.cpf.data).first()
            if released.user_id == user.id:
                
                amostra=1
                while amostra<=25:

                    os.remove("app/IA/fotos/pessoa." + str(released.id) + "." + str(amostra) + ".jpg")
                    amostra+=1
                        
                db.session.delete(released)
                db.session.commit()

                treinamento.treinamento()

                flash("Deleted people!")
                return redirect(url_for("index"))
            else:
                flash("Not authorized! The person belongs to another administrator.")
                return redirect(url_for("index"))
            
    return render_template('deleteReleased.html',
                            form=form)