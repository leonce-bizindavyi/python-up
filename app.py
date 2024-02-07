from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,and_,Column, Integer, String, Text, DateTime
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import secrets


app=Flask(__name__)

CORS(app)
app.config["JWT_SECRET_KEY"] = "5T52472er8a7m272a00o" 
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:terama_20819p@localhost/terama_20819u'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['UPLOAD_VIDEO_FOLDER'] = '/home/xrdpuser/Desktop/uploads/Videos'
app.config['ALLOWED_VIDEO_EXTENSIONS'] = {'mp4', 'mov', 'avi', 'wmf' 'flv', 'webm','mkv'}


db = SQLAlchemy(app)
ma = Marshmallow(app)

class Posts(db.Model):
    ID = Column(Integer, primary_key=True)
    Uniid = Column(String(255, collation='utf8mb4_general_ci'), nullable=False)
    Title = Column(String(100, collation='utf8mb4_general_ci'), nullable=False)
    Body = Column(Text(collation='utf8mb4_general_ci'), nullable=True)
    Image = Column(String(255, collation='utf8mb4_general_ci'), nullable=True)
    Video = Column(String(255, collation='utf8mb4_general_ci'))
    Categorie = Column(String(100, collation='utf8mb4_general_ci'), nullable=True)
    User = Column(Integer, nullable=False)
    Short = Column(Integer, default=0)
    Visible = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.now)

    def __init__(self,Uniid,Title,Video,User,Visible):
        self.Uniid = Uniid
        self.Title = Title
        self.Video = Video
        self.User = User
        self.Visible = Visible

        
with app.app_context():
    db.create_all()

with app.app_context():
    db.create_all()

class PostSchema(ma.Schema):
    class Meta:
        fields = ('Uniid','Title','Video','User','Visible')        
    
post_schema = PostSchema()
posts_schema = PostSchema(many=True)

@app.route('/',methods=['GET'])
def index():
    return {'message':'Hello Upload'}

"""  Posts Fonctions begin  """
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_VIDEO_EXTENSIONS']
@app.route('/upload', methods=['POST'])
def add_posts():
    user_id = request.form.get('User')
    videoName = request.form.get('Video')

    if 'videos' not in request.files or not user_id:
        return 'Invalid request format', 400

    videos = request.files.getlist('videos')
    if len(videos) == 0:
        return 'No video selected for uploading', 400
    for video in videos:
        if video and allowed_file(video.filename):
            filename = secure_filename(video.filename)
            new_filename = videoName

            if not os.path.exists(app.config['UPLOAD_VIDEO_FOLDER']):
                os.makedirs(app.config['UPLOAD_VIDEO_FOLDER'])

            video.save(os.path.join(app.config['UPLOAD_VIDEO_FOLDER'], new_filename))
            Uniid = secrets.token_hex(4)
            Title = filename
            Video = new_filename
            User = user_id
            Visible = 0

            create_post = Posts(Uniid, Title, Video, User, Visible)
            db.session.add(create_post)
            db.session.commit()
        else:
            return 'Invalid file type', 400

    return jsonify({'Success': True, 'message': 'Files uploaded successfully'}), 200

"""  Posts Fonctions end  """


if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=False)
