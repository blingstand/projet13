sudo service postgresql start
fichier_scss="spa_core/static/spa_core/css/style.scss"
fichier_css="spa_core/static/spa_core/css/style.css"
sass --watch $fichier_scss $fichier_css


# echo $fichier_css  
# if [ ${1} = "w" ]
# then
# 	echo "w a été tapé"
#     ./sass/dart-sass/sass $fichier_scss $fichier_css --watch --poll
# elif [ $1 = "c" ]
# then	
# 	echo "c a été tapé"
# 	./sass/dart-sass/sass $fichier_scss $fichier_css --style=compressed --no-source-map
# else
# 	echo "Commandes : c > compile || w > watch"
# fi
