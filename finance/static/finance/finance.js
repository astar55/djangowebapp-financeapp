var count = 0;

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
    this.count = 0;
    var input = document.querySelector(".hidden-input");
    input.style.display="inline";
    input.focus();
    input.addEventListener("focusout", hidesearch());
    console.log(count)
}

function hidesearch(){
    this.count += 1;
    if (this.count >= 2){
        var input = document.querySelector("paper-input");
        input.style.display="none";
        try{
            input.removeEventListener("focusout", hidesearch());
        }
        catch (RangeError){}
    }
    console.log(count)
}