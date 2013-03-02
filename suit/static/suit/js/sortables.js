/**
 * List sortables
 */
$.fn.suit_list_sortable = function () {

    var $inputs = $(this);
    if (!$inputs.length)
        return;

    var perform_move = function ($arrow, $row) {
        if ($arrow.data('dir') == 'down') {
            var $next = $row.next();
            if ($next.is(':visible') && $next.length) {
                $('.selected').removeClass('selected');
                $row.insertAfter($next).addClass('selected')
            }
        } else {
            var $prev = $row.prev();
            if ($prev.is(':visible') && $prev.length) {
                $('.selected').removeClass('selected');
                $row.insertBefore($prev).addClass('selected')
            }
        }
    };

    var on_arrow_click = function (e) {
        perform_move($(this), $(this).closest('tr'));
        e.preventDefault();
    };

    var create_link = function (text, direction) {
        return $('<a/>').attr('href', '#')
            .addClass('sortable sortable-' + direction)
            .attr('data-dir', direction).html(text)
            .click(on_arrow_click);
    };
    $inputs.each(function () {
        var $inline_sortable = $('<div class="inline-sortable"/>');
        var icon = '<i class="icon-arrow-up icon-alpha5"></i>';
        $(this).parent().append($inline_sortable);
        $inline_sortable.append(create_link(icon, 'up'));
        $inline_sortable.append(create_link(icon.replace('-up', '-down'), 'down'));
    });

    // Update input count right before submit
    if ($inputs && $inputs.length) {
        var $last_input = $inputs.last();
        var selector = $(this).selector;
        $($last_input[0].form).submit(function (e) {
            var i = 0;
            var fieldset_id = $last_input.attr('name').split('-')[0];
            $(selector).each(function () {
                var $input = $(this);
                // Check if any of new dynamic block values has been added
                var $set_block = $input.closest('.dynamic-' + fieldset_id);
                if (!$set_block.length || $set_block.find(":input[value!=''][type!='hidden']").serialize()) {
                    value = i++;
                    $input.val(value);
                }
            });
        });
    }

    var afterInlineAdd = function (prefix, row) {
        $(row).find('.sortable').click(on_arrow_click);
    };
    SuitAfterInline.register('bind_sortable_arrows', afterInlineAdd)
};


$(function () {

    // List sortables
    $('.suit-sortable').suit_list_sortable();

});
