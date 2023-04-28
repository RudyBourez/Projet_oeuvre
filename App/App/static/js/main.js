const flash = document.querySelector("#flash")
const allitems = document.querySelectorAll('body')
const passwordInput = document.getElementById('password')
const confirmPasswordInput = document.getElementById('confirm_password')

function remove_alerts(){
    if (flash.hasChildNodes()) {
        flash.removeChild(flash.firstChild)
    }
}

function TogglePassword() {
    if (passwordInput.type === "password") {
    passwordInput.type = "text";
    } else {
    passwordInput.type = "password";
    }
  }

function ToggleConfirmPassword() {
    if (confirmPasswordInput.type === "password") {
        confirmPasswordInput.type = "text";
    } else {
        confirmPasswordInput.type = "password";
    }
  }

setTimeout(remove_alerts, 5000)

allitems.forEach(element => {  
    element.addEventListener("click", remove_alerts)
});

