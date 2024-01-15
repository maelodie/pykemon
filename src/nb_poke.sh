#!/bin/bash

python3 main.py | tail -n +3 > temp.txt

# Créer un fichier de commandes Gnuplot temporaire
echo "plot 'temp.txt' using 1:2 with lines title 'nb pokemon feu', \
        'temp.txt' using 1:3 with lines title 'nb pokemon eau', \
        'temp.txt' using 1:4 with lines title 'nb pokemon poison'" > plot.gp
      

# Exécuter Gnuplot avec le fichier de commandes temporaire
gnuplot -p plot.gp

# Supprimer le fichier de commandes temporaire
rm plot.gp
rm temp.txt
