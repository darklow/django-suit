var django = django || {};
django.jQuery = jQuery.noConflict(true);

// Override Django jquery.init.js
// Make jQuery global - needed for Django-Select2
if (!window.jQuery)
    window.$ = window.jQuery = django.jQuery;

