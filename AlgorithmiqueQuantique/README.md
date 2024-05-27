<div align="center">
  <h1>Intelligence Artificielle - <i>Artificial Intelligence</i></h1>
  <p>
    L'intelligence artificielle est à la mode ! Mais savez vous vraiment vous en servir ? Ces challenges nécessitent d'utiliser des techniques d'intelligence artifielle, voir même de savoir les attaquer ! Je compte rajouter des ressources et peaufiner mes WU dans les prochaines semaines. N'hésitez pas à me contacter sur discord si vous souhaitez plus d'informations. - Sckathach#9336 sur le discord du 404 CTF. 
  </p>
  <p>
    <i>
      Artificial intelligence is all the rage! But do you really know how to use it? These challenges require you to use artificial intelligence techniques, and even know how to attack them! I plan to add more resources and refine my WU over the coming weeks. Don't hesitate to contact me on discord if you'd like more information. Sckathach#9336 on the 404 CTF's official discord.
    </i>
  </p>
  
</div>

## Challenges
- 🟦 Du poison [1/2]
- 🟩 Du poison [2/2]
- 🟧 Des portes dérobées
- 🟧 Du poison [3/2]

## Structure du répertoire
### Partie joueur 
``` 
├── challenges                      -> tous les challenges sont sous la forme de Jupyter Notebook :)
│   ├── chall_1.ipynb
│   ├── chall_2.ipynb
│   ├── chall_3.ipynb
│   └── chall_4.ipynb
├── data/                           -> contient les exemples pour le challenge 4
├── environment.yml
├── fl
│   ├── aggregators.py              -> mise en commun des modèles des différents clients, une simple moyenne ici
│   ├── federated_learning.py       -> exemple d'apprentissage fédéré pour pouvoir esssayer en local
│   ├── __init__.py
│   ├── model.py                    -> définition du modèle utilisé 
│   ├── preprocessing.py            -> traitement en amont des données pour qu'elles soient utilisable
│   ├── types.py
│   └── utils.py                    -> quelques fonctions utilitaires, par exemple pour afficher une image MNIST
├── models/
├── README.md
├── requirements.txt
└── weights
    └── base_fl.weights.h5          -> poids de base du modèle commun         
```

### Partie serveur 
```
├── api
│   ├── challenges.py
│   ├── challenges_weights/
│   ├── config.toml
│   ├── federated_learning.py       -> aprentissage fédéré côté serveurs avec les poids des autres clients déjà 
                                            calculés pour réduire le temps de calcul et surtout pour rendre le processus
                                            déterministe par rapport aux poids du joueur
│   ├── force_data/
│   ├── __init__.py
│   ├── main.py                     -> point d'entrée de l'API
│   └── utils.py
├── fl/
├── solutions
│   ├── adv.py                      
│   ├── adv_utils.py
│   ├── challenge_1_solution.ipynb
│   ├── challenge_2_solution.ipynb
│   ├── challenge_3_solution.ipynb
│   ├── challenge_4_solution.ipynb
│   ├── __init__.py
├── Dockerfile
└── weights
    └── base_fl.weights.h5
```

## Utilisation du serveur pour les tests 
La partie serveur est disponible dans `api/`. Pour l'utiliser, vous pouvez utiliser [Docker](https://www.docker.com/) 
avec : 
```shell
docker build -t challenges-ia . 
docker run -p 8000:8000 challenges-ia
```

Il est aussi possible d'utiliser directement l'API avec Python : 
```shell
python -m api.main
```

## Installation de la partie challenges sur Linux
> [!WARNING]
> ***&rarr;Il faut récupérer la version 2.15 de tensorflow.***

### Avec un environnement virtuel python
```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements
```
Sinon, pensez à installer Tensorflow correctement : https://www.tensorflow.org/install/pip

Pour utiliser une autre version de Python, il est possible d'appeler la commande différemment :  
```shell
python3.11 -m venv .venv
```
Je vous conseille d'utiliser Python 3.11, tous les challenges devraient fonctionner dessus. 

## Installation de la partie challenges avec Conda
```shell
conda create -n flow python=3.11
conda activate flow 
conda install -c conda-forge tensorflow=2.15
conda install jupyter pandas matplotlib
```

## Installation de la partie challenges sur Archlinux 
- Tutoriel incroyable pour installer les *drivers* Nvidia : https://github.com/korvahannu/arch-nvidia-drivers-installation-guide/blob/main/README.md

- Pour que la configuration reste au redémarrage : `sudo nvidia-persistenced --user nvidia-persistenced --persistence-mode`

- Il est possible (et je recommande si vous utilisez les modules dans plein de projets différents), d'installer les paquets de manière globale, par exemple :
```shell
pacman -S tensorflow 
```
> Il faudra alors demander à l'environnement virtuel de tout prendre en compte : `python -m venv --system-site-packages .venv`.

## Installation de la partie challenges sur autre chose que Linux
> [!TIP]
> Bonne chance :)

## Challenges sur Colab
Il est possible de faire tous les challenges sur Google Colab pour ne pas avoir à utiliser votre ordinateur. Pensez juste à ajouter le module `fl` comportant toutes les fonctions utilitaires dans votre session. 


