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

        function performMove($arrow, $row) {
            var $next, $prev;

            $row.closest('table').find('tr.selected').removeClass('selected');
            if (mptt_table) {
                function getPadding($tr) {
                    return parseInt($tr.find('th:first').css('padding-left'));
                }

                function findWithChildren($tr) {
                    var padding = getPadding($tr);
                    return $tr.nextUntil(function () {
                        return getPadding($(this)) <= padding
                    }).andSelf();
                }

                var padding = getPadding($row);
                var $rows_to_move = findWithChildren($row);
                if ($arrow.data('dir') === 'down') {
                    $next = $rows_to_move.last().next();
                    if ($next.length && getPadding($next) === padding) {
                        var $after = findWithChildren($next).last();
                        if ($after.length) {
                            $rows_to_move.insertAfter($after).addClass('selected');
                        }
                    }
                } else {
                    $prev = $row.prevUntil(function () {
                        return getPadding($(this)) <= padding
                    }).andSelf().first().prev();
                    if ($prev.length && getPadding($prev) === padding) {
                        $rows_to_move.insertBefore($prev).addClass('selected')
                    }
                }
            } else {
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
            markLastInline($row.parent());
        }

        function onArrowClick(e) {
            var $sortable = $(this);
            var $row = $sortable.closest(
                $sortable.hasClass('sortable-stacked') ? 'div.inline-related' : 'tr'
            );
            performMove($sortable, $row);
            e.preventDefault();
        }

        function createLink(text, direction, on_click_func, is_stacked) {
            return $('<a/>').attr('href', '#')
                .addClass('sortable sortable-' + direction +
                    (is_stacked ? ' sortable-stacked' : ''))
                .attr('data-dir', direction).html(text)
                .on('click', on_click_func);
        }

        function markLastInline($rowParent) {
            $rowParent.find(' > .last-sortable').removeClass('last-sortable');
            $rowParent.find('tr.form-row:visible:last').addClass('last-sortable');
        }

        var $lastSortable;
        $inputs.each(function () {
            var $inline_sortable = $('<div class="inline-sortable"/>'),
                icon = '<span class="fa fa-lg fa-arrow-up"></span>',
                $sortable = $(this),
                is_stacked = $sortable.hasClass('suit-sortable-stacked');

            var $up_link = createLink(icon, 'up', onArrowClick, is_stacked),
                $down_link = createLink(icon.replace('-up', '-down'), 'down', onArrowClick, is_stacked);

            if (is_stacked) {
                var $sortable_row = $sortable.closest('div.form-group'),
                    $stacked_block = $sortable.closest('div.inline-related'),
                    $links_span = $('<span/>').attr('class', 'stacked-inline-sortable');

                // Add arrows to header h3, move order input and remove order field row
                $links_span.append($up_link).append($down_link);
                $links_span.insertAfter($stacked_block.find('.inline_label'));
                $stacked_block.append($sortable);
                $sortable_row.remove();
            } else {
                $sortable.parent().append($inline_sortable);
                $inline_sortable.append($up_link);
                $inline_sortable.append($down_link);
                $lastSortable = $sortable;
            }
        });

        $lastSortable && markLastInline($lastSortable.closest('.form-row').parent());

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
                // e.preventDefault();
                $(selector).each(function () {
                    var $input = $(this);
                    var fieldset_id = $input.attr('name').split(/-\d+-/)[0];
                    // Check if any of new dynamic block values has been added
                    var $set_block = $input.closest('.dynamic-' + fieldset_id);
                    var $changed_fields = $set_block.find(":input[type!='hidden']:not(.suit-sortable)").filter(
                        function () {
                            return $(this).val() != "";
                        }).filter(filter_unchanged);
                    // console.log($changed_fields.length, $changed_fields);
                    var is_changelist = !$set_block.length;
                    if (is_changelist
                        || $set_block.hasClass('has_original')
                        || $changed_fields.serializeArray().length
                            // Since jQuery serialize() doesn't include type=file do additional check
                        || $changed_fields.find(":input[type='file']").addBack().length) {
                        value = i++;
                        $input.val(value);
                    }
                });
            });
        }

        Suit.after_inline.register('bind_sortable_arrows', function (prefix, row) {
            $(row).find('.suit-sortable').on('click', onArrowClick);
            markLastInline($(row).parent());
        });
    };


    $(function () {
        $('.suit-sortable').suit_list_sortable();
    });

}(django.jQuery));

// Call Suit.after_inline
django.jQuery(document).on('formset:added', function (e, row, prefix) {
    Suit.after_inline.run(prefix, row);
});
