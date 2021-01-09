import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy.sql import func
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
cur_category = 1

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
  def after_request(res):
    res.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    res.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE')
    return res

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    formatted_categories = [category.type for category in categories]
    return jsonify({
      "categories": formatted_categories,
      "success": True
    })

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
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = Question.query.all()
    formatted_questions = [question.format() for question in questions]
    categories = Category.query.all()
    formatted_categories = [category.id for category in categories]

    return jsonify({
      "success": True,
      "questions": formatted_questions[start:end],
      "total_questions": len(formatted_questions),
      "categories": formatted_categories,
      "current_category":  cur_category
    })


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
    
      question.delete()
      return jsonify({
        "success": True,
        "message": "deleted",
      })
    except:
      abort(422) 

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def post_question():
    body = request.get_json()
    new_question_desc = body.get('question', None)
    new_question_answer = body.get('answer', None)
    new_question_diff = body.get('difficulty', None)
    new_question_cat = body.get('category', None)

    max_id = db.session.query(func.max(Question.id)).all()
    max_id = max_id[0][0]+1
    question = Question(question=new_question_desc, answer=new_question_answer, category=new_question_cat, difficulty=new_question_diff, id=max_id)
    question.insert()
    

    return jsonify({
      "success": True,
      "message": "created a new question",
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
  @app.route('/search_questions', methods=['POST'])
  def search_question():
    body = request.get_json()
    search_term = body['searchTerm']
    questions = Question.query.filter(Question.question.ilike("%"+search_term+"%")).all()
    formatted_questions = [question.format() for question in questions]
    return jsonify({
      "success": True,
      "questions": formatted_questions,
      "total_questions": len(formatted_questions),
      "currentCategory": cur_category,
    })


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_category_questions(category_id):
    category_id = category_id +1
    cur_category = category_id
    questions = Question.query.filter(Question.category == category_id).all()
    formatted_questions = [question.format() for question in questions]

    return jsonify({
      "success": True,
      "questions": formatted_questions,
      "total_questions": len(formatted_questions),
      "current_category":  cur_category
    })

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
  @app.route('/quizzes', methods=['POST'])
  def get_quiz_question():
    body = request.get_json()
    previous_questions = body['previous_questions']
    quiz_category = body['quiz_category']['type']
    questions = Question.query.filter(Question.category == quiz_category).all() 
    formatted_questions = [question.format() for question in questions]

    found_new_question = False
    question = formatted_questions[0]
    while(not found_new_question):
      rand_num = random.randint(0, len(formatted_questions)-1)
      question_id = formatted_questions[rand_num]['id']
      exist = False
      for q in previous_questions:
        if(q.id == question_id):
          exist = True
      if(not exist):
        found_new_question = True
        question = formatted_questions[rand_num]
      

    return jsonify({
      "success": True,
      "question": question
    })


  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "Not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
    }), 422  
    
  return app

    