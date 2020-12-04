"""
	In this page you can find context for the sheet views script
"""
context_sheet_view = {
    'button_value':[
        {'name' : 'Ajouter',    'id' : 'ajouter', 'function' : 'add()'}, 
        {'name' : 'Modifier',   'id' : 'modifier', 'function' : 'alter()'},
        {'name' : 'Supprimer',  'id' : 'supprimer', 'function' : 'remove()'}],
    }

context_contact_owner_view = {
            'historic_cols':["Date", "Type", "Titre", "Objet"],
            'button_value':[
                {'name' : 'Ajouter',    'id' : 'ajouter', 'function' : 'Add()'}, 
                {'name' : 'Modifier ',   'id' : 'modifier', 'function' : 'Alter()'},
                {'name' : 'Supprimer',  'id' : 'supprimer', 'function' : 'Remove()'}]
        }


top_columns_anim = ["&nbsp;", "Nom", "Stérilisation", "Espèce", "Race", "Propriétaire", "Num dossier"]

top_columns_owner = [
    "&nbsp", "Identifiant", "Nom", "Prénom", "Nombre d'animaux", "Caution", "Tel", "Mail", 
    "Nb appel", "Nb mail", "Historique"
]
