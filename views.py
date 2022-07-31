from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_user,login_required,logout_user,current_user
from .models import Note
from . import db


views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def index():
    if request.method == 'POST':
        note = request.form.get('note')
         
        if len(note) < 1:
            flash('Note is too short!', category='error')   
        else:
            new_note = Note(note_content=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    
    return render_template("index.html", user=current_user)


@views.route("/note/delete/<string:id>")
@login_required
def delete_note(id):
    
    note_info = Note.query.filter_by(id=id).first()
    
    # note_info = db.session.query(Note).filter(Note.id==id).first()
    
    # print(id,note_info.user_id)
    
    if note_info.user_id == current_user.id:
        
        db.session.delete(note_info)
        db.session.commit()
        flash('Note Deleted Successfully!', category="success")
        
        
    return render_template("index.html", user=current_user)
    # return redirect(url_for('views.index'))
    

