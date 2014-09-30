(function ($) {

    // Register callbacks to perform after inline has been added
    Suit.after_inline = function () {
        var functions = {};
        var register = function (fn_name, fn_callback) {
            functions[fn_name] = fn_callback;
        };

        var run = function (inline_prefix, row) {
            for (var fn_name in functions) {
                functions[fn_name](inline_prefix, row);
            }
        };

        return {
            register: register,
            run: run
        };
    }();

    // Backwards compatiblity
    SuitAfterInline = Suit.after_inline;

    /**
     * Fixed submit buttons.
     */
    $.fn.suit_fixed = function () {
        $(this).each(function () {
            // extra_offset: 70 (60 Footer height + 10 top offset)
            var $fixed_item = $(this),
                item_pos = $fixed_item.offset(),
                extra_offset = 50;
            $(window).bind('scroll.sl resize.sl load.sl', function (e) {
                var $win = $(this),
                    item_height = $fixed_item.height(),
                    scroll_top = $win.scrollTop()
                ;
                if (scroll_top + $win.height() - item_height - extra_offset < item_pos.top) {
                    if (!$fixed_item.hasClass('fixed')) {
                        $fixed_item.addClass('fixed');
                    }
                } else {
                    $fixed_item.removeClass('fixed');
                }
            });

            $(window).trigger('scroll.sl');
        });
    };


    /**
     * Search filters - submit only changed fields
     */
    $.fn.suit_search_filters = function () {
        $(this).change(function () {
            var $field = $(this);
            var $option = $field.find('option:selected');
            var select_name = $option.data('name');
            if (select_name) {
                $field.attr('name', select_name);
            } else {
                $field.removeAttr('name');
            }
            // Handle additional values for date filters
            var additional = $option.data('additional');
            if (additional) {
                var hidden_id = $field.data('name') + '_add';
                var $hidden = $('#' + hidden_id);
                if (!$hidden.length) {
                    $hidden = $('<input/>').attr('type', 'hidden').attr('id', hidden_id);
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
    $.fn.suit_linked_select = function () {

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
                var $link = $add_link.next('a');
                if (!$link.length) {
                    $link = $('<a/>').addClass('linked-select-link');
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

    /**
     * Content tabs
     */
    $.fn.suit_form_tabs = function () {

        var $tabs = $(this);
        var tab_prefix = $tabs.data('tab-prefix');
        if (!tab_prefix)
            return;

        var $tab_links = $tabs.find('a');

        function tab_contents($link) {
            return $('.' + tab_prefix + '-' + $link.attr('href').replace('#', ''));
        }

        function activate_tabs() {
            // Init tab by error, by url hash or init first tab
            if (window.location.hash) {
                var found_error;
                $tab_links.each(function () {
                    var $link = $(this);
                    if (tab_contents($link).find('.error').length != 0) {
                        $link.addClass('error');
                        $link.trigger('click');
                        found_error = true;
                    }
                });
                !found_error && $($tabs).find('a[href=' + window.location.hash + ']').click();
            } else {
                $tab_links.first().trigger('click');
            }
        }

        $tab_links.click(function () {
            var $link = $(this);
            $link.parent().parent().find('.active').removeClass('active');
            $link.parent().addClass('active');
            $('.' + tab_prefix).removeClass('show').addClass('hide');
            tab_contents($link).removeClass('hide').addClass('show')
        });

        activate_tabs();
    };

    /**
     * Avoids double-submit issues in the change_form.
     */
    $.fn.suit_form_debounce = function () {
        var $form = $(this),
            $saveButtons = $form.find('.submit-row button'),
            submitting = false;

        $form.submit(function () {
            if (submitting) {
                return false;
            }

            submitting = true;
            $saveButtons.addClass('disabled');

            setTimeout(function () {
                $saveButtons.removeClass('disabled');
                submitting = false;
            }, 5000);
        });
    };

    $(function () {

        // Fixed submit buttons
        $('.submit-row').suit_fixed();

        // Show link to related item after Select
        $('.linked-select').suit_linked_select();

        // Handle change list filter null values
        $('.search-filter').suit_search_filters();

        // Menu toggle
        $("#menu-toggle").click(function (e) {
            e.preventDefault();
            $("#wrapper").toggleClass("toggled");
        });

    });

}(Suit.$));
