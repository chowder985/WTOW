import json
import os
import sys
from forms import *
from flask import Flask, request, abort, jsonify, render_template, flash, redirect, url_for
from models import setup_db, StreamingPlatform, Movie
from auth.auth import AuthError, requires_auth
from datetime import date
from flask_cors import CORS

QUESTIONS_PER_PAGE = 8


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    def env_override(key):
        return os.getenv(key)

    app.jinja_env.globals.update(env_override=env_override)

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type, Authorization, true")
        response.headers.add("Access-Control-Allow-Methods",
                             "GET, PUT, PATCH, POST, DELETE, OPTIONS")
        return response

    @app.route('/')
    def index():
        return render_template('pages/home.html')

    @app.route('/streamingplatforms')
    def streamingplatforms():
        try:
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE

            platforms = StreamingPlatform.query.all()
            formatted_platforms = [platform.format() for platform in platforms]
            current_platforms = formatted_platforms[start:end]

            if len(current_platforms) == 0:
                abort(400)

            data = {
                "total_platforms": len(formatted_platforms),
                "current_platforms": current_platforms,
                "page": page
            }

            return render_template('pages/streamingplatforms.html', areas=data)
        except:
            print(sys.exc_info())
            abort(400)

    @app.route('/streamingplatforms/<int:stream_id>')
    def show_streamingplatform(stream_id):
        try:
            platform = StreamingPlatform.query.filter(
                StreamingPlatform.id == stream_id).one_or_none()
            if platform is None:
                abort(404)

            data = platform.format()
            movies = platform.movies
            formatted_movies = [movie.format() for movie in movies]
            for movie in movies:
                formatted_platforms = [platform.format()
                                       for platform in movie.streamingplatforms]
                for formatted_movie in formatted_movies:
                    if formatted_movie['id'] == movie.id:
                        formatted_movie['platforms'] = formatted_platforms

            data['movies'] = formatted_movies
            return render_template('pages/show_streamingplatform.html', platform=data)
        except:
            print(sys.exc_info())
            abort(404)

    @app.route('/streamingplatforms/new')
    def new_platform():
        form = StreamingForm(meta={'csrf': False})
        return render_template('pages/new_platform.html', form=form)

    @app.route('/streamingplatforms/new', methods=['POST'])
    @requires_auth('add:platforms')
    def new_platform_submission(payload):
        body = request.get_json()
        try:
            name = body.get('name', None)
            logo_url = body.get('logo_url', None)

            platform = StreamingPlatform(
                name=name, logo_url=logo_url, num_movies=0)
            platform.insert()
            flash('Platform ' + platform.name + ' was successfully listed!')
            return jsonify({
                'success': True
            })
        except:
            print(sys.exc_info())
            flash('An error occurred. Platform ' +
                  body['name'] + ' could not be listed.')
            abort(422)

    @app.route('/streamingplatforms/search', methods=['POST'])
    def search_platform():
        try:
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE

            platforms = StreamingPlatform.query.filter(StreamingPlatform.name.ilike(
                f"%{request.form.get('search_term', '')}%")).all()
            formatted_platforms = [platform.format() for platform in platforms]
            current_platforms = formatted_platforms[start:end]

            if len(current_platforms) == 0:
                abort(404)

            data = {
                "total_platforms": len(formatted_platforms),
                "current_platforms": current_platforms,
                "page": page
            }

            return render_template('pages/streamingplatforms.html', areas=data)
        except:
            print(sys.exc_info())
            abort(404)

    @app.route('/movies')
    def movies():
        try:
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE

            movies = Movie.query.all()
            formatted_movies = [movie.format() for movie in movies]
            for movie in movies:
                formatted_platforms = [platform.format()
                                       for platform in movie.streamingplatforms]
                for formatted_movie in formatted_movies:
                    if formatted_movie['id'] == movie.id:
                        formatted_movie['platforms'] = formatted_platforms

            current_movies = formatted_movies[start:end]

            if len(current_movies) == 0:
                abort(400)

            data = {
                "total_movies": len(formatted_movies),
                "current_movies": current_movies,
                "page": page
            }

            return render_template('pages/movies.html', movies=data)
        except:
            print(sys.exc_info())
            abort(400)

    @app.route('/movies/new')
    def new_movie():
        try:
            form = MovieForm(meta={'csrf': False})
            platforms = StreamingPlatform.query.all()
            formatted_platforms = [platform.format() for platform in platforms]
            form.ott_platform.choices = [
                (platform['name'], platform['name']) for platform in formatted_platforms]
            return render_template('pages/new_movie.html', form=form)
        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/movies/new', methods=['POST'])
    @requires_auth('add:movies')
    def new_movie_submission(payload):
        body = request.get_json()
        try:
            title = body.get('title', None)
            director = body.get('director', None)
            poster_url = body.get('poster_url', None)
            release_date = body.get('release_date', None)
            ott_platforms = body.get('ott_platform', None)

            # on successful db insert, flash success
            movie = Movie(title=title, director=director,
                          poster_url=poster_url, release_date=release_date)

            for platform_name in ott_platforms:
                platform = StreamingPlatform.query.filter(
                    StreamingPlatform.name == platform_name).one_or_none()
                if platform is None:
                    abort(404)

                platform.movies.append(movie)

                platform.num_movies += 1
                platform.insert()

            flash('Movie ' + movie.title +
                  ' was successfully listed!')
            return jsonify({
                'success': True
            })
        except:
            print(sys.exc_info())
            flash('An error occurred. Movie ' +
                  body['title'] + ' could not be listed.')
            abort(422)

    @app.route('/movies/search', methods=['POST'])
    def search_movie():
        try:
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE

            movies = Movie.query.filter(Movie.title.ilike(
                f"%{request.form.get('search_term', '')}%")).all()
            formatted_movies = [movie.format() for movie in movies]

            current_movies = formatted_movies[start:end]
            if len(current_movies) == 0:
                abort(404)

            data = {
                "total_movies": len(formatted_movies),
                "current_movies": current_movies,
                "page": page
            }

            return render_template('pages/movies.html', movies=data)
        except:
            print(sys.exc_info())
            abort(404)

    @app.route('/movies/<int:movie_id>/edit')
    def edit_movie(movie_id):
        try:
            form = MovieForm()
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            form.title.data = movie.title
            form.director.data = movie.director
            form.poster_url.data = movie.poster_url
            form.release_date.data = movie.release_date

            platforms = StreamingPlatform.query.all()
            formatted_platforms = [platform.format() for platform in platforms]
            form.ott_platform.choices = [
                (platform['name'], platform['name']) for platform in formatted_platforms]

            platform_names = [(platform.name, platform.name)
                              for platform in movie.streamingplatforms]
            form.ott_platform.data = platform_names

            return render_template('pages/edit_movie.html', form=form, movie=movie)
        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/movies/<int:movie_id>/edit', methods=['PATCH'])
    @requires_auth('edit:movies')
    def edit_movie_submission(payload, movie_id):
        try:
            body = request.get_json()
            title = body.get('title', None)
            director = body.get('director', None)
            poster_url = body.get('poster_url', None)
            release_date = body.get('release_date', None)
            ott_platforms = body.get('ott_platform', None)

            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            movie.title = title
            movie.director = director
            movie.poster_url = poster_url
            movie.release_date = release_date
            platforms = []
            for ott_platform in ott_platforms:
                platform = StreamingPlatform.query.filter(
                    StreamingPlatform.name == ott_platform).one_or_none()
                if platform is None:
                    abort(404)

                if movie not in platform.movies:
                    platform.movies.append(movie)

                platforms.append(platform)

            movie.streamingplatforms = platforms
            movie.update()

            for platform in StreamingPlatform.query.all():
                platform.num_movies = len(platform.movies)
                platform.update()

            return jsonify({
                'success': True,
                'edited': movie_id
            })
        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie_title = ''
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)
            movie_title = movie.title
            movie.delete()
            flash('Movie ' + movie_title + ' was successfully deleted!')

            for platform in StreamingPlatform.query.all():
                platform.num_movies = len(platform.movies)
                platform.update()

            return jsonify({
                'success': True,
                'deleted': movie_id
            })
        except:
            flash('An error occurred. Movie ' +
                  movie_title + ' could not be deleted.')
            print(sys.exc_info())
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource could not be found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(405)
    def wrong_approach(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(AuthError)
    def authentication_error(error):
        print(error.error)
        return jsonify({
            'success': False,
            'error': error.error['code'],
            'message': error.error['description']
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
