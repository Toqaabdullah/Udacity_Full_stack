#reference: 02_trivia_api test_flaskr.py template & lesson 4 in "3. API Development and Documentation" section

import unittest
import json
import os
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor,Movie


class CapstoneProjectTestCase(unittest.TestCase): 

    def setUp(self):

        with open('roles.json', 'r') as f:
            self.roles = json.loads(f.read())

        assistant_jwt = self.roles["list_of_roles"]["assistant"]["token"]

        director_jwt = self.roles["list_of_roles"]["director"]["token"]

        producer_jwt = self.roles["list_of_roles"]["producer"]["token"]
        self.authorization = {"assistant": f'Bearer {assistant_jwt}',"director": f'Bearer {director_jwt}',"producer": f'Bearer {producer_jwt}'}

        self.app = create_app()
        self.client = self.app.test_client
        #self.database_name = "Capstone_test_db"
        self.database_name = "testDB"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app) #, self.database_path)

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

  
        response=self.client().get('/movies', headers={'Authorization': self.authorization["assistant"]})
        #load the response data
        data= json.loads(response.data)

     
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['total_movies'])

    def test_get_movies_405(self):

  
        response=self.client().get('/movies/1', headers={'Authorization': self.authorization["assistant"]})
        #load the response data
        data= json.loads(response.data)

   
        self.assertEqual(response.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Method Not allowed')


    def test_get_actors(self):

  
        response=self.client().get('/actors', headers={'Authorization': self.authorization["assistant"]})
  
        data= json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['total_actors'])


    def test_get_actors_404(self):

  
        response=self.client().get('/actor', headers={'Authorization': self.authorization["assistant"]})
        
        data= json.loads(response.data)

   
        self.assertEqual(response.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Not Found')

 
    def test_post_movies(self):
        movies={    "title": "Al Garima","release_date": "01/05/2022"}
        response = self.client().post('/movies', json=movies, headers={'Authorization': self.authorization["producer"]})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movies'])

    def test_post_movies_422(self):

        movies={ "release_date": "01/05/2022"}
        response = self.client().post('/movies', json=movies, headers={'Authorization': self.authorization["producer"]})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Unprocessable')

    def test_post_actors(self):
        actors={    "name": "Ahmed Ezz", "age": "50","gender": "male"}
        response = self.client().post('/actors', json=actors, headers={'Authorization': self.authorization["director"]})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['actors'])

    def test_post_actors_422(self):

        actors={ "n": "Ahmed Ezz", "a": "50","g": "male"}
        response = self.client().post('/actors', json=actors, headers={'Authorization': self.authorization["director"]})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Unprocessable')

    def test_patch_movies(self):
        movie={    "title": "Tito","release_date": "06/23/2004"}
        response = self.client().patch('/movies/3', json=movie, headers={'Authorization': self.authorization["director"]})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movie'])

    def test_patch_movies_422(self):

        movie={ "title": "Tito","release_date": 10 }
        response = self.client().patch('/movies/3', json=movie, headers={'Authorization': self.authorization["director"]})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Unprocessable')

    def test_patch_actors(self):
        actor={    "name": "Ahmed Elsakka", "age": 48 }
        response = self.client().patch('/actors/3', json=actor, headers={'Authorization': self.authorization["director"]})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['actors'])

    def test_patch_actors_422(self):

        actor={ "movies_id": 1000 }
        response = self.client().patch('/actors/3', json=actor, headers={'Authorization': self.authorization["director"]})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Unprocessable')

    def test_delete_movies(self):

        response = self.client().delete('/movies/1', headers={'Authorization': self.authorization["producer"]})
        data=json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        #self.assertTrue(data['id'])
"""
    def test_delete_movies_404(self):

        response = self.client().delete('/movies/')
        data=json.loads(response.data)

        self.assertEqual(response.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Not Found')


    def test_delete_actors(self):

        response = self.client().delete('/actors/1')
        data=json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        #self.assertTrue(data['id'])

    def test_delete_actors_422(self):

        response = self.client().delete('/actors/5000')
        data=json.loads(response.data)

        self.assertEqual(response.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Unprocessable')
     

    """



if __name__ == "__main__":
    unittest.main()
     