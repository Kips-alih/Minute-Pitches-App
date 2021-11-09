from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import Dislike, User,Pitch,Comment,Like
from flask_login import login_required,current_user
from .. import db,photos
from .forms import CommentForm, PitchForm,UpdateProfile



#views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data.
    '''

    title = 'Home - Welcome to Minute Pitches App'

    pitch_form = PitchForm()
    pitches = Pitch.query.order_by(Pitch.date_posted).all()
    return render_template('index.html', title = title,pitches = pitches)

@main.route('/user_pitch', methods=['GET', 'POST'])
@login_required
def user_pitch():
    pitch_form = PitchForm()

    if pitch_form.validate_on_submit():
        title = pitch_form.title.data
        category=pitch_form.category.data
        description=pitch_form.description.data
        user_pitch = Pitch(title=title,category=category,description=description,user=current_user)

        user_pitch.save_pitch()
        db.session.add(user_pitch)
        db.session.commit()
        
        return redirect(url_for('main.index'))
    else:
        pitches = Pitch.query.order_by(Pitch.date_posted).all()
    
    return render_template('user_pitch.html', pitches=pitches,pitch_form = pitch_form)
    
@main.route('/user_pitch', methods=['POST','GET'])
@login_required
def each_pitch():
    """
    function that get one pitch.
    """
    comment_form= CommentForm()
    if comment_form.validate_on_submit():
            comment= comment_form.comment.data
            user_id = current_user._get_current_object().id
            pitch_id = current_user._get_current_object().id
            comment= Comment(comment=comment,user_id=user_id,pitch_id=pitch_id)
            comment.save_comment()
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('main.each_pitch'))
    else:
        pitches= Pitch.query.order_by(Pitch.date_posted).all()
        comment=Comment.query.order_by(Comment.comment).all()
    return render_template('index.html', pitches=pitches,comment_form=comment_form,comment=comment)



@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    profile_form = UpdateProfile()

    if profile_form.validate_on_submit():
        user.bio = profile_form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',profile_form =profile_form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/user_pitch/<id>', methods=['GET', 'POST'])
@login_required
def pitch_comments(id):

    comments = Comment.query.filter_by(pitch_id=id).all()
    pitches = Pitch.query.get(id)
    if pitches is None:
        abort(404)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = Comment(
            comment=comment_form.comment.data,
            pitch_id=id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        comment_form.comment.data = ''
    return render_template('comment.html',pitches= pitches, comments=comments, comment_form = comment_form)

#Liking and Disliking
@main.route('/like/<int:id>',methods = ['POST','GET'])
@login_required
def like(id):
    get_pitches = Like.get_upvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for pitch in get_pitches:
        to_str = f'{pitch}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_vote = Like(user = current_user, pitch_id=id)
    new_vote.save()
    return redirect(url_for('main.index',id=id))
@main.route('/dislike/<int:id>',methods = ['POST','GET'])
@login_required
def dislike(id):
    pitch = Dislike.get_downvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for pitch in pitch:
        to_str = f'{pitch}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_downvote = Dislike(user = current_user, pitch_id=id)
    new_downvote.save()
    return redirect(url_for('main.index',id = id))