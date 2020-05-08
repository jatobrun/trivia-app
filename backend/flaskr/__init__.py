import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys
from models import setup_db, Question, Category
import json
from sqlalchemy.sql.expression import func
QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  db = setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    formatted_categories = {}
    if categories:
      for category in categories:
        formatted_categories[category.id] = category.type

      return jsonify({
          'success':True,
          'categories': formatted_categories
      })
    else:
      abort(404)

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
  @app.route('/questions')
  def get_questions():
    current_category = request.args.get('current_category', 1, type = int)
    page = request.args.get('page', 1, type = int)
    start = (page - 1)*QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    categories = Category.query.all()
    formatted_categories = {}
    for category in categories:
      formatted_categories[category.id] = category.type
    questions = Question.query.filter()
    formatted_questions = [question.format() for question in questions]
    return jsonify({
        'success': True,
        'questions': formatted_questions[start:end],
        'total_questions': len(formatted_questions),
        'categories': formatted_categories,
        'current_category': current_category
    })
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<question_id>', methods = ['DELETE'])
  def delete_question(question_id):
    error = False
    try:
      question = Question.query.filter_by(id = question_id).delete()
      db.session.commit()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()
    if error:
      abort(404)
    else:
      return jsonify({
          'success': True,
          'message': 'Delete is completed'
      })
      

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods = ['POST'])
  def post_question():
    error = False
    data = request.data
    data_dictionary = json.loads(data)
    try:
      question = data_dictionary['question']
      answer = data_dictionary['answer']
      category = data_dictionary['category']
      difficulty = data_dictionary['difficulty']
      question = Question(question = question, answer = answer, category = category, difficulty = difficulty).insert()
    except:
      db.session.rollback()
      error = True
      print(sys.exc_info())
    finally:
      db.session.close()
    if error: 
      abort(422)
    else:
      return jsonify({
          'success': True,
          'message': 'Create is completed'
      })
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods = ['POST'])
  def search_question():
    error = False
    data = request.data
    data_dictionary = json.loads(data)
    search_term = f"%{data_dictionary['searchTerm']}%"
    questions = Question.query.filter(Question.question.ilike(search_term)).all()
    if questions:
      questions_formatted = [question.format() for question in questions]
      current_category = request.args.get('current_category')
      return jsonify({
          'questions': questions_formatted,
          'total_questions': len(questions_formatted),
          'current_category': current_category,
          'success': True
      })
    else:
      print(sys.exc_info())
      abort(404)
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<category_id>/questions')
  def show_questions(category_id):
    questions = Question.query.filter_by(category = category_id).all()
    current_category = request.args.get('current_category')
    if questions:
      formatted_questions = [question.format() for question in questions]
      return jsonify({
          'success': True,
          'questions': formatted_questions,
          'total_questions': len(formatted_questions),
          'current_category': current_category
      })
    else:
      abort(404)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods = ['POST'])
  def create_quiz():
    error = False
    data = request.data
    data_dictionary = json.loads(data)
    try:
      questions = Question.query.filter_by(category = data_dictionary['quiz_category']['id']).order_by(func.random())
      formatted_questions = [question.format() for question in questions]
    except:
      error = True
      print(sys.exc_info())
    if error:
      abort(422)
    else:
      return jsonify({
          'question': formatted_questions[0],
          'success': True
      })
      
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not Found'
    }), 404
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': "Unprocessable"
    }), 422
  return app

    