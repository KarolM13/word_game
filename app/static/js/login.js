

function login()
{
    const nick = document.getElementById("loginNick").value;
    const password = document.getElementById("loginPassword").value;

    fetch("/api/login_user",{
        method: "POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({nick: nick,password: password})
    })
    .then(r => r.json())
    .then(data =>{
        if(data.success){
            window.location.href ="/";
        } 
        else{
            document.getElementById("loginError").textContent = data.error;
            document.getElementById("loginError").classList.remove("hidden");
        }
    })
}
function register()
{
    const nick = document.getElementById("registerNick").value;
    const password = document.getElementById("registerPassword").value;

    fetch("/api/register_user",{
        method: "POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({nick: nick, password: password})
    })
    .then(r => r.json())
    .then(data =>{
        if(data.success){
            window.location.href="/";
        }
        else{
            document.getElementById("registerError").textContent = data.error;
            document.getElementById("registerError").classList.remove("hidden");
        }
    })
}
document.getElementById("loginBtn").addEventListener("click",login);
document.getElementById("registerBtn").addEventListener("click",register);
document.getElementById("showRegister").addEventListener("click",function(){
    document.getElementById("registerForm").classList.remove("hidden");
    document.getElementById("loginForm").classList.add("hidden");
})
document.getElementById("showLogin").addEventListener("click",function(){
    document.getElementById("registerForm").classList.add("hidden");
    document.getElementById("loginForm").classList.remove("hidden");
})