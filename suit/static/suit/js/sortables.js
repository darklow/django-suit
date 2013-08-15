/**
 * List sortables
 */
(function ($) {
    $.fn.suit_list_sortable = function () {
        var $inputs = $(this);
        if (!$inputs.length)
            return;

        // Detect if this is normal or mptt table
        var mptt_table = $inputs.first().closest('table').hasClass('table-mptt');

        function perform_move($arrow, $row) {
            var $next, $prev;
            if (mptt_table) {
                function get_padding($tr) {
                    return parseInt($tr.find('th:first').css('padding-left'));
                }

                function find_with_children($tr) {
                    var padding = get_padding($tr);
                    return $tr.nextUntil(function () {
                        return get_padding($(this)) <= padding
                    }).andSelf();
                }

                $('.selected').removeClass('selected');
                var padding = get_padding($row);
                var $rows_to_move = find_with_children($row);
                if ($arrow.data('dir') === 'down') {
                    $next = $rows_to_move.last().next();
                    if ($next.length && get_padding($next) === padding) {
                        var $after = find_with_children($next).last();
                        if ($after.length) {
                            $rows_to_move.insertAfter($after).addClass('selected');
                        }
                    }
                } else {
                    $prev = $row.prevUntil(function () {
                        return get_padding($(this)) <= padding
                    }).andSelf().first().prev();
                    if ($prev.length && get_padding($prev) === padding) {
                        $rows_to_move.insertBefore($prev).addClass('selected')
                    }
                }
            } else {
                $('.selected').removeClass('selected');
                if ($arrow.data('dir') === 'down') {
                    $next = $row.next();
                    if ($next.is(':visible') && $next.length) {
                        $row.insertAfter($next).addClass('selected')
                    }
                } else {
                    $prev = $row.prev();
                    if ($prev.is(':visible') && $prev.length) {
                        $row.insertBefore($prev).addClass('selected')
                    }
                }
            }
        }

        function on_arrow_click(e) {
            perform_move($(this), $(this).closest('tr'));
            e.preventDefault();
        }

        function create_link(text, direction) {
            return $('<a/>').attr('href', '#')
                .addClass('sortable sortable-' + direction)
                .attr('data-dir', direction).html(text)
                .click(on_arrow_click);
        }

        $inputs.each(function () {
            var $inline_sortable = $('<div class="inline-sortable"/>');
            var icon = '<i class="icon-arrow-up icon-alpha5"></i>';
            $(this).parent().append($inline_sortable);
            $inline_sortable.append(create_link(icon, 'up'));
            $inline_sortable.append(create_link(icon.replace('-up', '-down'), 'down'));
        });

        // Filters out unchanged selects and sortable field itself
        function filter_unchanged(i, input) {
            if (input.type == 'select-one' || input.type == 'select-multiple') {
                for (var j = 0; j < input.options.length; j++) {
                    if (input.options[j].selected == input.options[j].defaultSelected) {
                        return false;
                    }
                }
            }else if($(input).hasClass('suit-sortable')){
                return false;
            }
            return true;
        }

        // Update input count right before submit
        if ($inputs && $inputs.length) {
            var $last_input = $inputs.last();
            var selector = $(this).selector;
            $($last_input[0].form).submit(function (e) {
                var i = 0;
                $(selector).each(function () {
                    var $input = $(this);
                    var fieldset_id = $input.attr('name').split('-')[0];
                    // Check if any of new dynamic block values has been added
                    var $set_block = $input.closest('.dynamic-' + fieldset_id);
                    if (!$set_block.length || $set_block.find(":input[value!=''][type!='hidden']").filter(filter_unchanged).serialize()) {
                        value = i++;
                        $input.val(value);
                    }
                });
            });
        }

        Suit.after_inline.register('bind_sortable_arrows', function (prefix, row) {
            $(row).find('.sortable').click(on_arrow_click);
        })
    };


    $(function () {
        $('.suit-sortable').suit_list_sortable();
    });

}(Suit.$));
