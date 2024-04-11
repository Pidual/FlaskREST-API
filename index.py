from flask import Flask , request
from flask_restful import Api, Resource , reqparse , abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import random
#Para la base datos hacemos pip install sqlalchemy
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) #Un video siempre debe tener un nombre por eso el nullable
    views = db.Column(db.Integer , nullable=False)
    likes  = db.Column(db.Integer , nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"
       
# db.create_all() **importante ** no descomentar esto por que creariamos otra base de datos y se borrarian
# todas las filas

#Request Parser for video getting and putting
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name",type=str, help="Name of the video", required=True)
video_put_args.add_argument("views",type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes",type=int, help="Likes of the video", required=True)

#Request Parser for video patch
video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name",type=str, help="Name of the video")
video_update_args.add_argument("views",type=int, help="Views of the video")
video_update_args.add_argument("likes",type=int, help="Likes of the video")

resource_fields = {'id':fields.Integer,
                   'name': fields.String,
                   'views':fields.Integer,
                   'likes':fields.Integer}

# Utilizamos un diccionario para responder requests 
# The information we return is serializable python dictionaries are very similar 
# to jsons
# CRUD = CREATE, READ, UPDATE, DELETE
# GET solo retorna datos
# POST crea un nuevo dato
# PUT modificar un dato
# DELETE borrar un dato

#Metodos get put delete
class Video(Resource):

    @marshal_with(resource_fields) #Serializara el resultado con los resource_fields
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first() # busca una fila que tenga el mismo video_id
        if not result:
            abort(404, message="Video id doesnt exist")
        return result , 200

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id taken... ")
        video = VideoModel(id=video_id, name=args['name'],views=args['views'],likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_put_args.parse_args()
        video = VideoModel.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message="Video doesnt exists... ")
        if "name" in args:
            video.name = args['name']
        if "views" in args:
            video.views = args['views']
        if "likes" in args:
            video.likes = args['likes']
        db.session.add(video)
        db.session.commit()
        return video

    def delete(self, video_id):
        video_to_delete = VideoModel.query.filter_by(id=video_id).first()
        if not video_to_delete:
            abort(404, message="Video doesnt exists... ")
        db.session.delete(video_to_delete)
        db.commit()
        return 'Deleted Succesfully', 204

    @app.route('/')
    def hello():
        return 'Hello, this is a simple Flask app '+ str(random.randint(0, 100))

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True) 

