from flask import Blueprint , render_template,flash,jsonify,request
from flask_login import login_required ,current_user
from .models import Note
from website import db
import json

views = Blueprint('views', __name__)

@views.route('/',methods=['POST','GET'])
@login_required
def home():
    if request.method=='POST':
        note = request.form.get('note')
        if len(note)<3:
            flash('Note is too short!')
        else:
            new_note = Note(Note_content = note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template('Home.html' , user=current_user)

@views.route('delete-note',methods=['POST'])
def delete_note():
    note = json.loads((request.data))
    noteid = note['noteid']
    note = Note.query.get(noteid)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})