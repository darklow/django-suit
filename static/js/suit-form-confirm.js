/**
 * Determines if a form is dirty by comparing the current value of each element
 * with its default value.
 *
 * @param {Form} form the form to be checked.
 * @return {Boolean} <code>true</code> if the form is dirty, <code>false</code>
 *                   otherwise.
 *
 * Taken from here: http://stackoverflow.com/a/155812/641263
 */

var confirmExitIfModified = (function () {

    function formIsDirty(form) {
        for (var i = 0; i < form.elements.length; i++) {
            var element = form.elements[i];
            var type = element.type;
            if (type == "checkbox" || type == "radio") {
                if (element.checked != element.defaultChecked) {
                    return true;
                }
            }
            else if (type == "hidden" || type == "password" ||
                type == "text" || type == "textarea") {
                if (element.value != element.defaultValue &&
                    // Fix for select2 multiple
                    element.getAttribute('class').indexOf('select2') == -1) {
                    return true;
                }
            }
            else if (type == "select-one" || type == "select-multiple") {
                for (var j = 0; j < element.options.length; j++) {
                    if (element.options[j].selected !=
                        element.options[j].defaultSelected) {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    var submit = false;
    return function (form_id, message) {
        var form = document.forms[form_id]
        form.onsubmit = function (e) {
            e = e || window.event;
            submit = true
        };
        window.onbeforeunload = function (e) {
            e = e || window.event;
            if (!submit && formIsDirty(form)) {
                // For IE and Firefox
                if (e) {
                    e.returnValue = message;
                }
                // For Safari
                return message;
            }
        };
    };
})();
