from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, BooleanField, SelectField, \
    DateField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from models import fecha_actual


class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)], render_kw={"placeholder": "Nombre"})
    password = PasswordField('Contraseña', validators=[DataRequired()], render_kw={"placeholder": "contraseña"})
    edad = IntegerField('Edad', render_kw={"placeholder": "edad"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "email"})
    submit = SubmitField('Registrar')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder": "email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "contraseña"})
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')


class ContactoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()], render_kw={"placeholder": "Nombre"})
    numero = StringField('Número', validators=[DataRequired()], render_kw={"placeholder": "Número"})
    submit = SubmitField('Registrar')


class SegForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=50)], render_kw={"placeholder": "Nombre"})
    edad = IntegerField('Edad',validators=[DataRequired()], render_kw={"placeholder": "11"})
    grado = StringField('Grado', validators=[DataRequired(), Length(max=40)], render_kw={"placeholder": "Grado"})
    localidad = StringField('Localidad', validators=[Length(max=60)],
                            render_kw={"placeholder": "Localidad"})
    email = StringField('Email', validators=[Length(max=150)], render_kw={"placeholder": "Email"})
    carpeta = StringField('Carpeta', validators=[Length(max=150)], render_kw={"placeholder": "Carpeta drive"})
    contacto = SelectField('Contacto', coerce=int)
    submit = SubmitField('Registrar')


class ConsultaForm(FlaskForm):
    fecha = DateField('Fecha', render_kw={f"placeholder": f"{fecha_actual()}"})
    profesional = StringField('Profesional', validators=[ Length(max=40)], render_kw={"placeholder": "Lic. Juan Perez"})
    comentario = StringField('Comentario', validators=[Length(max=100)], render_kw={"placeholder": "Comentario..."})
    usuario = SelectField('Usuario', coerce=int)
    submit = SubmitField('Registrar')


class EvalTipoForm(FlaskForm):
    evaluacion = StringField('Evaluacion', validators=[ Length(max=60)], render_kw={"placeholder": "Perfil completo"})
    submit = SubmitField('Registrar')


class EvalForm(FlaskForm):
    fecha = DateField('Fecha', render_kw={f"placeholder": f"{fecha_actual()}"})
    profesionales = StringField('Profesionales', validators=[Length(max=100)],
                                render_kw={"placeholder": "Lic. Juan Perez"})
    usuario = SelectField('Usuario', coerce=int)
    evaluacion = SelectField('Evaluacion', coerce=int)
    submit = SubmitField('Registrar')


class InformeForm(FlaskForm):
    fecha = DateField('Fecha', format='%m/%d/%Y', render_kw={f"placeholder": f"{fecha_actual()}"})
    comentario = StringField('Comentario', validators=[Length(max=100)], render_kw={"placeholder": "Comentario"})
    usuario = SelectField('Usuario', coerce=int)
    submit = SubmitField('Registrar')


class ResultadoForm(FlaskForm):
    fecha = DateField('Fecha', render_kw={f"placeholder": f"{fecha_actual()}"})
    comentario = StringField('Recomendación', validators=[Length(max=150)],
                                render_kw={"placeholder": "Comentario"})
    aa_cc = StringField('Altas capacidades', validators=[Length(max=50), DataRequired()],
                        render_kw={"placeholder": "Si"})
    excepcionalidad = StringField('Excepcionalidad', validators=[Length(max=50)],
                                  render_kw={"placeholder": "TDAH"})
    recomendacion = StringField('Recomendación', validators=[Length(max=100)],
                                render_kw={"placeholder": "Recomendación"})
    usuario = SelectField('Usuario', coerce=int)
    submit = SubmitField('Registrar')


class AcompForm(FlaskForm):
    fecha_inicio = DateField('Fecha', render_kw={f"placeholder": f"{fecha_actual()}"})
    encargado = StringField('Encargado', validators=[Length(max=50)],
                            render_kw={"placeholder": "Lic. Ana Díaz"})
    modalidad = StringField('Modalidad', validators=[Length(max=20)],
                            render_kw={"placeholder": "Anual"})
    comentario = TextAreaField('Comentario')
    usuario = SelectField('Usuario', coerce=int)
    tipo_acompa = SelectField('Acompañamiento', coerce=int)
    submit = SubmitField('Registrar')


class TipoAcompForm(FlaskForm):
    tipo = StringField('Tipo', validators=[Length(max=50), DataRequired()], render_kw={"placeholder": "Acompañamiento"})
    submit = SubmitField('Registrar')


class InfoForm(FlaskForm):
    fecha_creado = DateField('Fecha', render_kw={f"placeholder": f"{fecha_actual()}"})
    info = TextAreaField('Comentario')
    usuario = SelectField('Usuario', coerce=int)
    submit = SubmitField('Registrar')
