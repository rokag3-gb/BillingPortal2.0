
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    const colorMode = window.localStorage.getItem('colorMode');
    if (colorMode == "auto"){
        dispatchColorModeEvent(e.matches? "dark":"light");
    }
});

function dispatchColorModeEvent(mode){
    let colorModeVal = "";
    switch(mode){
        case "dark":
            colorModeVal = "dark";
            break;
        case "light":
            colorModeVal = "light";
            break;
        default:
            colorModeVal = window.matchMedia('(prefers-color-scheme: dark)').matches? "dark" : "light";
            break;
    }
    window.dispatchEvent(new CustomEvent('colorMode', {detail: colorModeVal}));
}

//mode: dark, light or auto
function setColorMode(mode){
    switch(mode){
        case "dark":
            window.localStorage.setItem("colorMode", "dark");
            break;
        case "light":
            window.localStorage.setItem("colorMode", "light");
            break;
        case "auto":
            window.localStorage.setItem("colorMode", "auto");
            break;
    }
    dispatchColorModeEvent(mode)
}

function getColorMode(){
    const colorModePref = window.localStorage.getItem('colorMode');
    let colorModeVal = "";
    switch(colorModePref){
        case "dark":
            colorModeVal = "dark";
            break;
        case "light":
            colorModeVal = "light";
            break;
        default:
            colorModeVal = window.matchMedia('(prefers-color-scheme: dark)').matches? "dark" : "light";
            break;
    }
    return colorModeVal;
}

window.addEventListener('load', ()=>{
    try{
        // Color Mode setting init
        const colorMode = window.localStorage.getItem('colorMode');
        document.getElementById("colorModeSelect").value = !colorMode? "auto":colorMode;
    }catch(e){}

    // Dark mode css init
    let darkModeCss = document.querySelector(`link[href="${darkModeCssPath}"]`);
    darkModeCss.disabled = getColorMode()!="dark";

    // Logo hide init
    const elemsToHide = document.getElementsByClassName((getColorMode()=="dark"?"light":"dark")+"mode-only")
    const elemsToShow = document.getElementsByClassName((event.detail)+"mode-only")
    for(let item of elemsToHide){
        item.style.display = "none";
    }
    for(let item of elemsToShow){
        item.style.display = "block";
    }

    window.addEventListener('colorMode', (event)=>{
        console.log(event.detail)
        darkModeCss.disabled = event.detail!="dark";

        const elemsToHide = document.getElementsByClassName((event.detail=="dark"?"light":"dark")+"mode-only");
        const elemsToShow = document.getElementsByClassName((event.detail)+"mode-only")
        for(let item of elemsToHide){
            item.style.display = "none";
        }
        for(let item of elemsToShow){
            item.style.display = "block";
        }

        let sidebar = document.getElementById("sidebar_class");
        sidebar.classList.remove(event.detail=="dark"?"navbar-card":"navbar-vibrant");
        sidebar.classList.add(event.detail=="dark"?"navbar-vibrant":"navbar-card");
    })

    
    
});

