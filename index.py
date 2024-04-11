from flask import Flask , request
from flask_restful import Api, Resource , reqparse , abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

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

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name",type=str, help="Name of the video", required=True)
video_put_args.add_argument("views",type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes",type=int, help="Likes of the video", required=True)

resource_fields = {'id':fields.String}

videos = {}

# Utilizamos un diccionario para responder requests 
# The information we return is serializable python dictionaries are very similar 
# to jsons
# CRUD = CREATE, READ, UPDATE, DELETE
# GET solo retorna datos
# POST crea un nuevo dato
# PUT modificar un dato
# DELETE borrar un dato

def abor_if_video_id_doesnt_exists(video_id):
    if video_id not in videos:
        abort(404, message="Video id is not valid...")

def abort_if_video_exists(video_id):
    if video_id in videos:
        abort(409, message="Video already exists with that ID")


class Video(Resource):
    def get(self, video_id):
        result = VideoModel.query.get(id=video_id) # busca una fila que tenga el mismo video_id
        return result

    #Argument Parses
    def put(self, video_id):
        abort_if_video_exists(video_id)
        args = video_put_args.parse_args()
        videos[video_id] = args #Args es un dicionario entonces todo bien haciendo esto
        return videos[video_id] , 201

    def delete(self, video_id):
        abor_if_video_id_doesnt_exists(video_id)
        del videos[video_id]
        return '', 204

    @app.route('/')
    def hello():
        return 'Hello, this is a simple Flask app'

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True) 

