const url = window.location.href
const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();


//clean owner input and display form like beginning
const CleanOwnerInput = function(e){
	//remplace all the owner input value with an empty one
	inputs = Array.from(document.querySelectorAll(".owner_input input"))
	for (input of inputs){
		if (input.id == "id_owner_sex_0" || input.id == "id_owner_sex_1"){
		}else{
			console.log(input.id + " effacé")
			input.value = ""
		}
	}
	divNF.classList.replace("d-none", "d-flex")
	divFormer.classList.replace("d-none", "d-flex")
	divNew.classList.replace("d-none", "d-flex")
	if (document.getElementById('id_select')){
		document.getElementById('id_select').remove()
	}
	for (div of ownDivs){
		div.classList.replace("d-flex", "d-none")
	}
}

// displays owner form with data from ajax request 
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
// Owner form
const dispNewOwn = function(){
	divNF.classList.replace("d-flex", "d-none")
	for (div of ownDivs){
		div.classList.replace("d-none", "d-flex")
	}
	removeFromOwnerBlank()
}

// fill blank with given values
const fillBlank = function(value){
	ids = ["id_owner_name", "id_owner_surname", 'id_phone', "id_mail"]
	values = [value.name, value.surname, value.phone, value.mail]
	for (index in ids){
		input = document.getElementById(ids[index])
		input.value = values[index]
	}
	let inputSex = document.getElementById('id_owner_sex').children;
	if (value.sex == 0){
		inputSex[0].firstChild.firstChild.checked = true
	}else{
		inputSex[1].firstChild.firstChild.checked = true
	}
}
const getBaseUrl = function(){
    //return the base url usefull for button add and alter
    let param = GetParam()
    if (param != ""){
        let baseUrl = url.split('/')
        baseUrl.pop(param)
        baseUrl = baseUrl.join("/")+"/"
        return baseUrl
    }
    return url
}
const GetParam = function(){
	//return param from url 
	param = url.split("/")
	param = param[param.length-1]
	return param
}
// remove data from owner Form
const removeFromOwnerBlank = function(){
	ids = ["id_owner_name", "id_owner_surname", 'id_phone', "id_mail", "id_caution", 
	"id_mail_reminder", "id_tel_reminder"]
	for (index in ids){
		input = document.getElementById(ids[index])
		input.value = ""
	}
}
// creates and displays select with owners name and validate button
const SelectOwners = function(owners, url, whatToDo){
	divFormer.classList.replace("d-flex", "d-none")
	divNew.classList.replace("d-flex", "d-none")
	select = document.createElement('select')
	select.id = "id_select"
	select.name = "former_owner"
	divNF.appendChild(select)
	for (owner of owners){
		option = document.createElement('option')
		option.value = owner.id
		option.onclick = function(event){
			value = {'ask_owner_data':"1", 'owner_id':event.target.value}
			sendDatasToServer( value, url, whatToDo)}
		option.innerHTML = owner.name
		select.appendChild(option)
	}
}
