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

})(typeof django !== 'undefined' ? django.jQuery : undefined);
