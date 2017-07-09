$(document).ready(function() {
    // fix menu when passed
    $('.masthead').visibility({
        once: false,
        onBottomPassed: function() {
            $('.fixed.menu').transition('fade in');
            },
        onBottomPassedReverse: function() {
            $('.fixed.menu').transition('fade out');

            $('.ui.sidebar').sidebar(
                'attach events',
                '.toc.item'
            );

            $('.ui.accordion').accordion();
        }
    });

    $('.ui.search').search({
        source: content
    });

    $('.ui.sidebar').sidebar(
        'attach events',
        '.toc.item'
    );

    $('.ui.accordion').accordion();

});