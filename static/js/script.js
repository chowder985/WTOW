const JWTS_LOCAL_KEY = 'JWTS_LOCAL_KEY';
let token = '';

function set_jwt() {
    localStorage.setItem(JWTS_LOCAL_KEY, token);
}

function check_token_fragment() {
    // parse the fragment
    const fragment = window.location.hash.substr(1).split('&')[0].split('=');
    console.log(fragment);
    // check if the fragment includes the access token
    if (fragment[0] === 'access_token') {
        // add the access token to the jwt
        token = fragment[1];
        // save jwts to localstore
        this.set_jwt();
        alert('Successfully Logged In!')
    }
}

window.onload = () => {
    check_token_fragment()
    if (localStorage.getItem(JWTS_LOCAL_KEY)) {
        token = localStorage.getItem(JWTS_LOCAL_KEY);
    }
    console.log(token)
}

function getSelectValues(select) {
    var result = [];
    var options = select && select.options;
    var opt;

    for (var i = 0, iLen = options.length; i < iLen; i++) {
        opt = options[i];

        if (opt.selected) {
            result.push(opt.value || opt.text);
        }
    }
    return result;
}

const logoutBtn = document.getElementById('logout-btn')
logoutBtn.onclick = e => {
    token = '';
    set_jwt();
    alert('Successfully Logged Out!')
}

if (document.getElementById('new-platform-submit')) {
    const addPlatform = document.getElementById('new-platform-submit')
    addPlatform.onsubmit = e => {
        e.preventDefault();
        fetch('/streamingplatforms/new', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({
                name: document.getElementById('name').value,
                logo_url: document.getElementById('logo_url').value
            })
        })
            .then(res => {
                return res.json()
            })
            .then(jsonRes => {
                if (jsonRes.success) {
                    console.log('Success: ' + jsonRes.success)
                } else {
                    alert('Error: ' + jsonRes.error + '\n' + jsonRes.message)
                }
                window.location.replace('/streamingplatforms')
            })
            .catch(e => {
                console.log(e)
            })
    }
}

if (document.getElementById('new-movie-submit')) {
    const addMovie = document.getElementById('new-movie-submit')
    addMovie.onsubmit = e => {
        e.preventDefault()
        ott_platform = document.getElementById('ott_platform')
        fetch('/movies/new', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({
                title: document.getElementById('title').value,
                director: document.getElementById('director').value,
                poster_url: document.getElementById('poster_url').value,
                release_date: document.getElementById('release_date').value,
                ott_platform: getSelectValues(ott_platform)
            })
        })
            .then(res => {
                return res.json()
            })
            .then(jsonRes => {
                if (jsonRes.success) {
                    console.log('Success: ' + jsonRes.success)
                } else {
                    alert('Error: ' + jsonRes.error + '\n' + jsonRes.message)
                }
                window.location.replace('/movies')
            })
            .catch(e => {
                console.log(e)
            })
    }
}

if (document.getElementsByClassName('delete-movie')) {
    const deleteMovies = document.getElementsByClassName('delete-movie')
    for (const deleteMovie of deleteMovies) {
        deleteMovie.onclick = e => {
            movieId = e.target.dataset['id']
            fetch('/movies/' + movieId, {
                method: 'DELETE',
                headers: {
                    'Authorization': 'Bearer ' + token
                }
            })
                .then(res => {
                    return res.json()
                })
                .then(jsonRes => {
                    if (jsonRes.success) {
                        console.log('Success: ' + jsonRes.success)
                    } else {
                        alert('Error: ' + jsonRes.error + '\n' + jsonRes.message)
                    }
                    window.location.replace('/movies');
                })
                .catch(e => {
                    console.log(e)
                })
        }
    }
}

if (document.getElementById('edit-submit-form')) {
    const editMovie = document.getElementById('edit-submit-form')
    editMovie.onsubmit = function (e) {
        e.preventDefault()
        movieId = e.target.dataset['id']
        ott_platform = document.getElementById('ott_platform')
        fetch('/movies/' + movieId + '/edit',
            {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token
                },
                body: JSON.stringify({
                    title: document.getElementById('title').value,
                    director: document.getElementById('director').value,
                    poster_url: document.getElementById('poster_url').value,
                    release_date: document.getElementById('release_date').value,
                    ott_platform: getSelectValues(ott_platform)
                })
            })
            .then(res => {
                return res.json()
            })
            .then(jsonRes => {
                if (jsonRes.success) {
                    console.log('Success: ' + jsonRes.success)
                } else {
                    alert('Error: ' + jsonRes.error + '\n' + jsonRes.message)
                }
                window.location.replace('/movies')
            })
            .catch(e => {
                console.log(e)
            })
    }
}
