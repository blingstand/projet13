/* maj 1.1
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


let param = ""

const BackCNS = function (pageName,destination){
    param = GetParam()
    newPage = url.split('/')
    idContent = newPage.indexOf(pageName)
    if (param != pageName){
        //fullPath - content - mail_id + cns
        window.location.href = destination+"/"+ param
    }else{
        let response = true
        if (pageName == "content"){
            response = confirm("Si vous quittez vous perdrez ce qui n'a pas été sauvegardé. Continuer ?")
        }
        if (response){
            newPage.splice(idContent,1, "cns")
            newPage = newPage.join('/')
            window.location.href = destination
        }
    }       
}
