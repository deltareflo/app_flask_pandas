from shared import db
from sqlalchemy import column, String, Integer
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import enum


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
    email = db.Column(String(length=150), unique= True)
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



class User(UserMixin):
    pass