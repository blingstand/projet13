/* from spa_core */

/***** variables */
const url = window.location.href
let csrftoken ="{{csrf_token}}"
let csrfSafeMethod
let variables = ["name", "color", "species", "race", 
"date_of_birth", "date_of_adoption", "caution", "nature_caution", 
"file", "chip", "tatoo", "is_neutered", "date_of_neuter", 
"futur_date_of_neuter", "status", "select_owner"]
let param = ""

/***** functions */

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
			document.getElementById('id_return').remove()
		}
		for (div of ownDivs){
			div.classList.replace("d-flex", "d-none")
		}
	}

	const OpenSmallPageOwner = (url_open) =>{
		//open an adittionnal page to add / modify owner datas
		const width  = document.body.clientWidth;
		const height = document.body.clientHeight;
		let wanted_width = (width * 35)/100
		let wanted_height = (height * 70)/100
		let spec =  "toolbar=yes,scrollbars=yes,resizable=yes,top=50,left=200,width="
		spec += wanted_width+",height="+wanted_height
		window.open(url_open, "_blank", spec);
	}

	// displays owner form with data from ajax request 
	const sendDatasToServer = function(value, url, whatToDo){
		// this functions fills the inputs with the given data from animal
		csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
		//AJAX
		csrfSafeMethod = function(method) {
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
	    // console.log("sendDatasToServer")
	    // console.log("data : " + value)
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
		if (document.getElementsByClassName("new-former")[0]){
			let divNF = document.getElementsByClassName("new-former")[0]
			let ownDivs = document.getElementsByClassName('owner_input') //div for input owner
			divNF.classList.replace("d-flex", "d-none")
			for (div of ownDivs){
				div.classList.replace("d-none", "d-flex")
			}
		}
		removeFromOwnerBlank()
		document.getElementById("id_mail_reminder").value = 0
		document.getElementById("id_tel_reminder").value = 0
	}

	// fill blank with given values 
	const fillBlank = function(value){
		ids = ["id_owner_name", "id_owner_surname", 'id_phone', "id_mail"]
		values = [value.name, value.surname, value.phone, value.mail]
		console.log("test fillBlank")
		console.log(document.getElementById('id_mail'))
		console.log(values[3])

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
	const GetParam = function(){
		//return param from url 
		let endUrl = url.split("/")
		endUrl = endUrl[endUrl.length-1]
		return endUrl
	}
	// remove data from owner Form
	const removeFromOwnerBlank = function(){
		ids = ["id_owner_name", "id_owner_surname", 'id_phone', "id_mail", 
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
			returnChoice = document.createElement('button')
			returnChoice.id = "id_return"
			returnChoice.textContent = "Retour"
			returnChoice.onclick = function(event){
				event.preventDefault()
				CleanOwnerInput(event)
			}
			divNF.appendChild(returnChoice)


		}

		/***** events */
		if (document.getElementById('submit')){
			document.getElementById('submit').addEventListener('click', function(event){
		//checks data consistency
		IsNeutered = document.getElementById('id_is_neutered_0').checked
		willBeNeuterable = document.getElementById('id_is_neutered_2').checked
		aniHasCaution = document.getElementById('id_caution').value
		console.log(Number(aniHasCaution) < 1)
		if (IsNeutered){
			alert("Si l'animal est déjà stéril, ne pas l'enregistrer.")
			event.preventDefault()
		}else{
			console.log("willBeNeuterable: ", willBeNeuterable)
			if (willBeNeuterable){
				if (document.getElementById('id_futur_date_of_neuter').value == ""){
					alert("Si l'animal n'est pas encore stéril, il faut indiquer quand il le sera.")
					event.preventDefault()
					return
				}
			}
			if (aniHasCaution == "" || Number(aniHasCaution) < 1) {
				alert("Si l'animal n'est pas stéril, il faut une caution.")
				event.preventDefault()
			}
		}
	});
		}
		if (document.getElementById('id_species')){
			document.getElementById('id_species').addEventListener('click', function(){
				if (document.getElementById('id_species_0').checked || document.getElementById('id_species_1').checked){
					document.getElementById('id_caution').value = "100"
				}else{
					document.getElementById('id_caution').value = "200"
				}})}