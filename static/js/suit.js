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

        var $fixed_item = $(this), pos = $fixed_item.offset();

        $(window).bind('scroll.sl resize.sl load.sl', function (e) {
            if ($(this).scrollTop() > (pos.top - 10) &&
                $fixed_item.css('position') == 'static') {
                $fixed_item.addClass('fixed');
            }
            else if ($(this).scrollTop() <= (pos.top - 10) &&
                $fixed_item.hasClass('fixed')) {
                $fixed_item.removeClass('fixed');
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

//    LeftNavigation && LeftNavigation.init();

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
