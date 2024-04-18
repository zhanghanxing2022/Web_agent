
function isInputElement(element) {
    return window.getComputedStyle(element).getPropertyValue('cursor') === 'text' ;
}


var allElements = document.querySelectorAll('*');
var inputElements = [];

allElements.forEach(function(element) {
    if (isInputElement(element)) {
        inputElements.push(selectChild(element));
    }
});

return inputElements;