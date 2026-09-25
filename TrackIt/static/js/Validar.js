document.getElementById("login").addEventListener("submit",function(e){
    let usuario = document.getElementById("TxtUsuario");
    let password = document.getElementById("TxtPassword");  
    let mensaje = document.getElementById("Lblmensaje");  
    let valido = true;

    mensaje.innerText = "";
    usuario.classList.remove("error");
    password.classList.remove("error");

    if(usuario.value.trim() === ""){
        mensaje.innerText = "El campo de usuario o contraseña está vacío";
        usuario.classList.add("error");
        valido=false;
    }else {
        usuario.classList.remove("error");
    }
    if (!valido) {
        e.preventDefault();
    }       

    if(password.value.trim() === ""){
        mensaje.innerText = "El campo de usuario o contraseña está vacío";
        password.classList.add("error");
        valido=false;
    }else {
        password.classList.remove("error");
    }
    if (!valido) {
        e.preventDefault();
    }
});
