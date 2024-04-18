function isPointerElement(element) {
    if (element.tagName.toLowerCase() === 'select'){
        return false;
    }
    if (element.tagName.toLowerCase() === 'option'){
        return false;
    }
    if (element.tagName.toLowerCase() === 'input' && element.type.toLowerCase() === 'button') {
        return true;
    }
    if (element.tagName.toLowerCase() === 'a' && element.href!= '') {
        return true;
    }
    return window.getComputedStyle(element).getPropertyValue('cursor') === 'pointer';
}


var allElements = document.querySelectorAll('*');
var clickableElements = [];

allElements.forEach(function(element) {
    if (isPointerElement(element) ) {
        clickableElements.push(selectChild(element));
    }
});

return clickableElements;