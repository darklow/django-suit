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

/**
 * Linked select - shows link to related item after Select
 */
$.fn.linked_select = function () {

    var get_link_name = function ($select) {
        var text = $select.find('option:selected').text();
        return text && $select.val() ? text + '' : '';
    };

    var get_url = function ($add_link, $select) {
        var value = $select.val();
        return $add_link.attr('href') + '../' + value + '/';
    };

    var add_link = function ($select) {
        var $add_link = $select.next();
        if ($add_link.hasClass('add-another')) {
            var $link = $add_link.next();
            if (!$link.length) {
                $link = $('<a/>').addClass('f11');
                $add_link.after($link).after(' &nbsp; ');
            }
            $link.text(get_link_name($select));
            $link.attr('href', get_url($add_link, $select));
        }
    };

    $(this).each(function () {
        add_link($(this));
    });

    $(document).on('change', this.selector, function () {
        add_link($(this));
    });
};

$(function () {

    // Fixed submit buttons
    $('.inner-right-column').fixed();

    // Show link to related item after Select
    $('.linked-select').linked_select();

    // Handle change list filter null values
    $('.search-filter').search_filters();

});
