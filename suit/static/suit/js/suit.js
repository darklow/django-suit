Suit = {};
window.Suit = Suit;

(function ($) {
    if (!$)
        return;

    Suit.$ = $;

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

    Suit.ListActionsToggle = function () {
        var $topActions;

        var init = function () {
            $(document).ready(function () {
                $topActions = $('.results').parent().find('.actions').eq(0);
                if (!$topActions.length)
                    return;

                $("tr input.action-select, #action-toggle").on('click', checkIfSelected);
            });
        };

        var checkIfSelected = function () {
            if ($('tr.selected').length) {
                $topActions.slideDown('fast');
            } else {
                $topActions.slideUp('fast');
            }
        };

        return {
            init: init
        }

    }();


    Suit.FixedBar = function () {
        var didScroll = false, $fixedItem, $fixedItemParent, $win, $body,
            itemOffset,
            extraOffset = 0,
            fixed = false;

        function init(selector) {
            $fixedItem = $(selector || '.submit-row');
            if (!$fixedItem.length)
                return;

            $fixedItemParent = $fixedItem.parents('form');
            itemOffset = $fixedItem.offset();
            $win = $(window);
            window.onscroll = onScroll;
            window.onresize = onScroll;
            onScroll();

            setInterval(function () {
                if (didScroll) {
                    didScroll = false;
                }
            }, 200);
        }

        function onScroll() {
            didScroll = true;

            var itemHeight = $fixedItem.height(),
                scrollTop = $win.scrollTop();

            if (scrollTop + $win.height() - itemHeight - extraOffset < itemOffset.top) {
                if (!fixed) {
                    $fixedItem.addClass('fixed');
                    $fixedItemParent.addClass('fixed').css('padding-bottom', itemHeight + 'px');
                    fixed = true;
                }
            } else {
                if (fixed) {
                    $fixedItem.removeClass('fixed');
                    $fixedItemParent.removeClass('fixed').css('padding-bottom', '');
                    fixed = false;
                }
            }
        }

        return {
            init: init
        };
    }();

    /**
     * Avoids double-submit issues in the change_form.
     */
    $.fn.suitFormDebounce = function () {
        var $form = $(this),
            $saveButtons = $form.find('.submit-row button, .submit-row input[type=button], .submit-row input[type=submit]'),
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

    /**
     * Content tabs
     */
    $.fn.suitFormTabs = function () {

        var $tabs = $(this);
        var tabPrefix = $tabs.data('tab-prefix');
        if (!tabPrefix)
            return;

        var $tabLinks = $tabs.find('a');

        function tabContents($link) {
            return $('.' + tabPrefix + '-' + $link.attr('href').replace('#', ''));
        }

        function activateTabs() {
            // Init tab by error, by url hash or init first tab
            if (window.location.hash) {
                var foundError;
                $tabLinks.each(function () {
                    var $link = $(this);
                    if (tabContents($link).find('.error, .errorlist').length != 0) {
                        $link.addClass('has-error');
                        $link.trigger('click');
                        foundError = true;
                    }
                });
                !foundError && $($tabs).find('a[href=\\' + window.location.hash + ']').click();
            } else {
                $tabLinks.first().trigger('click');
            }
        }

        $tabLinks.click(function () {
            var $link = $(this),
                showEvent = $.Event('shown.suit.tab', {
                    relatedTarget: $link,
                    tab: $link.attr('href').replace('#', '')
                });
            $link.parent().parent().find('.active').removeClass('active');
            $link.addClass('active');
            $('.' + tabPrefix).removeClass('show').addClass('hidden-xs-up');
            tabContents($link).removeClass('hidden-xs-up').addClass('show');
            $link.trigger(showEvent);
        });

        activateTabs();
    };

    /* Characters count for CharacterCountTextarea */
    $.fn.suitCharactersCount = function () {
        var $elements = $(this);

        if (!$elements.length)
            return;

        $elements.each(function () {
            var $el = $(this),
                $countEl = $('<div class="suit-char-count"></div>');
            $el.after($countEl);
            $el.on('keyup', function (e) {
                updateCount($(e.currentTarget));
            });
            updateCount($el);
        });

        function updateCount($el) {
            var maxCount = $el.data('suit-maxcount'),
                twitterCount = $el.data('suit-twitter-count'),
                value = $el.val(),
                len = twitterCount ? getTweetLength(value) : value.length,
                count = maxCount ? maxCount - len : len;
            if (count < 0)
                count = '<span class="text-danger">' + count + '</span>';

            $el.next().first().html(count);
        }

        function getTweetLength(input) {
            var tmp = "";
            for (var i = 0; i < 23; i++) {
                tmp += "o"
            }
            return input.replace(/(http:\/\/[\S]*)/g, tmp).length;
        }
    };

    /**
     * Search filters - submit only changed fields
     */
    $.fn.suitSearchFilters = function () {
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
            console.log($field, additional)
            if (additional) {
                var hiddenId = $field.data('name') + '_add';
                var $hidden = $('#' + hiddenId);
                if (!$hidden.length) {
                    $hidden = $('<input/>').attr('type', 'hidden').attr('id', hiddenId);
                    $field.after($hidden);
                }
                additional = additional.split('=');
                $hidden.attr('name', additional[0]).val(additional[1])
            }
        });
        $(this).trigger('change');
    };


})(typeof django !== 'undefined' ? django.jQuery : undefined);
