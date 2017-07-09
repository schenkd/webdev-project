$('select.dropdown').dropdown();

function getFilter(msg) {
    return $.ajax({
        url: '/_getFilter',
        type: 'POST',
        data: JSON.stringify(msg),
        datatype: 'json'
    });
};
