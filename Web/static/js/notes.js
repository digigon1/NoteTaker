$(document).ready(function(){
    M.Modal.init($('.modal'));
});

function createNote() {
    const title = $('#title').val().trim();
    $.ajax({
        url: '/api/notes/',
        type: 'PUT',
        data: {
            title
        }
    }).then(res => {
        window.location.href = '/notes/' + res;
    })
}

function deleteConfirm(id) {
    $('#confirm-delete').click(() => {
        deleteNote(id);
    });
    M.Modal.getInstance($('#modal-delete')).open();
}

function deleteNote(id) {
    $.ajax({
        url: `/api/notes/${id}`,
        type: "DELETE"
    }).then(() => {
        window.location.href = '/notes/';
    });
}

function updateNote() {
    const split_url = window.location.href.split('#')[0].split('/');
    const id = split_url[split_url.length - 1];
    
    const title = $('#title').val();
    const content = $('#content').val();

    $.post(`/api/notes/${id}`, {
        title,
        content
    }).then(() => {
        window.location.href = `/notes/${id}`;
    });
}