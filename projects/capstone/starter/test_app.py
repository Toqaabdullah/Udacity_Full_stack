#reference: 02_trivia_api test_flaskr.py template & lesson 4 in "3. API Development and Documentation" section

import unittest
import json
import os
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Actor,Movie


class CapstoneProjectTestCase(unittest.TestCase): 

    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "Capstone_test_db"
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

    def test_get_movies(self):

  
        response=self.client().get('/movies')
        #load the response data
        data= json.loads(response.data)

        #make sure from the expected data
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['title'])
        self.assertTrue(data['release_date'])
     