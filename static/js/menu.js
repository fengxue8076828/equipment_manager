
window.addEventListener('load',getMenu)

function getMenu(){
    const menuContainer=document.getElementById("menu-items")
    let menuHTML=""
    const xhr=new XMLHttpRequest()
    xhr.open('GET',"menu/",true)
    xhr.onload=function(){
        if (this.status===200){
            const responseText=JSON.parse(this.responseText)
            let menuItems=JSON.parse(responseText.menu)
            console.log(menuItems)
            for (let menu of menuItems) {
                if(!menu.fields.parent_module){
                    const menuItemHTML=`
                        <div class="menu-item" id="${menu.pk}">
                            <div class="menu-item-title">
                                <i class="fa-solid fa-file-lines"></i>
                                <h3 class="menu-item-text">${menu.fields.name}</h3>
                            </div>
                            <i class="fa-solid fa-caret-right"></i>
                        </div>
                    `
                    menuHTML+=menuItemHTML
                }
            }
            menuContainer.innerHTML=menuHTML

        }
    }
    xhr.send()
}