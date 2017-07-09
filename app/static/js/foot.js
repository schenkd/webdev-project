$('select.dropdown').dropdown();

function getFilter(msg) {
    $.ajax({
        url: '/_getFilter',
        type: 'POST',
        data: JSON.stringify(msg),
        datatype: 'json',
    }).done(function (reply) {
        $('#table').html(reply);
    });
};
