import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate 
from models import setup_db, Actor,Movie

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/*": {"origins": "*"}})
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')  
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
    return response

  @app.route('/home')
  def home():
    return jsonify({'success': True}), 200


  @app.route('/actors',methods=['GET'])
  def get_actors():

    actors=Actor.query.all()
    return jsonify( {"success": True, "actors": [actor.short() for actor in actors]}),200


  @app.route('/movies',methods=['GET'])
  def get_movies():
    movies=Movie.query.all()
    return jsonify( {"success": True, "movies": [movie.short() for movie in movies]}),200

  @app.route('/actors',methods=['POST'])
  def post_actors():
    body=request.get_json()
    new_name=body.get('name',None)
    new_age=body.get('age',None)
    new_gender=body.get('gender',None)
    new_movies_id= body.get('movies_id',None)

    try:

      actors=Actor(name=new_name,age=new_age,gender=new_gender,movies_id=new_movies_id)
      actors.insert()
        
       
      return jsonify({'success':True,'actors': [actors.short()]}),200

    except:

      print(sys.exc_info())
      abort(422)

  @app.route('/movies',methods=['POST'])
  def post_movies():
    body=request.get_json()
    new_title=body.get('title',None)
    new_release_date=body.get('release_date',None)
    #new_actors=body.get('actors',None)

    try:

      movies=Movie(title=new_title,release_date=new_release_date)
      movies.insert()
        
       
      return jsonify({'success':True,'movies': [movies.short()]}),200

    except:

      print(sys.exc_info())
      abort(422)

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)