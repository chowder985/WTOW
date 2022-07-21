## WTOW Reference

### Motivation
- As the boom of streaming platforms are on the rise, I have felt the need to locate which movies I could stream on which platforms.

### Getting Started
- Base URL: https://wtow-985841.herokuapp.com/ 
- Authentication: This app has two roles.
    - Roles: 
        - 1. Viewer: can perform the following actions, [add:movies, edit:movies]
        - 2. Admin: can perform the following actions, [add:platforms, add:movies, edit:movies, delete:movies]
    - Reviewers may use the below accounts to test all endpoints.
        - Viewer account
        ```
        Username: test1@fsnd.com
        Password: Abcdef123!
        ```
        - Admin account
        ```
        Username: test2@fsnd.com
        Password: Abcdef123!
        ```

### Development Setup
To start and run the local development server,
1. Initialize and activate a virtualenv:
```
$ cd YOUR_PROJECT_DIRECTORY_PATH/
$ python -m venv env
$ source env/bin/activate
```
2. Install the dependencies:
```
$ pip3 install -r requirements.txt
```
3. Run the development server:
```
$ python app.py
```

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "Resource could not be found"
}
```
The API will return five error types when requests fail:
- 400: Bad request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable 
- Authentication Error: varies by error

### Endpoints
#### GET /
- General:
    - Main page for this web app.
    - Returns a jinja template that renders home.html.
- Sample: `curl https://wtow-985841.herokuapp.com/`

#### GET /streamingplatforms
- General:
    - Retrieves all the streaming platforms from the DB.
    - Returns a jinja template that renders streamingplatforms.html, which contains a list of streaming platforms.
    - Results are paginated in groups of 8. Include a request argument to choose page number, starting from 1. 
- Sample: `curl https://wtow-985841.herokuapp.com/streamingplatforms`

#### GET /streamingplatforms/{platform_id}
- General:
    - Shows the movies that are streamable on the streaming platform with id {platform_id}.
    - Returns a jinja template that renders show_streamingplatform.html, which contains a list of movies that are streamable on the platform with id {platform_id}.
    - Results are paginated in groups of 8. Include a request argument to choose page number, starting from 1. 
- Sample: `curl https://wtow-985841.herokuapp.com/streamingplatforms/1`

#### GET /streamingplatforms/new
- General:
    - Renders a form to submit to add new streaming platform.
    - Returns a jinja template that renders new_platform.html
- Sample: `curl https://wtow-985841.herokuapp.com/streamingplatforms/new`

#### POST /streamingplatforms/new
- General:
    - Creates a new streaming platform with a name and logo url.
    - If the post request went through, it will return the success value of true.
    - Otherwise, it will return the success value of false with the following error and message.
- Samples: 
    - Create platform: `curl https://wtow-985841.herokuapp.com/streamingplatforms/new -X POST -H "Content-Type: application/json, Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkprSmdla2hsSkh3UTJENlk5LThCVCJ9.eyJpc3MiOiJodHRwczovL2Rldi0zenAxbC1oYS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJkOTFiMDk5ZTYzMWQ5MTM3N2EwYTM1IiwiYXVkIjoid3RvdyIsImlhdCI6MTY1ODQwMDI5MywiZXhwIjoxNjU4NDA3NDkzLCJhenAiOiIxWkJ0ekxsTlFGYnZYUDRpTVJKOHliaWx3RVVaVXN1UCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOm1vdmllcyIsImFkZDpwbGF0Zm9ybXMiLCJkZWxldGU6bW92aWVzIiwiZWRpdDptb3ZpZXMiXX0.BIL0eoSCDPPPzVe4C5QwB6QSz0WeZKjusojdSs-O1zJQZXhgH0ia2BjPaRUWirdKHnarYNBiJ_uXePomFKKDayz0YB77lCq3PjkRRPurVqMWp_gFF-pn5KDBYS_8Zdq4Zl1rsk9TNJdlxlYlnj0o_-ZFI4OCGEZMJwORJoKgP5A_1pR6DAuciFSNQdVmRjcWOvhPjbNpFYDOclx2GkNrmd-v7qxBpxkTEwzpPtZ_AWYL2u29AlZRpahjtXszZBxSOmTE6rY1McQtGC-q4i7zOOh0vCxUbC6EjilDdVDlqKJ04vFM5Kku1GSoJrFInIGCs6660oZpUtFpa1o1_qk3IQ" -d '{"name": "Watcha", "logo_url": "https://wtow-images.s3.us-east-2.amazonaws.com/watcha.png"}'`

```
{
  "success": true
}
```

#### POST /streamingplatforms/search
- General:
    - Searches for a streaming platform.
    - Returns a jinja template that renders streamingplatforms.html with the resulting platforms.
- Samples: 
    - Create platform: `curl https://wtow-985841.herokuapp.com/streamingplatforms/search -X POST -d '{"search_term": "net"}'`

#### GET /movies
- General:
    - Retrieves all the movies from the DB.
    - Returns a jinja template that renders movies.html, which contains a list of all movies.
    - Results are paginated in groups of 8. Include a request argument to choose page number, starting from 1. 
- Sample: `curl https://wtow-985841.herokuapp.com/movies`

#### GET /movies/new
- General:
    - Renders a form to submit to add new movie.
    - Returns a jinja template that renders new_movie.html
- Sample: `curl https://wtow-985841.herokuapp.com/movies/new`

#### POST /movies/new
- General:
    - Creates a new movie with a title, director, release date, poster url, and streaming platforms.
    - If the post request went through, it will return the success value of true.
- Samples: 
    - Create movie: `curl https://wtow-985841.herokuapp.com/movies/new -X POST -H "Content-Type: application/json, Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkprSmdla2hsSkh3UTJENlk5LThCVCJ9.eyJpc3MiOiJodHRwczovL2Rldi0zenAxbC1oYS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJkOTE5NjdlNjNlZGJkYWExN2E1YmM2IiwiYXVkIjoid3RvdyIsImlhdCI6MTY1ODQwMTcxOSwiZXhwIjoxNjU4NDA4OTE5LCJhenAiOiIxWkJ0ekxsTlFGYnZYUDRpTVJKOHliaWx3RVVaVXN1UCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOm1vdmllcyIsImVkaXQ6bW92aWVzIl19.1MdGh0mmM9NoAqyinyybEr2voXLHhtM6ckqG8N2qGwXYONz-Uy1eDw-eIkTywiYnZOFJe3oZ8-pfh9C3w0-haXtYNHYumKNnYTvfg9WUIpsO9AkxD4C4-8hK3IYZYMY0SBbxyfGv-GlrllXAV6UiF21pPmH1l2kbwbtOfQ3rjhn7QYNk9MfI0HBy0qLi0QXjgw1d0HR8w1YdM_8seDTA0Nz51PUu8wvtlLqv-mLX84Z_o3f9a0wixN6K-wG3SrwmMcGgy7t_hj5MBLoH0I9tfm5jCDEDXj6CvPPb8esHaDbPCEcXX81Gbzi885bhrM8X4vqOQM8zZ6WHrdY40ColoA" -d '{"title": "Thor: Love and Thunder", "director": "Ilhoon Lee", "release_date": "2022-07-05","poster_url": "https://media-cache.cinematerial.com/p/500x/w6vxvchp/thor-love-and-thunder-movie-poster.jpg?v=1653357775", "ott_platform": ["Netflix"]}'`

```
{
  "success": true
}
```

#### POST /movies/search
- General:
    - Searches for movies that match the search term.
    - Returns a jinja template that renders movies.html with the resulting movies.
- Samples: 
    - Create platform: `curl https://wtow-985841.herokuapp.com/movies/search -X POST -d '{"search_term": "about"}'`

#### GET /movies/{movie_id}/edit
- General:
    - Renders a form to edit the movie with id {movie_id}.
    - Returns a jinja template that renders edit_movie.html
- Sample: `curl https://wtow-985841.herokuapp.com/movies/1/edit`

#### PATCH /movies/{movie_id}/edit
- General:
    - Modifies the movie with id {movie_id} according to the submitted data.
    - If the post request went through, it will return the success value of true and id of the edited movie
- Samples: 
    - Edit movie: `curl https://wtow-985841.herokuapp.com/movies/1/edit -X PATCH -H "Content-Type: application/json, Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkprSmdla2hsSkh3UTJENlk5LThCVCJ9.eyJpc3MiOiJodHRwczovL2Rldi0zenAxbC1oYS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJkOTE5NjdlNjNlZGJkYWExN2E1YmM2IiwiYXVkIjoid3RvdyIsImlhdCI6MTY1ODQwMTcxOSwiZXhwIjoxNjU4NDA4OTE5LCJhenAiOiIxWkJ0ekxsTlFGYnZYUDRpTVJKOHliaWx3RVVaVXN1UCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOm1vdmllcyIsImVkaXQ6bW92aWVzIl19.1MdGh0mmM9NoAqyinyybEr2voXLHhtM6ckqG8N2qGwXYONz-Uy1eDw-eIkTywiYnZOFJe3oZ8-pfh9C3w0-haXtYNHYumKNnYTvfg9WUIpsO9AkxD4C4-8hK3IYZYMY0SBbxyfGv-GlrllXAV6UiF21pPmH1l2kbwbtOfQ3rjhn7QYNk9MfI0HBy0qLi0QXjgw1d0HR8w1YdM_8seDTA0Nz51PUu8wvtlLqv-mLX84Z_o3f9a0wixN6K-wG3SrwmMcGgy7t_hj5MBLoH0I9tfm5jCDEDXj6CvPPb8esHaDbPCEcXX81Gbzi885bhrM8X4vqOQM8zZ6WHrdY40ColoA" -d '{"title": "Jurassic World: Dominion", "director": "Ilhoon Lee", "release_date": "2022-05-05","poster_url": "https://media-cache.cinematerial.com/p/500x/evkyojkp/jurassic-world-dominion-movie-poster.jpg?v=1654959848", "ott_platform": ["Disney+"]}'`

```
{
  "success": true
  "edited": 1
}
```

#### DELETE /movies/{movie_id}
- General:
    - Deletes the movie with id {movie_id}.
    - If the post request went through, it will return the success value of true and id of the deleted movie
- Samples: 
    - Edit movie: `curl https://wtow-985841.herokuapp.com/movies/1 -X DELETE -H "Content-Type: application/json, Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkprSmdla2hsSkh3UTJENlk5LThCVCJ9.eyJpc3MiOiJodHRwczovL2Rldi0zenAxbC1oYS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJkOTFiMDk5ZTYzMWQ5MTM3N2EwYTM1IiwiYXVkIjoid3RvdyIsImlhdCI6MTY1ODQwMDI5MywiZXhwIjoxNjU4NDA3NDkzLCJhenAiOiIxWkJ0ekxsTlFGYnZYUDRpTVJKOHliaWx3RVVaVXN1UCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOm1vdmllcyIsImFkZDpwbGF0Zm9ybXMiLCJkZWxldGU6bW92aWVzIiwiZWRpdDptb3ZpZXMiXX0.BIL0eoSCDPPPzVe4C5QwB6QSz0WeZKjusojdSs-O1zJQZXhgH0ia2BjPaRUWirdKHnarYNBiJ_uXePomFKKDayz0YB77lCq3PjkRRPurVqMWp_gFF-pn5KDBYS_8Zdq4Zl1rsk9TNJdlxlYlnj0o_-ZFI4OCGEZMJwORJoKgP5A_1pR6DAuciFSNQdVmRjcWOvhPjbNpFYDOclx2GkNrmd-v7qxBpxkTEwzpPtZ_AWYL2u29AlZRpahjtXszZBxSOmTE6rY1McQtGC-q4i7zOOh0vCxUbC6EjilDdVDlqKJ04vFM5Kku1GSoJrFInIGCs6660oZpUtFpa1o1_qk3IQ"`

```
{
  "success": true
  "deleted": 1
}
```