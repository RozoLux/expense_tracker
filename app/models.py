from . import db

class Categories (db.Model) :
    categoryid = db.Column(db.Integer, primary_key=True)
    categoryname = db.Column(db.String, nullable=False)

class Expenses (db.Model) :
    expenseid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    categoryid = db.Column(db.Integer, nullable=False)

class Profilepictures (db.Model) :
    profilepictureid = db.Column(db.Integer, primary_key=True)
    imagedata = db.Column(db.LargeBinary, nullable=False)

class Users (db.Model) :
    userid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    profilepictureid = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'userid': self.userid,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'profilepictureid': self.profilepictureid
        }