import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate 
from models import setup_db, Actor,Movie
from auth.auth import AuthError, requires_auth
import sys
import traceback

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
  @requires_auth('get:actors')
  def get_actors(payload):
    try:
      actors=Actor.query.all()
      return jsonify( {"success": True, "actors": [actor.short() for actor in actors],'total_actors': len(actors)}),200

    except Exception as e:
      print('Error while doing something:', e)
      traceback.print_exc()

    
    


  @app.route('/movies',methods=['GET'])
  def get_movies():
    movies=Movie.query.all()
    return jsonify( {"success": True, "movies": [movie.short() for movie in movies],'total_movies': len(movies)}),200

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

  @app.route('/movies/<int:id>', methods=['PATCH'])
  def patch_movies(id):

    body=request.get_json()
        
    try:

      
      movie=Movie.query.filter_by(id=id).one_or_none()
    
      if movie is None:
        print(sys.exc_info())

        abort(404)

      new_title=body.get('title',None)
      new_release_date=body.get('release_date',None)

      if new_title:

        movie.title = new_title

      if new_release_date:

        movie.release_date = new_release_date

      movie.update()
      return jsonify({'success':True,'movie': [movie.short()]}),200

    except:
      print(sys.exc_info())

      abort(422)

  @app.route('/actors/<int:id>', methods=['PATCH'])
  def patch_actors(id):

    body=request.get_json()
        
    try:
      actor=Actor.query.filter_by(id=id).one_or_none()
    
      if actor is None:
        print(sys.exc_info())

        abort(404)

      new_name=body.get('name',None)
      new_age=body.get('age',None)
      new_gender=body.get('gender',None)
      new_movies_id= body.get('movies_id',None)

      if new_name:

        actor.name = new_name

      if new_age:
        actor.age = new_age

      if new_gender:
        actor.gender = new_gender

      if new_movies_id:
        actor.movies_id = new_movies_id

      actor.update()
      return jsonify({'success':True,'actors': [actor.short()]}),200

    except:
      print(sys.exc_info())

      abort(422)


  @app.route('/movies/<int:id>', methods=['DELETE'])
  def delete_drinks(id):
    try:


      movie=Movie.query.filter_by(id=id).one_or_none()
    
      if movie is None:
        abort(404)

      movie.delete()
      return jsonify({"success": True, "delete": id}),200

    except:
      abort(422)

  @app.route('/actors/<int:id>', methods=['DELETE'])
  def delete_actors(id):
    try:


      actor=Actor.query.filter_by(id=id).one_or_none()
    
      if actor is None:
        abort(404)

      actor.delete()
      return jsonify({"success": True, "delete": id}),200

    except:
      abort(422)



  
  @app.errorhandler(404)

  def not_found(error):
    

    return jsonify({

      "success": False, 

      "error": 404,
      "message": "Not Found"

      }), 404



  @app.errorhandler(400)

  def bad_request(error):
    

    return jsonify({

      "success": False, 

      "error": 400,
      "message": "Bad Request"

      }), 400

  @app.errorhandler(422)

  def unprcessable(error):
    

    return jsonify({

      "success": False, 

      "error": 422,
      "message": "Unprocessable"

      }), 422
  
  @app.errorhandler(500)

  def server_error(error):
    

    return jsonify({

      "success": False, 

      "error": 500,
      "message": "Internal Server Error"

      }), 500

  @app.errorhandler(405)

  def server_error(error):
    

    return jsonify({

      "success": False, 

      "error": 405,
      "message": "Method Not allowed"

      }), 405
  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)