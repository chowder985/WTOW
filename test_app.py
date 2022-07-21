import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, StreamingPlatform


class WTOWTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "wtow_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_streamingplatform = {
            "name": "Watcha", "logo_url": "https://wtow-images.s3.us-east-2.amazonaws.com/watcha.png"}
        self.new_movie = {"title": "Thor: Love and Thunder", "director": "Ilhoon Lee", "release_date": "2022-07-05",
                          "poster_url": "https://media-cache.cinematerial.com/p/500x/w6vxvchp/thor-love-and-thunder-movie-poster.jpg?v=1653357775", "ott_platform": ["Netflix"]}
        self.admin_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkprSmdla2hsSkh3UTJENlk5LThCVCJ9.eyJpc3MiOiJodHRwczovL2Rldi0zenAxbC1oYS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJkODE5MTg2ZDUzNzAwNTJkMzAwNjFlIiwiYXVkIjoid3RvdyIsImlhdCI6MTY1ODMzNzQxMiwiZXhwIjoxNjU4MzQ0NjEyLCJhenAiOiIxWkJ0ekxsTlFGYnZYUDRpTVJKOHliaWx3RVVaVXN1UCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOm1vdmllcyIsImFkZDpwbGF0Zm9ybXMiLCJkZWxldGU6bW92aWVzIiwiZWRpdDptb3ZpZXMiXX0.UfSO4BkaUdH5BNwh8gOe4v_A2mEHQqT6iChT0e5CqxjqSW4Ie_ePGBUZZj7zPP_kRBjzpxGZjnqAIf7K6d658khPFrlNai5ukPAlqt_aJUDxWQ1gBPV1_7ox0yUzTc3qOHGYwCmMbwcavoyzqPVd6vra4RJBFpGBpHc4vjVMqD6PNZqoTAfP-BzL9xasoCjZvebkeTQ8IAUQlpC9Yu-nrQ8ViMITdZVZncIES6TlY7W7T0YwEt_IYQnPGBCT2eVbSfu6rg8XU5xuu8Vf127TWqb5Om5-EFd81vBjM9FQ0oiPhKsrZKbIt11_Ufc0tKVgL5S0Y0Ixv31awEA4dCkcPA'
        self.viewer_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkprSmdla2hsSkh3UTJENlk5LThCVCJ9.eyJpc3MiOiJodHRwczovL2Rldi0zenAxbC1oYS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJkNTZiOWYzYWEwNjQyMWZjMWZiMzgyIiwiYXVkIjoid3RvdyIsImlhdCI6MTY1ODMzODY0MywiZXhwIjoxNjU4MzQ1ODQzLCJhenAiOiIxWkJ0ekxsTlFGYnZYUDRpTVJKOHliaWx3RVVaVXN1UCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOm1vdmllcyIsImVkaXQ6bW92aWVzIl19.zue5Q4dE9X3vteqWvGtEwLiyomPhFRnvD2BAzznAIaOnAmoowexINCtsnt7tau3bf7NqT0IBwa7XkTmCpPUWQHw5t8V6YC5xIIMFhpz4scxH3P7B4E8ZpIAOUIi64aWgt96dDuixq9BCHdq-1fyxrZnTIxmJ8x6ACJgJH0uT_5mEcET2sMmTJX7lZmB5KoDG0HQltBLd5p2koajjmqaEJSM-p09CxTX5fmdIvUE5tKwblJAT8x0bXXhHEf55vz6VQDE4iOwIlXcKik_pIWiip_ZwxJKBAhQ3u7eqq4gVeoeWGEVlNiqjgHqXRrUppxTWQAuZjQdyYO71NsCM042Jgg'

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_home_success(self):
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)

    def test_home_method_not_allowed(self):
        res = self.client().post('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'method not allowed')

    # Streaming Platform Tests

    def test_new_streamingplatform_success(self):
        res = self.client().get('/streamingplatforms/new')

        self.assertEqual(res.status_code, 200)

    def test_new_streamingplatform_method_not_allowed(self):
        res = self.client().delete('/streamingplatforms/new')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'method not allowed')

    def test_submit_new_platform_success(self):
        res = self.client().post('/streamingplatforms/new', headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.admin_jwt},
                                 json=self.new_streamingplatform)
        data = json.loads(res.data)

        platform = StreamingPlatform.query.filter(
            StreamingPlatform.name == self.new_streamingplatform['name']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(platform)

    def test_submit_new_platform_does_not_have_permission(self):
        res = self.client().post('/streamingplatforms/new',
                                 headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.viewer_jwt}, json=self.new_streamingplatform)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 'does_not_have_permission')
        self.assertEqual(data['message'], 'The user does not have permission')

    def test_streamingplatforms_success(self):
        res = self.client().get('/streamingplatforms')

        self.assertEqual(res.status_code, 200)

    def test_show_platforms_beyond_valid_page(self):
        res = self.client().get('/streamingplatforms?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad request')

    def test_show_streamingplatform_success(self):
        res = self.client().get('/streamingplatforms/1')

        platform = StreamingPlatform.query.filter(
            StreamingPlatform.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(platform)

    def test_show_streamingplatform_not_found(self):
        res = self.client().get('/streamingplatforms/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource could not be found')

    def test_search_platform_success(self):
        res = self.client().post(
            '/streamingplatforms/search', data={"search_term": "net"})

        platforms = StreamingPlatform.query.filter(StreamingPlatform.name.ilike(
            f"%net%")).all()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(platforms)

    def test_search_platform_not_found(self):
        res = self.client().post('/streamingplatforms/search',
                                 data={"search_term": "watcjkdjflaskfjd"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource could not be found')

    # Movies Test

    def test_submit_new_movie_success(self):
        res = self.client().post('/movies/new',
                                 headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.admin_jwt}, json=self.new_movie)
        data = json.loads(res.data)

        movie = Movie.query.filter(
            Movie.title == self.new_movie['title']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(movie)

    def test_submit_new_movie_authorization_header_missing(self):
        res = self.client().post('/movies/new', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 'authorization_header_missing')
        self.assertEqual(data['message'], 'Authorization header is expected')

    def test_movies_success(self):
        res = self.client().get('/movies')

        movies = Movie.query.all()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(movies)

    def test_show_movies_beyond_valid_page(self):
        res = self.client().get('/movies?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad request')

    def test_new_movie_success(self):
        res = self.client().get('/movies/new')

        self.assertEqual(res.status_code, 200)

    def test_new_movie_method_not_allowed(self):
        res = self.client().delete('/movies/new')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'method not allowed')

    def test_search_movie_success(self):
        res = self.client().post(
            '/movies/search', data={"search_term": "top"})

        movies = Movie.query.filter(Movie.title.ilike(
            f"%top%")).all()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(movies)

    def test_search_movie_not_found(self):
        res = self.client().post('/movies/search',
                                 data={"search_term": "fjdksfjdslk"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource could not be found')

    def test_show_edit_movie_success(self):
        res = self.client().get('/movies/1/edit')

        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(movie)

    def test_show_edit_movie_unprocessable(self):
        res = self.client().get('/movies/1000/edit')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable')

    def test_edit_movie_success(self):
        res = self.client().patch('/movies/2/edit', headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.viewer_jwt}, json={"title": "Jurassic World: Dominion", "director": "Ilhoon Lee", "release_date": "2022-05-05",
                                                                                                                                                      "poster_url": "https://media-cache.cinematerial.com/p/500x/evkyojkp/jurassic-world-dominion-movie-poster.jpg?v=1654959848", "ott_platform": ["Disney+"]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['edited'], 2)

    def test_edit_movie_authorization_header_missing(self):
        res = self.client().patch('/movies/1000/edit', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 'authorization_header_missing')
        self.assertEqual(data['message'], 'Authorization header is expected')

    def test_delete_movie_success(self):
        res = self.client().delete('/movies/10',
                                   headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.admin_jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 10)

    def test_delete_movie_does_not_have_permission(self):
        res = self.client().delete('/movies/1000',
                                   headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.viewer_jwt})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 'does_not_have_permission')
        self.assertEqual(data['message'], 'The user does not have permission')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
