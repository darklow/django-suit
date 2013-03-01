/**
 * List sortables
 */
$.fn.suit_list_sortable = function () {
    var previous_value = 0;

    var perform_move = function ($arrow, $row) {
        var level = $row.data('level');
        if ($arrow.data('dir') === 'down') {
            var next = $row.next();
            if (next.length/* && next.data('level') === level*/) {
                $row.insertAfter(next).addClass('selected')
            }
        } else {
            var prev = $row.prev();
            console.info($row);
            if (prev.length/* && prev.data('level') === level*/) {
                $row.insertBefore(prev).addClass('selected')
            }
        }
    }

//    if (perform_move) {
//        $.post($arrow.data('url'))
//            .done(function (data) { data.ok ? perform_move() : window.location.reload() })
//            .fail(function () { alert("Error moving category. Please try again later") });
//    }

    var create_link = function (text, className, direction) {
        var $link = $('<a/>').attr('href', '#').addClass(className).data('dir', direction).text(text);
        $link.click(function (e) {
            var $arrow = $(this);
            $('.selected').removeClass('selected');
            var $row = $arrow.closest('tr');
            perform_move($arrow, $row);
            e.preventDefault();

        });
        return  $link;
    }

    var $inputs = $(this);
    $inputs.each(function () {
        var $input = $(this);
        /*var value = parseInt($input.val()) || 0;
         if (previous_value >= value) {
         value = previous_value + 1
         $input.val(value)
         }
         previous_value = value;*/
//        $input.hide()
        var $up_link = create_link('Up', 'sortable', 'up');
        var $down_link = create_link('Down', 'sortable', 'down');
        var $link_div = $input.parent().append($('<div class="inline-sortable"/>'));
        $link_div.append($up_link);
        $link_div.append($down_link);
    });

    // Update input count right before submit
    if ($inputs && $inputs.length) {
        var $first_input = $inputs.first();
        var fieldset_id = $first_input.attr('name').split('-')[0];
        var selector = $(this).selector;
        var $form = $($first_input[0].form);
        $form.submit(function (e) {
            var i = 0;
            $(selector).each(function () {
                var $input = $(this);
                // Check if any of dynamic block values is added
                var $set_block = $input.closest('.dynamic-' + fieldset_id);
                if ($set_block) {
                    value = '';
                    if ($set_block.find(":input[value!=''][type!='hidden']").serialize()) {
                        value = i++;
                    }
                    $input.val(value);
                }
            });
        })
    }
};


$(function () {

    // List sortables
    $('.suit-sortable').suit_list_sortable();

});
