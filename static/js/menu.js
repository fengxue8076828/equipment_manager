
window.addEventListener('load',getMenu)

function renderMenu(parent_module,menus){
    let menuHTML=""
    let items=menus.filter(function(menu){
        return menu.fields.parent_module==parent_module
    })
    for (let item of items){
        menuHTML+=renderMenuItem(item)
        menuHTML+=renderMenu(item.pk,menus)
    }
    return menuHTML
}

function renderMenuItem(item){
    let menuItemHTML=''
    if (!item.fields.parent_module){
        menuItemHTML=`
            <div class="menu-item" id="${item.pk}">
                <div class="menu-item-title">
                    <i class="fa-solid fa-file-lines"></i>
                    <h3 class="menu-item-text">${item.fields.name}</h3>
                </div>
                <i class="fa-solid fa-caret-right"></i>
            </div>
        `
    }else {
        menuItemHTML=`
        <div class="menu-item menu-second hide" id="${item.pk}" data-parent="${item.fields.parent_module}">
            <div class="menu-item-title">
                <i class="fa-solid fa-file-lines"></i>
                <h3 class="menu-item-text">${item.fields.name}</h3>
            </div>
            <i class="fa-solid fa-caret-right"></i>
        </div>
    `
    }
    return menuItemHTML
}

function getMenu(){
    const menuContainer=document.getElementById("menu-items")
    let menuHTML=""
    const xhr=new XMLHttpRequest()
    xhr.open('GET',"menu/",true)
    xhr.onload=function(){
        if (this.status===200){
            const responseText=JSON.parse(this.responseText)
            let menuItems=JSON.parse(responseText.menu)
            menuContainer.innerHTML=renderMenu(null,menuItems)
        }
    }
    xhr.send()
}
document.addEventListener('click',function(e){
    if ((e.target.classList.contains("menu-item") && !e.target.dataset.parent) ||
     (e.target.closest(".menu-item") && !e.target.closest(".menu-item").dataset.parent)
     ){
        secondItems=document.querySelectorAll("[data-parent]")
        secondItems.forEach(function(item){
            item.classList.remove("hide")
            if (item.dataset.parent!=(e.target.classList.contains("menu-item")?
            e.target.id:e.target.closest(".menu-item").id)){
                item.classList.add("hide")
            }
        })
    }
})

document.getElementById("photo").addEventListener('click',function(){
    const xhr=new XMLHttpRequest()
    mainContent=document.getElementById("main-content")
    xhr.open('GET','user-profile/',true)
    xhr.onload=function(){
        if (this.status==200){
            const contentText=JSON.parse(this.responseText)
            mainContent.innerHTML=contentText.content
        }
    }
    xhr.send()
})