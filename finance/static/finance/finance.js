var elist;

function _nativeSubmit(event) {
    var input = document.createElement('input');
    var form = document.querySelector("#ticker-form")
    input.hidden = true;
    input.name = "ticker";
    input.value = document.querySelector("#ticker").value
    form.appendChild(input);
    form.submit();
}

function search(){
    var input = document.querySelector(".hidden-input");
    input.style.display="inline";
    input.focus();
    //input.addEventListener("focus", hidesearch());
}

function hidesearch(){
    if (document.querySelector(":focus") != document.querySelector("paper-input")){
        var input = document.querySelector("paper-input");
        input.style.display="none";
        try{
        input.removeEventListener("focusout", hidesearch());
        }
        catch (RangeError) {}
    }
    else{
        removetimer();
    }
}

function removetimer(){
    window.clearTimeout(elist);
}