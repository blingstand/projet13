"""
	In this page you can find context for the sheet views script
"""
context_sheet_view = {
    'button_value':[
        {'name' : 'Ajouter',    'id' : 'ajouter', 'function' : 'add()'}, 
        {'name' : 'Modifier',   'id' : 'modifier', 'function' : 'alter()'},
        {'name' : 'Supprimer',  'id' : 'supprimer', 'function' : 'remove()'}],
    'anim_cols':["Nom", "Stérilisation", "Espèce", "Race", "Propriétaire", "Num dossier"]}

context_contact_owner_view = {
            'historic_cols':["Date", "Type", "Titre", "Objet"],
            'button_value':[
                {'name' : 'Ajouter Prise de Contact',    'id' : 'ajouter', 'function' : 'Add()'}, 
                {'name' : 'Modifier Prise <br> de Contact',   'id' : 'modifier', 'function' : 'Alter()'},
                {'name' : 'Supprimer Prise de Contact',  'id' : 'supprimer', 'function' : 'Remove()'}]
        }