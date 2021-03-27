$(document).ready(function(){
    M.Modal.init($('.modal'));

    $('#username').keydown(event => checkEnter(event.which, login));
    $('#password').keydown(event => checkEnter(event.which, login));

    $('#username-add').keydown(event => checkEnter(event.which, createUser));
    $('#password-add').keydown(event => checkEnter(event.which, createUser));
});


// Util to call function if enter is pressed
function checkEnter(key, callback) {
    if (key == 13) {
        callback();
    }
}


// Login functionality
function login() {
    const username = $('#username').val().trim();
    const password = $('#password').val().trim();

    $.post('/api/auth/', {
        username,
        password
    }).then(jwt => {
        localStorage.jwt = jwt;
        console.log(jwt);
        window.location.href = '/notes/';
    });
}


// User creation functionality
function createUser() {
    const username = $('#username-add').val().trim();
    const password = $('#password-add').val().trim();

    $.ajax({
        url: '/api/users/',
        type: 'PUT',
        data: {
            username,
            password
        }
    }).then(() => {
        window.location.href = window.location.href;
    });
}
