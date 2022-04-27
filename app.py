from flask import Flask, render_template, request, redirect, url_for, abort
import pandas as pd
from werkzeug.urls import url_parse

from config import DeveloperConfig
from models import Usuarios, db
from dataframe_all import dataframe_p1, cambio_baremo_one_p1, p1_dict_one, dataframe_p2
from forms import SignupForm, LoginForm
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

app = Flask(__name__)

app.config.from_object(DeveloperConfig)
login_manager = LoginManager(app)
login_manager.login_view = "login"
db.app = app
db.init_app(app)

#df1 = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSQ5NCVPoep7GUF5rFwqZ6jcaP84OVob42xcJjaBwo6YmWJM3MT89QmQaavTSo3Eqoi8cgsM1dOPv0S/pub?output=csv")
df1= dataframe_p1()
df_2 = dataframe_p2()
@login_manager.user_loader
def load_user(user_id):
    return Usuarios.get_by_id(int(user_id))


@app.route('/')
@login_required
def inicio():

    return render_template('datos_p1.html',
                           columns= df1.columns.values,
                           data= list(df1.values.tolist()),
                           link_column="Id",
                           zip=zip)


@app.route('/p2')
@login_required
def basc_p2():

    return render_template('datos_p2.html',
                           columns= df_2.columns.values,
                           data= list(df_2.values.tolist()),
                           link_column="Id",
                           zip=zip)


@app.route('/informe/<int:p1_id>', methods= ['GET', 'POST'])
@login_required
def informes(p1_id):
    baremo_list = ['General', 'Mujeres', 'Varones']
    if request.method == 'POST':

        baremo = request.form.get('baremo_p1')
        if baremo in baremo_list:
            datos_cambiados = cambio_baremo_one_p1(df1, p1_id, baremo)
            datos_one= p1_dict_one(df1, datos_cambiados, p1_id)
        else:
            datos_one = p1_dict_one(df1, df1, p1_id)
        return render_template('informe.html', datos=datos_one, lista=baremo_list)

    #p1_id = 2
    datos = df1['Id'] == p1_id
    dato_filtrado = df1[datos]
    if len(dato_filtrado) == 0:
        abort(404, description="Upss! Parece que hubo un error")
    dato_filtrado.columns = dato_filtrado.columns.str.replace(" ", "_")
    dato_dict = dato_filtrado.to_dict('records')
    return render_template('informe.html', datos=dato_dict, lista=baremo_list)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('inicio'))


@app.route('/login/', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))
    form= LoginForm()
    if form.validate_on_submit():
        user = Usuarios.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('inicio')
            return redirect(next_page)
    return render_template('auth-signin.html', form=form)


@app.route('/signup/',  methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        edad = form.edad.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = Usuarios.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
            # Creamos el usuario y lo guardamos
            user = Usuarios(nombre=name, email=email, edad=edad)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('inicio')
            return redirect(next_page)
    return render_template('signup.html', form=form, error=error)


if __name__ == '__main__':

    #print jdata
    db.create_all()
    app.run(debug=True)




