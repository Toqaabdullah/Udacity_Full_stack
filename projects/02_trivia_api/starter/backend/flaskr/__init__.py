import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys 


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"*" : {"origins": '*'}})


  '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')  
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/questions',methods=['GET'])
  def retrieve_questions():

    #Ten records pagination
    page=request.args.get('page',1,type=int)
    start=(page-1)*QUESTIONS_PER_PAGE
    end=start+QUESTIONS_PER_PAGE

    #To get questions
    questions=Question.query.order_by(Question.id).all()
    formatted_questions=[question.format() for question in questions]

    #To identify Categories according to ID
    categories=Category.query.all()
    formatted_catogories={}
    for category in categories:
      formatted_catogories[category.id]=category.type

    #error 404 in case of getting page out of range
    if (len(formatted_questions[start:end])==0):
      abort(404)

    #Return all requirements
    return jsonify({'success':True,'questions':formatted_questions[start:end] ,'total_questions': len(questions),'categories':formatted_catogories})

  @app.route('/categories',methods=['GET'])
  def retrieve_categories():
    #get categories
    categories=Category.query.all()
    formatted_catogories={}
    for category in categories:
      formatted_catogories[category.id]=category.type
    return jsonify({'success': True, 'categories':formatted_catogories})

  @app.route('/questions/<int:id>',methods=['DELETE'])
  def delete_questions(id):
    #filter the question which should be deleted
    try:
      question=Question.query.filter(Question.id==id).one_or_none()

      if question is None:
        abort(404)
     
     #delete the question and display the total questions after deletion
      question.delete()
      questions=Question.query.all()
      return jsonify({'success':True,'deleted':id,'total_questions':len(questions)})

    except:
      abort(422)

  @app.route('/questions',methods=['POST'])
  def post_question():
    #get the body from the request
    body=request.get_json()
      
    #assign the new records
    new_question=body.get('question',None)
    new_answer=body.get('answer',None)
    new_category=body.get('category',None)
    new_difficulty=body.get('difficulty',None)

    #insert the new question and display its ID & total questions
    try:
      question=Question(question=new_question,answer=new_answer,category=new_category,difficulty=new_difficulty)
      question.insert()
        
      questions=Question.query.all()
      return jsonify({'success':True,'created':question.id,'total_questions':len(questions)})

    except:
      abort(422)
  
  @app.route('/categories/<int:id>/questions',methods=['GET'])
  def post_question_by_category(id):
   
    #filter category according to endpoint
    try:
      
      category=Category.query.filter_by(id=id).one_or_none()
    
    #in case it is not found
      if category is None:
        abort(404)

    #get questions of the same category
      questions=Question.query.filter_by(category=id).all()
      formatted_questions=[question.format() for question in questions]
    

      return jsonify({'success':True,'questions': formatted_questions,'total_questions':len(formatted_questions)})

    except:
      abort(422)
      

  @app.route('/questions/search',methods=['POST'])
  def question_search():
    #get request keyword
    body=request.get_json()
    search=body.get('keyword')
    
    #search for keyword in the questions, return the result
    try:
      questions = Question.query.filter(Question.question.ilike(f'%{search}%')).all()
      formatted_questions=[question.format() for question in questions]

      return jsonify({'success':True,'questions': formatted_questions,'total_questions':len(formatted_questions)})

    except:
      abort(422)



  @app.route('/questions/quiz',methods=['POST'])
  def random_questions():
   
   #get category, previuos question from the request
    body=request.get_json()
    category=body.get('category',None)

    previous_question=body.get('previous_question',None)
    try:
      
      # get random question according to the given category if exists
      if(category):
        questions=Question.query.filter_by(category=category).all()

      else:
        questions=Question.query.all()

      random_question= questions[random.randrange(0,len(questions),1)]

      # if it is similar to the previous question, get another random question
      flag=True
      while flag:

        if str(random_question.id) in previous_question:
          random_question= questions[random.randrange(0,len(questions),1)]
    
        else:
          flag=False

      return jsonify({'success':True,'question': random_question.format()})

    except:
      print(sys.exc_info())
      abort(422)




      
  

  @app.route('/home')
  def home():
    return jsonify({'success': True}), 200
    
  

    

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''




  '''
  @DONE: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
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

    