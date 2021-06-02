
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
    window.dispatchEvent(new Event('colormode', {colorMode: colorModeVal}));
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
    const colorModePref = localStorage.getItem('colorMode');
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