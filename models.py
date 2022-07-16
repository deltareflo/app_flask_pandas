from shared import db
import datetime
from sqlalchemy import column, String, Integer, ForeignKey, Boolean, Text, Date
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import enum


def fecha_actual():
    hoy = datetime.date.today()
    return hoy.strftime("%d/%m/%Y")


class TimestampMixin(object):
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)


class IntEnum(db.TypeDecorator):
    impl = db.Integer()

    def __init__(self, enumtype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enumtype = enumtype

        def process_bind_param(self, value, dialect):
                if isinstance(value, enum):
                    return value
                elif isinstance(value, int):
                    return value
                return value.value

        def process_result_value(self, value, dialect):
            return self._enumtype(value)


class Opciones(enum.Enum):
    varon= 'varón'
    mujer= 'mujer'
    general= 'general'


class Usuarios(db.Model, UserMixin):
    __tablename__= 'basc_user'

    id = db.Column(Integer, primary_key=True)
    nombre= db.Column(String(length=50), nullable=False)
    edad = db.Column(Integer)
    email = db.Column(String(length=150), unique=True)
    password= db.Column(String(length=128))
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Usuarios.query.get(id)
    @staticmethod
    def get_by_email(email):
        return Usuarios.query.filter_by(email=email).first()


class Examenes(db.Model):

    id = db.Column(Integer, primary_key=True)
    item1= db.Column(Integer)
    item2= db.Column(Integer)
    item3= db.Column(Integer)


class SegUser(db.Model, UserMixin):
    __tablename__= 'seguimiento_user'

    id = db.Column(Integer, primary_key=True)
    nombre = db.Column(String(length=50), nullable=False)
    edad = db.Column(Integer)
    grado = db.Column(String(length=40))
    localidad = db.Column(String(length=60))
    email = db.Column(String(length=150))
    carpeta = db.Column(String(length=150))
    status = db.Column(Boolean, default=True)
    # ForeignKey
    id_contacto = db.Column(Integer, ForeignKey('contacto_user.id'))
    contacto = db.relationship('ContactoSegUser', backref='seguimiento_user', lazy=True)

    def __repr__(self):
        return f'<User {self.nombre}>'


class ContactoSegUser(db.Model, UserMixin):
    __tablename__ = 'contacto_user'

    id = db.Column(Integer, primary_key=True)
    nombre = db.Column(String(length=50), nullable=False)
    telefono = db.Column(String(length=40))

    def __repr__(self):
        return f'<User {self.nombre}>'


class ConsultaSegUser(db.Model, UserMixin):
    __tablename__ = 'consulta_user'

    id = db.Column(Integer, primary_key=True)
    fecha = db.Column(Date)
    profesional = db.Column(String(length=40))
    comentario = db.Column(String(length=100))
    id_user = db.Column(Integer, ForeignKey('seguimiento_user.id'))
    user = db.relationship('SegUser', backref='consulta_user', lazy=True)

    def __repr__(self):
        return f'<Profesional {self.profesional}>'


class EvalSegUser(db.Model, UserMixin):
    __tablename__ = 'evaluacion_user'

    id = db.Column(Integer, primary_key=True)
    fecha = db.Column(Date)
    profesionales = db.Column(String(length=100))
    # Foreignkey
    id_user = db.Column(Integer, ForeignKey('seguimiento_user.id'))
    user = db.relationship('SegUser', backref='eval_user', lazy=True)
    id_eval = db.Column(Integer, ForeignKey('tipos_eval.id'))
    evaluacion = db.relationship('EvaluacionTipo', backref='tipos_eval', lazy=True)

    def __repr__(self):
        return f'<Profesional {self.profesionales}>'


class EvaluacionTipo(db.Model, UserMixin):
    __tablename__ = 'tipos_eval'

    id = db.Column(Integer, primary_key=True)
    evaluacion = db.Column(String(length=60), nullable=False)

    def __repr__(self):
        return f'<Evaluacion {self.evaluacion}>'


class InformeSegUser(db.Model, UserMixin):
    __tablename__ = 'informe_user'
    # Unir a la tabla resultado y relacionar con evalauacion
    id = db.Column(Integer, primary_key=True)
    fecha = db.Column(Date)
    comentario = db.Column(String(length=100))
    # Foreignkey
    id_user = db.Column(Integer, ForeignKey('seguimiento_user.id'))
    user = db.relationship('SegUser', backref='informe_user', lazy=True)

    def __repr__(self):
        return f'<Fecha {self.fecha}>'


class ResultadoSegUser(db.Model, UserMixin):
    __tablename__ = 'resultado_user'

    id = db.Column(Integer, primary_key=True)
    fecha = db.Column(Date)
    comentario = db.Column(String(length=150))
    aa_cc = db.Column(String(length=50), nullable=False)
    excepcionalidad = db.Column(String(length=50))
    recomendacion = db.Column(String(length=150))

    # Foreignkey
    id_user = db.Column(Integer, ForeignKey('seguimiento_user.id'))
    user = db.relationship('SegUser', backref='resultado_user', lazy=True)

    def __repr__(self):
        return f'<Resultado {self.aa_cc}>'


class AcompSegUser(db.Model, UserMixin):
    __tablename__ = 'acompanhar_user'

    id = db.Column(Integer, primary_key=True)
    fecha_inicio = db.Column(Date)
    encargado = db.Column(String(length=50))
    modalidad = db.Column(String(length=20))
    comentario = db.Column(Text)
    # Foreignkey
    id_user = db.Column(Integer, ForeignKey('seguimiento_user.id'))
    user = db.relationship('SegUser', backref='acomp_user', lazy=True)
    id_tipo = db.Column(Integer, ForeignKey('tipo_acompanamiento.id'))
    tipo = db.relationship('Tipo', backref='tipo_acompanamiento', lazy=True)

    def __repr__(self):
        return f'<Encargada {self.encargado}>'


class Tipo(db.Model, UserMixin):
    __tablename__ = 'tipo_acompanamiento'

    id = db.Column(Integer, primary_key=True)
    tipo = db.Column(String(length=50), nullable=False)

    def __repr__(self):
        return f'<Tipo {self.tipo}>'


class InfoSeg(db.Model, UserMixin):
    __tablename__ = 'info_seguimiento'

    id = db.Column(Integer, primary_key=True)
    fecha_creado = db.Column(Date)
    info = db.Column(Text, nullable=False)
    id_user = db.Column(Integer, ForeignKey('seguimiento_user.id'))
    user = db.relationship('SegUser', backref='info_user', lazy=True)

    def __repr__(self):
        return f'<Info {self.info}>'
