$(function () {
    // Add AJAX loader
    $('.plugin-list .text').click(function(){
        var $target = $(this).parent().parent().parent().parent().children("div.plugin-editor");
        var $icon = $('<i/>').attr('id','suit-loading-icon');
        $icon.css({'display': 'inline-block', 'top': -25, 'left': 15, 'position': 'absolute'});
        $target.prepend($icon)

    });
});
