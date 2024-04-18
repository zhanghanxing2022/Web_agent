var selectElement =document.querySelectorAll('select');
var option = []
selectElement.forEach((select)=>{
    let a = [selectChild(select)]
    
    for (child of select.children){
        
        if (child.tagName='OPTION')
        {
            a.push(selectChild(child))

        }
    }
    option.push(a)
    
    
})
return option