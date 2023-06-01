const display = document.getElementById("normalDisplay")
const sidebar = document.getElementById("nav__wrapper");
const mainPage = document.getElementById("main__page");
const nav_items = document.querySelector(".newSection")

function setMainPageOffset(){
    mainPage.style.marginLeft = sidebar.offsetWidth + "px";
}

addEventListener("load", setMainPageOffset);
addEventListener("resize", setMainPageOffset);

//Open add menu

const addButton = document.getElementById("nav__add");
const delButton = document.getElementById("nav__del")
const addMenu = document.getElementById("addMenu");
const delMenu = document.getElementById("delMenu")

async function fetchPageIds() {
    
    let response = await fetch("/page_ids", {
        method: 'GET'
    });
    ids =  await response.json();
    intIds = ids.ids
    return intIds
}

function openAddMenu() {
    display.classList.remove('closeAddMenuEffect');
    display.classList.add('openAddMenuEffect');
    addMenu.style.display = "block";
    display.style.pointerEvents = "none";
}

function openDelMenu() {
    display.classList.remove('closeAddMenuEffect');
    display.classList.add('openAddMenuEffect');
    delMenu.style.display = "block";
    display.style.pointerEvents = "none";
}

addButton.onclick = openAddMenu;
delButton.onclick = openDelMenu;

const closeButton = document.getElementById("close");
const closeDelButton = document.getElementById("closeDel")
const createButton = document.getElementById("create");

function closeAddMenu() {
    display.classList.remove('openAddMenuEffect');
    display.classList.add('closeAddMenuEffect');
    display.style.pointerEvents = "all";
    addMenu.style.display = "none";
}

function closeDelMenu() {
    display.classList.remove('openAddMenuEffect');
    display.classList.add('closeAddMenuEffect');
    display.style.pointerEvents = "all";
    delMenu.style.display = "none";
}


closeButton.onclick = closeAddMenu;
closeDelButton.onclick = closeDelMenu;


const loginButton = document.getElementById("login__button");
const loginMenu = document.getElementById("loginMenu");

async function openLogInMenu()  {
    if(loginButton.innerHTML === "Log In")
    {
        loginMenu.classList.toggle("openWindow");
    } else if(loginButton.innerHTML === "Log Out")
    {
        start = document.cookie.lastIndexOf("token=") + "token=".length;
        token = document.cookie.substring(start, start+33)
        postLogout(token)
        location.reload()
    }
}

async function postLogout(token) {
    let response = await fetch("/logout", {
        method: 'POST',
        headers: {
            'token': token,
          }});
    return await response.json();
}

loginButton.onclick = openLogInMenu;

async function fetchLogin(token) {
    val = ""
    let response = await fetch("/verify_token", {
        headers: {
            'token': token,
          }});
    return await response.json();
}

async function logedinPage() {
    start = document.cookie.lastIndexOf("token=") + "token=".length;
    token = document.cookie.substring(start, start+33);
    text = await fetchLogin(token);
    
    if(text.valid)
    {
        loginButton.innerHTML = "Log Out";
    } else {
        addButton.remove();
        delButton.remove();
        loginButton.innerHTML = "Log In";
    }

    pages = await fetchPageIds()
    console.log(pages.length)
    for(i = 1; i < pages.length; i+=2)
    {
        var a = document.createElement('a');
        var text = document.createTextNode(pages[i].substring(10));
        a.appendChild(text);
        a.title = pages[i].substring(10)
        a.href = "/page/<" + pages[i-1] + ">"
        a.target = "_blank"
        console.log(a)
        nav_items.appendChild(a)
    }

    mainPage.style.marginLeft = sidebar.offsetWidth + "px";
}

addEventListener("load", logedinPage);