from flask_login import UserMixin
from app import db, login_manager

# Define User model
class Users(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=120), nullable=False, unique=True)
    email = db.Column(db.String(length=120), nullable=False, unique=True)
    password = db.Column(db.String(length=120),nullable=False)
    height = db.Column(db.Float,nullable=False)
    weight = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float,nullable=False)
    

    # Add any additional fields or methods as needed

    '''@property
    def password(self):
        return self.password'''

    def check_password_correction(self,attempted_password):
        if self.password == attempted_password:
            return True
        else:
            return False
    
class Testuser(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=120), nullable=False, unique=True)
    email = db.Column(db.String(length=120), nullable=False, unique=True)
    password = db.Column(db.String(length=120),nullable=False)
    height = db.Column(db.Float,nullable=False)
    weight = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float,nullable=False)





# Define user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
