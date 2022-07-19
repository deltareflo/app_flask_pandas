import datetime

from flask import Flask, render_template, request, redirect, url_for, abort,flash
import pandas as pd
from werkzeug.urls import url_parse

from config import DeveloperConfig
from models import Usuarios, db, SegUser, ContactoSegUser, ConsultaSegUser, EvalSegUser, EvaluacionTipo, \
    ResultadoSegUser, Tipo, AcompSegUser, InfoSeg, InformeSegUser, Profesionales
from dataframe_all import dataframe_p1, cambio_baremo_one_p1, p1_dict_one, dataframe_p2, cambio_baremo_one_p2, \
    dataframe_p3, dataframe_s3, cambio_baremo_one_s3, cambio_baremo_one_p3, dataframe_s2, cambio_baremo_one_s2

from forms import SignupForm, LoginForm, ContactoForm, SegForm, ConsultaForm, EvalForm, EvalTipoForm, ResultadoForm, \
    TipoAcompForm, AcompForm, InfoForm, ProfeForm
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from decorators import admin_required
from sqlalchemy import desc


def insert_contacto():
    pass


app = Flask(__name__)

app.config.from_object(DeveloperConfig)
login_manager = LoginManager(app)
login_manager.login_view = "login"
db.app = app
db.init_app(app)

#df1 = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSQ5NCVPoep7GUF5rFwqZ6jcaP84OVob42xcJjaBwo6YmWJM3MT89QmQaavTSo3Eqoi8cgsM1dOPv0S/pub?output=csv")
df1= dataframe_p1()
df_2 = dataframe_p2()
df_3 = dataframe_p3()
df_s3 = dataframe_s3()
df_s2 = dataframe_s2()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


@app.errorhandler(401)
def internal_error(error):
    return render_template('401.html'), 401


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


@app.route('/add-contact',  methods=["GET", "POST"])
@login_required
@admin_required
def contacto():
    form = ContactoForm()
    if form.validate_on_submit():
        name = form.nombre.data
        num = form.numero.data
        # Comprobamos que no hay ya un usuario con ese email

        # Creamos el usuario y lo guardamos
        user = ContactoSegUser(nombre=name, telefono=num)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('contacto'))
    return render_template('add_contacto.html',
                           form=form)


@app.route('/add-user/',  methods=["GET", "POST"])
@login_required
@admin_required
def usuario():
    form = SegForm()
    contactos = [(b.id, b.nombre) for b in ContactoSegUser.query.all()]
    form.contacto.choices = contactos
    if form.validate_on_submit():

        name = form.nombre.data
        edad = form.edad.data
        grado = form.grado.data
        localidad = form.localidad.data
        email = form.email.data
        carpeta = form.carpeta.data
        mensaje = "Registro creado"
        # Creamos el usuario y lo guardamos
        new_user = SegUser(nombre=name, edad=edad, grado=grado,
                           email=email, carpeta=carpeta, id_contacto=form.contacto.data,
                           localidad=localidad)
        db.session.add(new_user)
        db.session.commit()
        flash(mensaje)
        return redirect(url_for('usuario'))
    return render_template('add_usuario.html',
                           form=form)


@app.route('/all-contact/',  methods=["GET"])
@login_required
def all_contacto():
    contacts = ContactoSegUser.query.all()

    return render_template('all_contacto.html',
                           contacts=contacts)


@app.route('/edit-contact/<int:c1_id>',  methods=["GET", "POST"])
@login_required
@admin_required
def edit_contacto(c1_id):
    form = ContactoForm()
    contacts = ContactoSegUser.query.filter_by(id=c1_id).first()
    if form.validate_on_submit():

        contacts.nombre = form.nombre.data
        contacts.telefono = form.numero.data
        mensaje = "Registro actualizado"
        # Creamos el usuario y lo guardamos
        db.session.commit()
        flash(mensaje)
        return redirect(url_for('all_contacto'))
    return render_template('edit_contacto.html',
                           contacts=contacts, form=form)


@app.route('/all-usuario/',  methods=["GET"])
@login_required
def all_usuario():
    users = SegUser.query.all()
    contactos = [(b.id, b.nombre, b.telefono) for b in ContactoSegUser.query.all()]
    return render_template('all_usuario.html',
                           users=users, contactos=contactos)


@app.route('/edit-user/<int:u1_id>',  methods=["GET", "POST"])
@login_required
@admin_required
def edit_usuario(u1_id):

    contacts = SegUser.query.filter_by(id=u1_id).first()
    form = SegForm()
    contactos = [(b.id, b.nombre) for b in ContactoSegUser.query.all()]
    form.contacto.choices = contactos
    form.contacto.data = contacts.id_contacto
    if form.validate_on_submit():

        contacts.nombre = form.nombre.data
        contacts.edad = form.edad.data
        contacts.grado = form.grado.data
        contacts.localidad = form.localidad.data
        contacts.email = form.email.data
        contacts.carpeta = form.carpeta.data
        mensaje = "Registro actualizado"
        # Creamos el usuario y lo guardamos
        db.session.commit()
        flash(mensaje)
        return redirect(url_for('all_usuario'))
    return render_template('edit_usuario.html',
                           contacts=contacts, form=form)


@app.route('/seguimiento/<int:s1_id>',  methods=["GET", "POST"])
@login_required
def seguimiento(s1_id):

    user = SegUser.query.filter_by(id=s1_id).first()
    contact = ContactoSegUser.query.filter_by(id=user.id_contacto).first()
    consulta = ConsultaSegUser.query.filter_by(id_user=user.id).first()
    if consulta:
        prof_consul = Profesionales.query.filter_by(id=consulta.id_prof).first()
    else:
        prof_consul = None

    evaluacion = EvalSegUser.query.filter_by(id_user=user.id).first()
    if evaluacion:
        tipo_eval = EvaluacionTipo.query.filter_by(id=evaluacion.id_eval).first()
        prof1 = Profesionales.query.filter_by(id=evaluacion.id_prof).first()
        prof2 = Profesionales.query.filter_by(id=evaluacion.id_prof1).first()
    else:
        tipo_eval = None
        prof1 = None
        prof2 = None

    resultado = ResultadoSegUser.query.filter_by(id_user=user.id).first()
    acompa = AcompSegUser.query.filter_by(id_user=user.id).all()
    profesionales = Profesionales.query.all()
    tipo_acomp = Tipo.query.all()
    infos = InfoSeg.query.filter_by(id_user=user.id).order_by(desc(InfoSeg.fecha_creado))
    return render_template('ficha.html',
                           contact=contact, user=user, consulta=consulta, prof_consul=prof_consul,
                           evaluacion=evaluacion, tipo_eval=tipo_eval, prof1=prof1,
                           prof2=prof2, resultado=resultado, profesionales=profesionales,
                           acompa=acompa, infos=infos, tipo_acomp=tipo_acomp)


@app.route('/all-prof/',  methods=["GET"])
@login_required
def all_prof():
    profesionales = Profesionales.query.all()
    return render_template('all_prof.html',
                           profesionales=profesionales)


@app.route("/add-prof/", methods=['GET', 'POST'])
@login_required
@admin_required
def add_prof():
    form = ProfeForm()
    if form.validate_on_submit():

        nombre = form.nombre.data
        mensaje = "Registro creado"
        # Creamos el usuario y lo guardamos
        new_nombre = Profesionales(nombre=nombre)
        db.session.add(new_nombre)
        db.session.commit()
        flash(mensaje)
        return redirect(url_for('all_prof'))
    return render_template('add_prof.html',
                           form=form)


@app.route('/edit-prof/<int:pf_id>',  methods=["GET", "POST"])
@login_required
@admin_required
def edit_prof(pf_id):
    profesional = Profesionales.query.filter_by(id=pf_id).first()
    form = ProfeForm()
    if form.validate_on_submit():

        profesional.nombre = form.nombre.data
        mensaje = "Registro actualizado"
        # Actualizamos el registro y lo guardamos
        db.session.commit()
        flash(mensaje)
        return redirect(url_for('all_prof'))
    return render_template('edit_prof.html',
                           profesional=profesional, form=form)


@app.route("/add-consulta/", methods=['GET', 'POST'], defaults={'user_id': None})
@app.route("/add-consulta/<int:user_id>", methods=['GET', 'POST'])
@login_required
@admin_required
def add_consulta(user_id):
    form = ConsultaForm()
    users = [(b.id, b.nombre) for b in SegUser.query.all()]
    form.usuario.choices = users
    profs = [(b.id, b.nombre) for b in Profesionales.query.all()]
    form.profesional.choices = profs
    if user_id:
        form.usuario.data = user_id

    if form.validate_on_submit():

        fecha = request.form['fecha']
        user = form.usuario.data
        profesional = form.profesional.data
        comentario = form.comentario.data
        mensaje = "Registro creado"
        # Creamos el usuario y lo guardamos
        new_consulta = ConsultaSegUser(fecha=fecha, id_prof=profesional, id_user=user,
                                       comentario=comentario)
        db.session.add(new_consulta)
        db.session.commit()
        flash(mensaje)
        return redirect(url_for('all_consulta'))
    return render_template('add_consulta.html',
                           form=form)


@app.route('/all-consulta/',  methods=["GET"])
@login_required
def all_consulta():
    consultas = ConsultaSegUser.query.all()
    users = [(b.id, b.nombre) for b in SegUser.query.all()]
    profs = [(b.id, b.nombre) for b in Profesionales.query.all()]
    return render_template('all_consulta.html',
                           consultas=consultas, users=users, profs=profs)


@app.route('/edit-consultas/<int:pr_id>',  methods=["GET", "POST"])
@login_required
@admin_required
def edit_consulta(pr_id):
    consultas = ConsultaSegUser.query.filter_by(id=pr_id).first()
    form = ConsultaForm(usuario=consultas.id_user)
    users = [(b.id, b.nombre) for b in SegUser.query.all()]
    form.usuario.choices = users
    if form.validate_on_submit():

        consultas.fecha = form.fecha.data
        consultas.profesional = form.profesional.data
        consultas.id_user = form.usuario.data
        consultas.comentario = form.comentario.data
        mensaje = "Registro actualizado"
        # Actualizamos el registro y lo guardamos
        db.session.commit()
        flash(mensaje)
        return redirect(url_for('all_consulta'))
    return render_template('edit_consulta.html',
                           consultas=consultas, form=form)


@app.route('/all-tipo/',  methods=["GET"])
@login_required
def all_tipo():
    tipos = EvaluacionTipo.query.all()
    return render_template('all_tipo_evaluacion.html',
                           tipos=tipos)


@app.route("/add-tipo-eval/", methods=['GET', 'POST'])
@login_required
@admin_required
def add_tipo_eval():
    form = EvalTipoForm()
    if form.validate_on_submit():

        tipo = form.evaluacion.data
        mensaje = "Registro creado"
        # Creamos el registro y lo guardamos
        new_tipo = EvaluacionTipo(evaluacion=tipo)
        db.session.add(new_tipo)
        db.session.commit()
        flash(mensaje)
        return redirect(url_for('all_tipo'))
    return render_template('add_tipo_eval.html',
                           form=form)


@app.route('/edit-tipos/<int:te_id>',  methods=["GET", "POST"])
@login_required
@admin_required
def edit_tipos(te_id):
    tipos = EvaluacionTipo.query.filter_by(id=te_id).first()
    form = EvalTipoForm()
    if form.validate_on_submit():

        tipos.evaluacion= form.evaluacion.data
        mensaje = "Registro actualizado"
        # Actualizamos el registro y lo guardamos
        db.session.commit()
        flash(mensaje)
        return redirect(url_for('all_tipo'))
    return render_template('edit_pruebas.html',
                           tipos=tipos, form=form)


@app.route('/all-evaluacion/',  methods=["GET"])
@login_required
def all_evaluacion():
    evaluaciones = EvalSegUser.query.all()
    users = [(b.id, b.nombre) for b in SegUser.query.all()]
    tipos = [(b.id, b.evaluacion) for b in EvaluacionTipo.query.all()]
    profs = [(b.id, b.nombre) for b in Profesionales.query.all()]
    return render_template('all_evaluacion.html',
                           evaluaciones=evaluaciones, users=users, tipos=tipos, profs=profs)


@app.route("/add-evaluacion/", methods=['GET', 'POST'], defaults={'user_id': None})
@app.route("/add-evaluacion/<int:user_id>", methods=['GET', 'POST'])
@login_required
@admin_required
def add_evaluacion(user_id):
    form = EvalForm()
    users = [(b.id, b.nombre) for b in SegUser.query.all()]
    form.usuario.choices = users
    if user_id:
        form.usuario.data = user_id

    tipo = [(b.id, b.evaluacion) for b in EvaluacionTipo.query.all()]
    form.evaluacion.choices = tipo
    profs = [(b.id, b.nombre) for b in Profesionales.query.all()]
    form.profesional1.choices = profs
    form.profesional2.choices = profs

    if form.validate_on_submit():

        fecha = form.fecha.data
        user = form.usuario.data
        profesional1 = form.profesional1.data
        profesional2 = form.profesional2.data
        tipo_eval = form.evaluacion.data
        mensaje = "Registro creado"

        # Creamos el usuario y lo guardamos
        new_evaluacion = EvalSegUser(fecha=fecha, id_prof=profesional1, id_prof1=profesional2,
                                     id_user=user, id_eval=tipo_eval)
        db.session.add(new_evaluacion)
        db.session.commit()
        flash(mensaje)
        return redirect(url_for('all_evaluacion'))
    return render_template('add_evaluacion.html',
                           form=form)


@app.route('/edit-evaluacion/<int:ev_id>',  methods=["GET", "POST"])
@login_required
@admin_required
def edit_evaluacion(ev_id):
    evaluacion = EvalSegUser.query.filter_by(id=ev_id).first()
    form = EvalForm(usuario=evaluacion.id_user, evaluacion=evaluacion.id_eval, profesional1=evaluacion.id_prof,
                    profesional2=evaluacion.id_prof1)
    users = [(b.id, b.nombre) for b in SegUser.query.all()]
    form.usuario.choices = users
    # form.usuario.data = evaluacion.id_user
    tipo = [(b.id, b.evaluacion) for b in EvaluacionTipo.query.all()]
    form.evaluacion.choices = tipo
    profs = [(b.id, b.nombre) for b in Profesionales.query.all()]
    form.profesional1.choices = profs
    form.profesional2.choices = profs
    if form.validate_on_submit():

        evaluacion.fecha = form.fecha.data
        evaluacion.id_prof = form.profesional1.data
        evaluacion.id_prof1 = form.profesional2.data
        evaluacion.id_user = form.usuario.data
        evaluacion.id_eval = form.evaluacion.data
        mensaje = "Registro actualizado"
        # Actualizamos el registro y lo guardamos
        db.session.commit()
        flash(mensaje)
        return redirect(url_for('all_evaluacion'))
    return render_template('edit_evaluacion.html',
                           evaluacion=evaluacion, users=users, tipo=tipo, form=form)


@app.route('/all-resultado/',  methods=["GET"])
@login_required
def all_resultado():
    resultados = ResultadoSegUser.query.all()
    users = [(b.id, b.nombre) for b in SegUser.query.all()]
    return render_template('all_informe.html',
                           resultados=resultados, users=users)


@app.route("/add-resultado/", methods=['GET', 'POST'], defaults={'user_id': None})
@app.route("/add-resultado/<int:user_id>", methods=['GET', 'POST'])
@login_required
@admin_required
def add_resultado(user_id):
    form = ResultadoForm()
    users = [(b.id, b.nombre) for b in SegUser.query.all()]
    form.usuario.choices = users
    if user_id:
        form.usuario.data = user_id

    if form.validate_on_submit():

        fecha = form.fecha.data
        user = form.usuario.data
        comentario = form.comentario.data
        aa_cc = form.aa_cc.data
        excepcionalidad = form.excepcionalidad.data
        recomendacion = form.recomendacion.data
        mensaje = "Registro creado"
        # Creamos el usuario y lo guardamos
        new_resultado = ResultadoSegUser(fecha=fecha, comentario=comentario, aa_cc=aa_cc, id_user=user,
                                          excepcionalidad=excepcionalidad, recomendacion=recomendacion)
        db.session.add(new_resultado)
        db.session.commit()
        flash(mensaje)
        return redirect(url_for('all_resultado'))
    return render_template('add_resultado.html',
                           form=form)


@app.route('/edit-resultado/<int:rs_id>',  methods=["GET", "POST"])
@login_required
@admin_required
def edit_resultado(rs_id):
    resultado = ResultadoSegUser.query.filter_by(id=rs_id).first()
    form = ResultadoForm(usuario=resultado.id_user)
    users = [(b.id, b.nombre) for b in SegUser.query.all()]
    form.usuario.choices = users
    if form.validate_on_submit():

        resultado.fecha = form.fecha.data
        resultado.comentario = form.comentario.data
        resultado.id_user = form.usuario.data
        resultado.aa_cc = form.aa_cc.data
        resultado.excepcionalidad = form.excepcionalidad.data
        resultado.recomendacion = form.recomendacion.data
        mensaje = "Registro actualizado"
        # Actualizamos el registro y lo guardamos
        db.session.commit()
        flash(mensaje)
        return redirect(url_for('all_resultado'))
    return render_template('edit_resultado.html',
                           resultado=resultado, users=users, form=form)


@app.route('/all-tipo-acomp/',  methods=["GET"])
@login_required
def all_tipo_acomp():
    tipos = Tipo.query.all()

    return render_template('all_tipo_acomp.html',
                           tipos=tipos)


@app.route("/add-tipo-acomp/", methods=['GET', 'POST'])
@login_required
@admin_required
def add_tipo_acomp():
    form = TipoAcompForm()
    if form.validate_on_submit():

        tipo = form.tipo.data
        mensaje = "Registro creado"
        # Creamos el registro y lo guardamos
        new_tipo = Tipo(tipo=tipo)
        db.session.add(new_tipo)
        db.session.commit()
        flash(mensaje)
        return redirect(url_for('all_tipo_acomp'))
    return render_template('add_tipo_acomp.html',
                           form=form)


@app.route('/edit-tipos-acomp/<int:ta_id>',  methods=["GET", "POST"])
@login_required
@admin_required
def edit_tipos_acomp(ta_id):
    tipos = Tipo.query.filter_by(id=ta_id).first()
    form = TipoAcompForm()
    if form.validate_on_submit():

        tipos.tipo= form.tipo.data
        mensaje = "Registro actualizado"
        # Actualizamos el registro y lo guardamos
        db.session.commit()
        flash(mensaje)
        return redirect(url_for('all_tipo_acomp'))
    return render_template('edit_tipo_acomp.html',
                           tipos=tipos, form=form)


@app.route('/all-acomp/',  methods=["GET"])
@login_required
def all_acomp():
    acomp = AcompSegUser.query.all()
    users = [(b.id, b.nombre) for b in SegUser.query.all()]
    tipos = [(b.id, b.tipo) for b in Tipo.query.all()]
    profesionales = Profesionales.query.all()
    return render_template('all_acomp.html',
                           acomp=acomp, users=users, tipos=tipos, profesionales=profesionales)


@app.route("/add-acomp/", methods=['GET', 'POST'], defaults={'user_id': None})
@app.route("/add-acomp/<int:user_id>", methods=['GET', 'POST'])
@login_required
@admin_required
def add_acomp(user_id):
    form = AcompForm()
    users = [(b.id, b.nombre) for b in SegUser.query.all()]
    form.usuario.choices = users
    profs = [(b.id, b.nombre) for b in Profesionales.query.all()]
    form.encargado.choices = profs
    if user_id:
        form.usuario.data = user_id

    tipo = [(b.id, b.tipo) for b in Tipo.query.all()]
    form.tipo_acompa.choices = tipo
    if form.validate_on_submit():

        fecha = form.fecha_inicio.data
        user = form.usuario.data
        encargado = form.encargado.data
        tipo_acomp = form.tipo_acompa.data
        modalidad = form.modalidad.data
        comentario = form.comentario.data
        mensaje = "Registro creado"
        # Creamos el usuario y lo guardamos
        new_acomp = AcompSegUser(fecha_inicio=fecha, id_prof=encargado,
                                      id_user=user, modalidad=modalidad, comentario=comentario, id_tipo=tipo_acomp)
        db.session.add(new_acomp)
        db.session.commit()
        flash(mensaje)
        return redirect(url_for('all_acomp'))
    return render_template('add_acomp.html',
                           form=form)


@app.route('/edit-acomp/<int:ac_id>',  methods=["GET", "POST"])
@login_required
@admin_required
def edit_acomp(ac_id):
    acomp = AcompSegUser.query.filter_by(id=ac_id).first()
    form = AcompForm(usuario=acomp.id_user, tipo_acompa=acomp.id_tipo, encargado=acomp.id_prof)
    users = [(b.id, b.nombre) for b in SegUser.query.all()]
    form.usuario.choices = users
    tipo = [(b.id, b.tipo) for b in Tipo.query.all()]
    form.tipo_acompa.choices = tipo
    profs = [(b.id, b.nombre) for b in Profesionales.query.all()]
    form.encargado.choices = profs
    if form.validate_on_submit():

        acomp.fecha_inicio = form.fecha_inicio.data
        acomp.id_prof = form.encargado.data
        acomp.id_user = form.usuario.data
        acomp.id_tipo = form.tipo_acompa.data
        acomp.modalidad = form.modalidad.data
        acomp.comentario = form.comentario.data
        mensaje = "Registro actualizado"
        # Actualizamos el registro y lo guardamos
        db.session.commit()
        flash(mensaje)
        return redirect(url_for('all_acomp'))
    return render_template('edit_acomp.html',
                           acomp=acomp, users=users, tipo=tipo, profs=profs, form=form)


@app.route('/all-info/',  methods=["GET"])
@login_required
def all_info():
    infos = InfoSeg.query.all()
    users = [(b.id, b.nombre) for b in SegUser.query.all()]
    return render_template('all_info.html',
                           infos=infos, users=users)


@app.route("/add-info/", methods=['GET', 'POST'], defaults={'user_id': None})
@app.route("/add-info/<int:user_id>", methods=['GET', 'POST'])
@login_required
@admin_required
def add_info(user_id):
    form = InfoForm()
    users = [(b.id, b.nombre) for b in SegUser.query.all()]
    form.usuario.choices = users
    if user_id:
        form.usuario.data = user_id

    if form.validate_on_submit():

        fecha = form.fecha_creado.data
        user = form.usuario.data
        info = form.info.data
        mensaje = "Registro creado"
        # Creamos el usuario y lo guardamos
        new_info = InfoSeg(fecha_creado=fecha, id_user=user, info=info)
        db.session.add(new_info)
        db.session.commit()
        flash(mensaje)
        return redirect(url_for('all_info'))
    return render_template('add_info.html',
                           form=form)


@app.route('/edit-info/<int:if_id>',  methods=["GET", "POST"])
@login_required
@admin_required
def edit_info(if_id):
    info = InfoSeg.query.filter_by(id=if_id).first()
    form = InfoForm(usuario=info.id_user)
    users = [(b.id, b.nombre) for b in SegUser.query.all()]
    form.usuario.choices = users
    if form.validate_on_submit():

        info.fecha_creado = form.fecha_creado.data
        info.info = form.info.data
        info.id_user = form.usuario.data
        mensaje = "Registro actualizado"
        # Actualizamos el registro y lo guardamos
        db.session.commit()
        flash(mensaje)
        return redirect(url_for('all_info'))
    return render_template('edit_info.html',
                           info=info, users=users, form=form)


@app.route('/p3')
@login_required
def basc_p3():

    return render_template('datos_p3.html',
                           columns= df_3.columns.values,
                           data= list(df_3.values.tolist()),
                           link_column="Id",
                           zip=zip)


@app.route('/s3')
@login_required
def basc_s3():

    return render_template('datos_s3.html',
                           columns= df_s3.columns.values,
                           data= list(df_s3.values.tolist()),
                           link_column="Id",
                           zip=zip)


@app.route('/s2')
@login_required
def basc_s2():

    return render_template('datos_s2.html',
                           columns= df_s2.columns.values,
                           data= list(df_s2.values.tolist()),
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


@app.route('/informe-p2/<int:p2_id>', methods= ['GET', 'POST'])
@login_required
def informes_p2(p2_id):
    baremo_list = ['General', 'Mujeres', 'Varones']
    if request.method == 'POST':
        baremos = []
        baremo = request.form.get('baremo_p2')
        baremos.append(baremo)
        if baremo in baremo_list:
            datos_cambiados = cambio_baremo_one_p2(df_2, p2_id, baremos)
            datos_one= p1_dict_one(df_2, datos_cambiados, p2_id)
        else:
            datos_one = p1_dict_one(df_2, df_2, p2_id)
        return render_template('informe_p2.html', datos=datos_one, lista=baremo_list)

    #p1_id = 2
    datos = df_2['Id'] == p2_id
    dato_filtrado = df_2[datos]
    if len(dato_filtrado) == 0:
        abort(404, description="Upss! Parece que hubo un error")
    dato_filtrado.columns = dato_filtrado.columns.str.replace(" ", "_")
    dato_dict = dato_filtrado.to_dict('records')
    return render_template('informe_p2.html', datos=dato_dict, lista=baremo_list)


@app.route('/informe-p3/<int:p3_id>', methods= ['GET', 'POST'])
@login_required
def informes_p3(p3_id):
    baremo_list = ['General', 'Mujeres', 'Varones']
    if request.method == 'POST':
        baremos = []
        baremo = request.form.get('baremo_p3')
        baremos.append(baremo)
        if baremo in baremo_list:
            datos_cambiados = cambio_baremo_one_p3(df_3, p3_id, baremos)
            datos_one= p1_dict_one(df_3, datos_cambiados, p3_id)
        else:
            datos_one = p1_dict_one(df_3, df_3, p3_id)
        return render_template('informe_p3.html', datos=datos_one, lista=baremo_list)

    #p1_id = 2
    datos = df_3['Id'] == p3_id
    dato_filtrado = df_3[datos]
    if len(dato_filtrado) == 0:
        abort(404, description="Upss! Parece que hubo un error")
    dato_filtrado.columns = dato_filtrado.columns.str.replace(" ", "_")
    dato_dict = dato_filtrado.to_dict('records')
    return render_template('informe_p3.html', datos=dato_dict, lista=baremo_list)


@app.route('/informe-s3/<int:s3_id>', methods= ['GET', 'POST'])
@login_required
def informes_s3(s3_id):
    baremo_list = ['General', 'Mujeres', 'Varones']
    if request.method == 'POST':
        baremos = []
        baremo = request.form.get('baremo_s3')
        baremos.append(baremo)
        if baremo in baremo_list:
            datos_cambiados = cambio_baremo_one_s3(df_s3, s3_id, baremos)
            datos_one= p1_dict_one(df_s3, datos_cambiados, s3_id)
        else:
            datos_one = p1_dict_one(df_s3, df_s3, s3_id)
        return render_template('informe_s3.html', datos=datos_one, lista=baremo_list)

    #p1_id = 2
    datos = df_s3['Id'] == s3_id
    dato_filtrado = df_s3[datos]
    if len(dato_filtrado) == 0:
        abort(404, description="Upss! Parece que hubo un error")
    dato_filtrado.columns = dato_filtrado.columns.str.replace(" ", "_")
    dato_dict = dato_filtrado.to_dict('records')
    return render_template('informe_s3.html', datos=dato_dict, lista=baremo_list)


@app.route('/informe-s2/<int:s2_id>', methods= ['GET', 'POST'])
@login_required
def informes_s2(s2_id):
    baremo_list = ['General', 'Mujeres', 'Varones']
    if request.method == 'POST':
        baremos = []
        baremo = request.form.get('baremo_s2')
        baremos.append(baremo)
        if baremo in baremo_list:
            datos_cambiados = cambio_baremo_one_s2(df_s2, s2_id, baremos)
            datos_one= p1_dict_one(df_s2, datos_cambiados, s2_id)
        else:
            datos_one = p1_dict_one(df_s2, df_s2, s2_id)
        return render_template('informe_s2.html', datos=datos_one, lista=baremo_list)

    #p1_id = 2
    datos = df_s2['Id'] == s2_id
    dato_filtrado = df_s2[datos]
    if len(dato_filtrado) == 0:
        abort(404, description="Upss! Parece que hubo un error")
    dato_filtrado.columns = dato_filtrado.columns.str.replace(" ", "_")
    dato_dict = dato_filtrado.to_dict('records')
    return render_template('informe_s2.html', datos=dato_dict, lista=baremo_list)


@app.route('/test-s3')
@login_required
def test_basc_s3():

    return render_template('addpaciente_s3.html')


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
        # Comprobamos que no hubiera un usuario con ese email
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




