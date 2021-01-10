import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = 'postgresql://postgres:@localhost:5432/trivia'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_fail_get_categories(self):
        res = self.client().get('/category')
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)    

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_fail_get_questions(self):
        res = self.client().get('/question')

        self.assertEqual(res.status_code, 404)

    def test_delete_question(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data.decode('utf-8'))

        question = Question.query.filter(Question.id == 1).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question, None)

    def test_fail_delete_question(self):
        res = self.client().delete('/questions/10000')

        self.assertEqual(res.status_code, 422)
        
            

    def test_add_question(self):
        new_question = {
            "question": "Knock knock, who is there?",
            "answer": "noone",
            "difficulty": 2,
            "category": 3
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "created a new question")

    def test_fail_add_question(self):
        new_question = {
            "question": "Knock knock, who is there?",
            "answer": "noone",
            "difficulty": 2,
            "category": 3
        }
        res = self.client().post('/question', json=new_question)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)
         

    def test_search_question(self):
        searchTerm = {
            "searchTerm": "actor",
        }
        res = self.client().post('/search_questions', json=searchTerm)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)        
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_fail_search_question(self):
        searchTerm = {
            "searchTerm": "actor",
        }
        res = self.client().post('/searchquestions', json=searchTerm)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)

    def test_get_category_questions(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data.decode('utf-8'))
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    
    def test_fail_get_category_questions(self):
        res = self.client().get('/category/1/questions')
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 404)
        

    def test_get_quiz_questions(self):
        data = {
            "previous_questions": [],
            "quiz_category": {"id": 1, "type": 2}
        }
        res = self.client().post('/quizzes', json=data)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))   

    def test_fail_get_quiz_questions(self):
        data = {
            "previous_questions": [],
            "quiz_category": {"id": 1, "type": 2}
        }
        res = self.client().post('/quizz', json=data)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)  

    def test_404(self):
        res = self.client().post('/quiz')
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not found")

    
    def test_422(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()