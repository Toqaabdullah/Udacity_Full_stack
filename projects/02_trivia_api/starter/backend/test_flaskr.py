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
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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

    def test_get_paginated_questions(self):

        #response equals to the client get endpoint
        response=self.client().get('/questions')
        #load the response data
        data= json.loads(response.data)

        #make sure from the expected data
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_404_sent_requesting_beyond_valid_page(self):

        response=self.client().get('/questions?page=1000')
        data=json.loads(response.data)

        self.assertEqual(response.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Not Found')

    def test_categeories(self):
        response=self.client().get('/categories')
        data= json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])

    def test_404_for_invalid_category(self):

        response=self.client().get('catogories?page=1000')
        data=json.loads(response.data)

        self.assertEqual(response.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Not Found')

  

    def test_delete_questions(self):
        

        response = self.client().delete('/questions/2')
        data=json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['deleted'])
        self.assertTrue(data['total_questions'])

    def invalid_deletion_404(self):

        response = self.client().delete('/questions/1000')
        data=json.loads(response.data)

        self.assertEqual(response.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Not Found')


    def test_post_question(self):

        question={
            'question':'what is the new question?',
            'answer': 'answer',
            'difficulty': 1,
            'category':5
        }

        response = self.client().get('/questions', json=question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])

    def post_question_422(self):

        question={
            'question':'what is the new question?',
            'answer': 'answer',
            'difficulty': 1,
            'category':50
        }
        response = self.client().post('/questions', json=question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Unprocessable')

    def test_post_question_by_category(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def post_question_by_category_404 (self):
        response = self.client().get('/categories/50/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Not Found')

    def test_question_search(self):

        keyword={'keyword':'wh'}
        response = self.client().post('/questions/search', json=keyword)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def search_question_bad_request(self):

        keyword={'keyword'}
        response = self.client().post('/questions/search', json=keyword)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Bad Request')

    def test_quiz(self):

        previous_question={ 'previous_question':'5'}
        response = self.client().post('/questions/quiz', json=previous_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['question'])

    def quiz_fails_500(self):

        response = self.client().post('/questions/search')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Internal Server Error')









    





        




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()