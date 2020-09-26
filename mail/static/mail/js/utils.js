const url = window.location.href

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