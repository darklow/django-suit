var LeftNavigation = (function ($navigation) {

    if (!$navigation.length) return;

    function init() {
        var self = this;

        // Navigation switcher
        var $liActive = $navigation.find('li.active');
        $navigation.find('ul > li > a').click(function (e) {
            var $li = $(this).parent();
            var $link = $(this);
            if ($link.attr('href').indexOf('#') != -1) {
//                var isActive = $li.hasClass('active');
//                $li.parent().find('.active').removeClass('active');
//                if (!isActive)
//                    $li.addClass('active');
//                else
//                    $liActive.addClass('active');

                $link.attr('href', $li.find('ul li:first a').first().attr('href'));
                $link.click();
//                e.preventDefault();
            }

        });

        // Active nav if no active found
        if (!$('#left-nav li.active').length) {
            $('#left-nav a').each(function () {
                $link = $(this);
                if (document.location.pathname.indexOf($link.attr('href')) == 0) {
                    var $main_li = $link.parent();
                    $main_li.addClass('active');
                    $link.parent().parent().parent().addClass('active');
                    if (!$main_li.find('ul').length) {
                        return false;
                    }
                }
            });
        }
    }

    return {
        init: init
    }

})($('#left-nav'));

var Select2Utils = (function () {

    function width(element) {
        var $element = $(element);
        var width = $element.outerWidth();
        width += parseInt($element.css("padding-left").replace('px', ''));
        width += parseInt($element.css("padding-right").replace('px', ''));
        return width + 2 + 'px';
    }

    return {
        width: width
    }

});

var DatePicker = (function () {

    var lang = document.documentElement.getAttribute('lang');

    function update() {
        var selector = arguments[0];
        $(selector ? selector : '.datepicker').datepicker({
            format: 'dd.mm.yyyy',
            weekStart: 1,
            autoclose: true,
            todayBtn: 'linked',
            todayHighlight: true,
            language: lang
        });
    }

    return {
        update: update
    }
})();

/**
 * Fixed submit buttons.
 */
$.fn.fixed = function () {
    $(this).each(function () {

        var fixadent = $(this), pos = fixadent.offset();

        $(window).bind('scroll.sl resize.sl load.sl', function (e) {
            if ($(this).scrollTop() > (pos.top - 10) &&
                fixadent.css('position') == 'static') {
                fixadent.addClass('fixed');
            }
            else if ($(this).scrollTop() <= (pos.top - 10) &&
                fixadent.hasClass('fixed')) {
                fixadent.removeClass('fixed');
            }
        });

        $(window).trigger('scroll.sl');
    });
};


/**
 * Search filters - submit only changed fields
 */
$.fn.search_filters = function () {
    $(this).change(function () {
        $field = $(this);
        if (!$field.val()) {
            $field.data('name', $field.attr('name'));
            $field.attr('name', '')
        } else if (!$field.attr('name')) {
            $field.attr('name', $field.data('name'));
        }
    });
    $(this).trigger('change');
};

$(function () {

    LeftNavigation && LeftNavigation.init();

    $('.inner-right-column').fixed();

    if ((jQuery().select2)) {
        $('.select2').select2({
            // width: 'element'
            width: function () {
                var $element = $(this.element);
                var width = $element.outerWidth();
                width += parseInt($element.css("padding-left").replace('px', ''));
                width += parseInt($element.css("padding-right").replace('px', ''));
                return width + 2 + 'px';
            }
        });
    }

    // Handle filter absolute null values
    $('.search-filter').search_filters();

});
