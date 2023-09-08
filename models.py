
from sqlalchemy import join, select
from common import db, DictConverter

class CurrentUser:
    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    
    def has_permission(self, permissionCode:str):
        # return db.session.execute(db.Select(Permission).filter_by(code=permissionCode)).scalar() is not None
        stmt = (
            select(Permission)
            .select_from(
                join(
                    join(
                        join(
                            join(User, UserRole, User.id == UserRole.user_id),
                            Role,
                            UserRole.role_id == Role.id,
                        ),
                        RolePermission,
                        Role.id == RolePermission.role_id,
                    ),
                    Permission,
                    RolePermission.permission_id == Permission.id,
                )
            )
            .where(User.id == self.id)
        )
        
        permissions = [p[0].code for p in db.session.execute(stmt).fetchall()]
        return permissionCode in permissions
  

class Entity:
    def as_dict(self):
        d = DictConverter.as_dict(self)
        return d

class Category(db.Model, Entity):
    __tablename__ = 'category'
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Login(db.Model, Entity):
    __tablename__ = "login"
    id = db.Column(db.String(100), primary_key=True)
    userName = db.Column(db.String(100), unique=True, nullable=False)
    normalizedUserName = db.Column(db.String(100), unique=True, nullable=False)
    passwordHash = db.Column(db.String(256), nullable=False)

class User(db.Model, Entity):
    __tablename__ = "user"
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    login_id = db.Column(db.String(100), db.ForeignKey(Login.id), nullable=False)

class Permission(db.Model, Entity):
    __tablename__ = "permission"
    id = db.Column(db.String(100), primary_key=True)
    code = db.Column(db.String(100), unique=True, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Role(db.Model, Entity):
    __tablename__ = "role"
    id = db.Column(db.String(100), primary_key=True)
    code = db.Column(db.String(100), unique=True, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class UserRole(db.Model, Entity):
    __tablename__ = "userRole"
    id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey(User.id), nullable=False)
    role_id = db.Column(db.String(100), db.ForeignKey(Role.id), nullable=False)

class RolePermission(db.Model, Entity):
    __tablename__ = "rolePermission"
    id = db.Column(db.String(100), primary_key=True)
    role_id = db.Column(db.String(100), db.ForeignKey(Role.id), nullable=False)
    permission_id = db.Column(db.String(100), db.ForeignKey(Permission.id), nullable=False)

