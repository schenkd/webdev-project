$(document).ready(function() {
    // fix menu when passed
    $('.masthead').visibility({
        once: false,
        onBottomPassed: function() {
            $('.fixed.menu').transition('fade in');
            },
        onBottomPassedReverse: function() {
            $('.fixed.menu').transition('fade out');
            // create sidebar and attach to menu open
            $('.ui.sidebar').sidebar('attach events', '.toc.item');

            $('.ui.accordion').accordion();

            var content = [
                { title: 'Andorra' },
                { title: 'United Arab Emirates' },
                { title: 'Afghanistan' },
                { title: 'Antigua' },
                { title: 'Anguilla' },
                { title: 'Albania' },
                { title: 'Armenia' },
                { title: 'Netherlands Antilles' },
                { title: 'Angola' },
                { title: 'Argentina' },
                { title: 'American Samoa' },
                { title: 'Austria' },
                { title: 'Australia' },
                { title: 'Aruba' },
                { title: 'Aland Islands' },
                { title: 'Azerbaijan' },
                { title: 'Bosnia' },
                { title: 'Barbados' },
                { title: 'Bangladesh' },
                { title: 'Belgium' },
                { title: 'Burkina Faso' },
                { title: 'Bulgaria' },
                { title: 'Bahrain' },
                { title: 'Burundi' }
                // etc
            ];

            $('.ui.search').search({source: content});
              }
    });

    // create sidebar and attach to menu open
    $('.ui.search').search({source: content});

    $('.ui.sidebar').sidebar('attach events', '.toc.item');

    $('.ui.accordion').accordion();


});
var content = [
    { title: 'Andorra' },
    { title: 'United Arab Emirates' },
    { title: 'Afghanistan' },
    { title: 'Antigua' },
    { title: 'Anguilla' },
    { title: 'Albania' },
    { title: 'Armenia' },
    { title: 'Netherlands Antilles' },
    { title: 'Angola' },
    { title: 'Argentina' },
    { title: 'American Samoa' },
    { title: 'Austria' },
    { title: 'Australia' },
    { title: 'Aruba' },
    { title: 'Aland Islands' },
    { title: 'Azerbaijan' },
    { title: 'Bosnia' },
    { title: 'Barbados' },
    { title: 'Bangladesh' },
    { title: 'Belgium' },
    { title: 'Burkina Faso' },
    { title: 'Bulgaria' },
    { title: 'Bahrain' },
    { title: 'Burundi' }
    // etc
];
