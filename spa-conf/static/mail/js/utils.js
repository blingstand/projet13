/*
    this script is working for 
    mail/
        content.html
        settings.html
        cns.html

    plan :
    > variables
    > fonctions
    > events
*/

let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

const sendDatasToServer = function(value, url, whatToDo){
    // this functions fills the inputs with the given data from animal
    //AJAX
    const csrfSafeMethod = function(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            // if not safe, set csrftoken
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    }); 
    console.log("sendDatasToServer")
    console.log("data : " + value)
    $.ajax({ 
        type:"POST", 
        url: url, 
        dataType: 'json',
        data: value,
        success: function (res) {
            if (res.data){
                whatToDo(res.data)
            }else{
                whatToDo()
            }
            
        },
        error: function (res) {
            alert("erreur lors de l'envoie de données");
            console.log(res.status);
            console.log(res.error);
        }
    })          
}



const BackCNS = function (pageName){
    let param = GetParam()
    newPage = url.split('/')
    idContent = newPage.indexOf(pageName)
    if (param != pageName){
        //fullPath - content - mail_id + cns
        newPage.splice(idContent, 1, "cns")
        newPage = newPage.join('/')
        window.location.href = newPage
    }else{
        let response = true
        if (pageName == "content"){
            response = confirm("Si vous quittez vous perdrez ce qui n'a pas été sauvegardé. Continuer ?")
        }
        if (response){
            newPage.splice(idContent,1, "cns")
            newPage = newPage.join('/')
            window.location.href = newPage
        }
    }       
}
const GetParam = function(){
    //return param from url 
    param = url.split("/")
    param = param[param.length-1]
    return param
}