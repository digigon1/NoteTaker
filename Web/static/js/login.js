function login() {
    const username = $('#username').val().trim();
    const password = $('#password').val().trim();

    $.post('/api/auth', {
        username,
        password
    }).then(() => {
        window.location.href = '/notes/';
    });
}