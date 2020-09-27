"""
	In this page you can find context for the sheet views script
"""
context_sheet_view = {
    'button_value':[
        {'name' : 'Ajouter Animaux',    'id' : 'ajouter', 'function' : 'add()'}, 
        {'name' : 'Modifier Animaux',   'id' : 'modifier', 'function' : 'alter()'},
        {'name' : 'Afficher Propriétaires',  'id' :'display', 'function' : 'display()'},
        {'name' : 'Supprimer Animal/Animaux',  'id' : 'supprimer', 'function' : 'remove()'}],
    'anim_cols':["nom", "stérilisation", "espèce", "race", "propriétaire", "num dossier", \
        "num tatouage", "num puce"]}

context_contact_owner_view = {
            'historic_cols':["Date", "Type", "Titre", "Objet"],
            'button_value':[
                {'name' : 'Ajouter Contact',    'id' : 'ajouter', 'function' : 'Add()'}, 
                {'name' : 'Modifier Contact',   'id' : 'modifier', 'function' : 'Alter()'},
                {'name' : 'Supprimer Contact',  'id' : 'supprimer', 'function' : 'Remove()'}]
        }