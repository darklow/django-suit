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
            var $sortable = $(this);
            var $row = $sortable.closest(
                $sortable.hasClass('sortable-stacked') ? 'div.inline-related' : 'tr'
            );
            perform_move($sortable, $row);
            e.preventDefault();
        }

        function create_link(text, direction, on_click_func, is_stacked) {
            return $('<a/>').attr('href', '#')
                .addClass('sortable sortable-' + direction +
                    (is_stacked ? ' sortable-stacked' : ''))
                .attr('data-dir', direction).html(text)
                .click(on_click_func);
        }

        $inputs.each(function () {
            var $inline_sortable = $('<div class="inline-sortable"/>'),
                icon = '<i class="icon-arrow-up icon-alpha5"></i>',
                $sortable = $(this),
                is_stacked = $sortable.hasClass('suit-sortable-stacked');

            var $up_link = create_link(icon, 'up', on_arrow_click, is_stacked),
                $down_link = create_link(icon.replace('-up', '-down'), 'down', on_arrow_click, is_stacked);

            if (is_stacked) {
                var $sortable_row = $sortable.closest('div.form-row'),
                    $stacked_block = $sortable.closest('div.inline-related'),
                    $links_span = $('<span/>').attr('class', 'stacked-inline-sortable');

                // Add arrows to header h3, move order input and remove order field row
                $links_span.append($up_link).append($down_link);
                $stacked_block.find('h3').append($links_span);
                $stacked_block.append($sortable);
                $sortable_row.remove();
            } else {
                $sortable.parent().append($inline_sortable);
                $inline_sortable.append($up_link);
                $inline_sortable.append($down_link);
            }

        });

        // Filters out unchanged checkboxes, selects and sortable field itself
        function filter_unchanged(i, input) {
            if (input.type == 'checkbox') {
                if (input.defaultChecked == input.checked) {
                    return false;
                }
            } else if (input.type == 'select-one' || input.type == 'select-multiple') {
                var options = input.options, option;
                for (var j = 0; j < options.length; j++) {
                    option = options[j];
                    if (option.selected && option.selected == option.defaultSelected) {
                        return false;
                    }
                }
            } else if ($(input).hasClass('suit-sortable')) {
                if (input.defaultValue == input.value && input.value == 0) {
                    return false;
                }
            }
            return true;
        }

        // Update input count right before submit
        if ($inputs && $inputs.length) {
            var $last_input = $inputs.last();
            var selector = $(this).selector;
            $($last_input[0].form).submit(function (e) {
                var i = 0, value;
                $(selector).each(function () {
                    var $input = $(this);
                    var fieldset_id = $input.attr('name').split(/-\d+-/)[0];
                    // Check if any of new dynamic block values has been added
                    var $set_block = $input.closest('.dynamic-' + fieldset_id);
                    var $changed_fields = $set_block.find(":input[value!=''][type!='hidden']").filter(filter_unchanged);
                    if (!$set_block.length
                        || $set_block.hasClass('has_original')
                        || $changed_fields.serialize()
                        // Since jQuery serialize() doesn't include type=file do additional check
                        || $changed_fields.find(":input[type='file']").addBack().length) {
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
