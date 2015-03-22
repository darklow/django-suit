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
            var $fixed_item = $(this), pos = $fixed_item.offset(), extra_offset = 70;
            $(window).bind('scroll.sl resize.sl load.sl', function (e) {
                var $win = $(this), scroll_top = $win.scrollTop();
                if ($fixed_item.height() < $win.height() &&
                    scroll_top > (pos.top - 10) &&
                    $fixed_item.height() < $win.height()) {
                    !$fixed_item.hasClass('fixed') && $fixed_item.addClass('fixed');
                    var max_top = Math.min(10, $(document).height() - $fixed_item.height() - scroll_top - extra_offset);
                    $fixed_item.css('top', max_top + 'px');
                }
                else if (scroll_top <= (pos.top - 10) &&
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
            return $add_link.attr('href').split('?')[0] + '../' + value + '/';
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
        $('.inner-right-column').suit_fixed();

        // Show link to related item after Select
        $('.linked-select').suit_linked_select();

        // Handle change list filter null values
        $('.search-filter').suit_search_filters();

    });

}(Suit.$));

/**
 * Add a button for toggling which columns to display
 */
(function ($) {
    function create_cookie_for_page(name, value, days) {
        var expires, date;
        date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toGMTString();
        document.cookie = encodeURI(name) + "=" + encodeURI(value) + expires + "; path=" + window.location.pathname;
    }

    function read_cookie(name) {
        var nameEQ = encodeURI(name) + "=",
            ca = document.cookie.split(';'),
            c, i;
        for (i = 0; i < ca.length; i++) {
            c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1, c.length);
            }
            if (c.indexOf(nameEQ) == 0) {
                return decodeURI(c.substring(nameEQ.length, c.length));
            }
        }
        return null;
    }

    $(function () {
        var result_list = $('#result_list'),
            toggle_column_wrapper,
            dropdown_menu,
            column_headers,
            toggle_columns_init_cookie,
            default_columns,
            visible_columns;
        if (result_list && document.getElementsByClassName('columns-togglable').length === 1) {
            column_headers = result_list.find('thead th:not(.action-checkbox-column, .__unicode__-column)');
            if (column_headers.length) {
                // Create the toggle column drop down
                result_list.addClass('table-toggle-columns');
                toggle_column_wrapper = $('<div class="toggle-column-wrapper dropdown"><a href="#"></a><ul ' +
                    'class="dropdown-menu pull-right" role="menu" aria-labelledby="dLabel"></ul></div>');
                toggle_column_wrapper.insertBefore(result_list);
                dropdown_menu = toggle_column_wrapper.children('.dropdown-menu');
                column_headers.each(function (index, el) {
                    var $el = $(el),
                        el_text = $el.find('.text a, span').text();
                    dropdown_menu.append($('<li><a tabindex="-1" href="#" data-toggle-text="' + el_text +
                        '"><i class="icon-ok"></i>' + el_text + '</a></li>'));
                });
                toggle_columns_init_cookie = read_cookie('toggle-columns');
                default_columns = document.getElementById('default-column-data-list');
                visible_columns = [];
                // visible_columns comes from the cookie, then the default columns, then an empty array
                if (toggle_columns_init_cookie) {
                    visible_columns = JSON.parse(toggle_columns_init_cookie);
                    if (!$.isArray(visible_columns)) {
                        visible_columns = [];
                    }
                } else if (default_columns !== null) {
                    $.each(default_columns.children, function (i, el) {
                        var column = el.getAttribute('data-default-column');
                        if (column) {
                            visible_columns.push(column);
                        }
                    });
                    default_columns.parentNode.removeChild(default_columns);
                }
                if (visible_columns.length < column_headers.length) {
                    // Hide the columns not in visible_column
                    $.each(column_headers, function (i, el) {
                        var $el = $(el),
                            text = $.trim($el.find('div.text').text()),
                            header,
                            columns;
                        if ($.inArray(text, visible_columns) === -1) {
                            columns = result_list.find('tr > *:nth-child(' + ($el.index() + 1) + ')');
                            columns.toggle();
                            $(dropdown_menu.find('a[data-toggle-text="' + text +
                                '"] i')).toggleClass('icon-ok icon-remove');
                            column_headers.filter(':visible').removeClass('last_visible').last().addClass('last_visible');
                            header = $(columns[0]).filter(':hidden');
                            if (header.hasClass('sorted')) {
                                window.location = header.find('.sortremove').attr('href');
                            }
                        }
                    });
                }
                column_headers.filter(':visible').last().addClass('last_visible');
                dropdown_menu.on('click', 'li a', function () {
                    // Show/hide column on column toggle, and update the cookie
                    var $this = $(this),
                        toggle_text,
                        index,
                        columns,
                        header;
                    $this.find('i').toggleClass('icon-ok icon-remove');
                    toggle_text = $this.data('toggle-text');
                    index = 1 + result_list.find('tr div.text:contains(' + toggle_text + ')').filter(function () {
                        return $.trim($(this).text()) === toggle_text;
                    }).parent().index();
                    columns = result_list.find('tr > *:nth-child(' + index + ')');
                    columns.toggle();
                    column_headers.filter(':visible').removeClass('last_visible').last().addClass('last_visible');
                    create_cookie_for_page(
                        'toggle-columns',
                        JSON.stringify(column_headers.filter(':visible').find('div.text').map(function (i, el) {
                            return $.trim($(el).text());
                        }).get()),
                        3650
                    );
                    header = $(columns[0]).filter(':hidden');
                    if (header.hasClass('sorted')) {
                        window.location = header.find('.sortremove').attr('href');
                    }
                });
                toggle_column_wrapper.children('a').dropdown();
            }
        }
    });
}(Suit.$));
