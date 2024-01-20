from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,and_
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from werkzeug.utils import secure_filename
import datetime
import os
import secrets


app=Flask(__name__)

CORS(app)
app.config["JWT_SECRET_KEY"] = "5T52472er8a7m272a00o" 
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:''@localhost/terama'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['UPLOAD_VIDEO_FOLDER'] = '/uploads/Videos'
app.config['ALLOWED_VIDEO_EXTENSIONS'] = {'mp4', 'mov', 'avi', 'wmf' 'flv', 'webm','mkv'}


db = SQLAlchemy(app)
ma = Marshmallow(app)

class Posts(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Uniid = db.Column(db.String(255),nullable=False)
    Title = db.Column(db.String(100),nullable=False)
    Body = db.Column(db.TEXT, nullable=True)
    Image= db.Column(db.String(255), nullable=True)
    Video= db.Column(db.String(255), nullable=False)
    Categorie= db.Column(db.String(100), nullable=True)
    User= db.Column(db.Integer,nullable=False)
    Short =db.Column(db.Integer, default=0)
    Visible= db.Column(db.Integer, nullable=False,default=0)
    created_at= db.Column(db.String(50), default=datetime.datetime.now())

    def __init__(self,Uniid,Title,Body,Image,Video,Categorie,User,Visible):
        self.Uniid = Uniid
        self.Title = Title
        self.Body = Body
        self.Image = Image
        self.Video = Video
        self.Categorie = Categorie
        self.User = User
        self.Visible = Visible

        
with app.app_context():
    db.create_all()

with app.app_context():
    db.create_all()

class PostSchema(ma.Schema):
    class Meta:
        fields = ('Uniid','Title','Body','Image','Video','Categorie','User','Visible')        
    
post_schema = PostSchema()
posts_schema = PostSchema(many=True)

@app.route('/',methods=['GET'])
def index():
    return {'message':'Hello Upload'}

"""  Posts Fonctions begin  """
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_VIDEO_EXTENSIONS']
@app.route('/upload',methods=['POST'])
def add_posts():
    if 'videos' not in request.files:
        return 'No file part', 400
    videos = request.files.getlist('videos')
    if len(videos) == 0:
        return 'No video selected for uploading', 400
    for video in videos:
        print(videos)
        if video and allowed_file(video.filename):
            filename = secure_filename(video.filename)
            new_filename = secrets.token_hex(15)
            new_filename = new_filename+"_"+filename[-6:]
            if not os.path.exists(app.config['UPLOAD_VIDEO_FOLDER']):
                os.makedirs(app.config['UPLOAD_VIDEO_FOLDER'])
            video.save(os.path.join(app.config['UPLOAD_VIDEO_FOLDER'], new_filename))
        else:
            return 'Invalid file type', 400
    return 'File saved as {}'.format(new_filename), 200
    # Uniid  = request.json['Uniid']
    # Title = request.json['Title']
    # Body = request.json['Body']
    # Image = request.json['Image']
    # Video = request.json['Video']
    # Categorie  = request.json['Categorie']
    # User = request.json['User']
    # Visible = request.json['Visible']
    # addpost = Posts(Uniid,Title,Body,Image,Video,Categorie,User,Visible)
    # db.session.add(addpost)
    # db.session.commit()
    # newuser = user.jsonify(addpost)
    # if newuser:
    #     return "200" 

"""  Posts Fonctions end  """
if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)