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
        var $field = $(this);
        var $option = $field.find('option:selected');
        var select_name = $option.data('name');
        $field.attr('name', select_name ? select_name : '')
        // Handle additional values for date filters
        var additional = $option.data('additional');
        if (additional) {
            console.info(additional);
            var hidden_id = $field.data('name') + '_add';
            var $hidden = $('#' + hidden_id);
            if(!$hidden.length){
                $hidden = $('<input/>').attr('type','hidden').attr('id', hidden_id);
                $field.after($hidden);
            }
            additional = additional.split('=');
            $hidden.attr('name', additional[0]).val(additional[1])
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
