<div align="center">
  <h1>Algorithmique quantique - <i>Quantum computing</i></h1>
</div>

## Challenges
- 🟦 Des trains superposés
- 🟩 De l'écoute, pas très discrète
- 🟧 De la multiplicité des problèmes
- 🟥 De l'inversion

## Installation challenges
Avec un environnement virtuel Python : 
```shell
python -m venv .venv 
source .venv/bin/activate
pip install -r requirements.txt
```

Si les requirements ne passent pas, il suffit de Perceval, Qiskit (pour les visualisations de la sphère de Bloch), et 
Numpy Matplotlib : 
```shell 
pip install perceval-quandela qiskit numpy matplotlib
```

## Installation API pour vérifier les challenges 
J'ai utilisé FastAPI pour vérifier les challenges côté serveur. Vous pouvez tout reproduire en local, tout le code est 
disponible dans le module `api/`. Pour cela, vous aurez besoin de : 
```shell
pip install toml fastapi uvicorn
```

Il vous suffira ensuite d'[installer Docker sur votre système](https://docs.docker.com/get-docker/) puis de construire 
et lancer l'API : 
```shell
# À la racine du dossier 
docker build -t perceval . 
docker run -p 8000:8000 perceval 
```

## Ressources supplémentaires
- Il est recommandé de faire le tour de présentation de Perceval :
  https://perceval.quandela.net/docs/notebooks/Tutorial.html

- Il sera peut-être utile de jeter un coup d'œil à la documentation de Perceval : https://perceval.quandela.net/docs/
  ou directement au code : https://github.com/Quandela/Perceval, la documentation est jeune et pas encore complète.

- Un forum Perceval est disponible ici : https://perceval.quandela.net/forum/

- Excellentes vidéos d'IBM : https://learning.quantum.ibm.com/. Le framework utilisé est celui de qiskit, mais la
  théorie est la même.

- Pour ceux qui préfèrent les livres : [Quantum computation and quantum information](https://www.cambridge.org/highereducation/books/quantum-computation-and-quantum-information/01E10196D0A682A6AEFFEA52D53BE9AE#overview)
  de Michael Nielsen et Isaac Chuang. Il est disponible à la bibliothèque nationale de France François Mitterrand.

## Papiers intéressants
- Multi-partite quantum cryptographic protocols with noisy GHZ states : https://arxiv.org/abs/quant-ph/0404133
- Analysis of Various Attacks over BB84 Quantum Key Distribution Protocol :
  https://www.ijcaonline.org/volume20/number8/pxc3873313.pdf
- Simple Proof of Security of the BB84 Quantum Key Distribution Protocol :
  https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.85.441

## L'année prochaine (*shht...*)
- Solving the Network Shortest Path Problem on a Quantum Annealer : https://ieeexplore.ieee.org/document/9186612
- Entanglement in Graph States and its Applications : https://arxiv.org/abs/quant-ph/0602096
- Quantum Algorithms for Lattice Problems : https://eprint.iacr.org/2024/555

