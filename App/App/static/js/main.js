const flash = document.querySelector("#flash")
const allitems = document.querySelectorAll('body')

function remove_items(){
    if (flash.hasChildNodes()) {
        flash.removeChild(flash.firstChild)
    }
}

setTimeout(remove_items, 5000)

allitems.forEach(element => {  
    element.addEventListener("click", remove_items)
}); 

