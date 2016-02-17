Suit = {};
window.Suit = Suit;

(function ($) {
    if (!$)
        return;

    Suit.ListActionsToggle = function () {
        var $topActions;

        var init = function () {
            $(document).ready(function () {
                $topActions = $('.results').prev('.actions');
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
                    $fixedItemParent.addClass('fixed').css('padding-bottom', itemHeight+'px');
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

})(typeof django !== 'undefined' ? django.jQuery : undefined);
