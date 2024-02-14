class LivreRepository:
    def __init__(self):
        self.livres = []
        self.prochain_id = 1  # Initialisez le prochain ID à 1

    def creer(self, titre, auteur):
        livre = Livre(self.prochain_id, titre, auteur)  # Ajoutez l'ID au livre
        self.livres.append(livre)
        self.prochain_id += 1  # Incrémente le prochain ID

    def lire_tous(self):
        return self.livres

    def lire(self, titre):
        for livre in self.livres:
            if livre.titre == titre:
                return livre
        return None

    def mettre_a_jour(self, id, nouveau_titre, nouveau_auteur):
        for livre in self.livres:
            if livre.id == id:
                livre.titre = nouveau_titre
                livre.auteur = nouveau_auteur
                break

    def supprimer(self, id):
        livre = self.lire_par_id(id)
        if livre:
            self.livres.remove(livre)

    def lire_par_id(self, id):
        for livre in self.livres:
            if livre.id == id:
                return livre
        return None