from . import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
from datetime import datetime


#Added this code to solve the Exception: Missing user_loader or request_loader.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class Pitch(db.Model): 
    _tablename_ = 'pitches'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    category = db.Column(db.String)
    description = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    comment = db.relationship('Comment', backref='pitch', lazy='dynamic')
    upvote = db.relationship("Like",backref="pitch",lazy="dynamic")
    downvote = db.relationship("Dislike",backref="pitch",lazy="dynamic")


    # save pitch

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitches(cls,id):
            pitches =Pitch.query.filter_by(pitch_id=id).all()
            return pitches

    def _repr_(self):
        return f'Pitch {self.title}'

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))

    pitch = db.relationship('Pitch',backref = 'user',lazy = "dynamic")
    upvote = db.relationship('Like',backref='user',lazy='dynamic')
    downvote = db.relationship('Dislike',backref='user',lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)


    def __repr__(self):
        return f'User {self.username}'

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    pitch_id = db.Column(db.Integer,db.ForeignKey("pitch.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()
    
    def _repr_(self):

        return f'Comment {self.comment}'


class Like(db.Model):
  _tablename_ = 'likes'
  id = db.Column(db.Integer,primary_key=True)
  user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
  pitch_id = db.Column(db.Integer,db.ForeignKey('pitch.id'))
  def save(self):
    db.session.add(self)
    db.session.commit()
  @classmethod
  def get_upvotes(cls,id):
    upvote = Like.query.filter_by(pitch_id=id).all()
    return upvote
  def _repr_(self):
      return f'{self.user_id}:{self.pitch_id}'


class Dislike(db.Model):
  _tablename_ = 'dislikes'
  id = db.Column(db.Integer,primary_key=True)
  user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
  pitch_id = db.Column(db.Integer,db.ForeignKey('pitch.id'))
  def save(self):
    db.session.add(self)
    db.session.commit()
  @classmethod
  def get_downvotes(cls,id):
    downvote = Dislike.query.filter_by(pitch_id=id).all()
    return downvote
  def _repr_(self):
    return f'{self.user_id}:{self.pitch_id}'
