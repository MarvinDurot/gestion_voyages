"""
Gestion de l'application en mode textuel
"""

from services import *
from models import Session
import os


class MenuAction:
    """
    Action composant un menu textuel,
    définie par un nom, une callback (éxécutée si action sélectionnée)
    et une donnée perso (ex: id d'une table)
    """

    def __init__(self, name, callback, data=None):
        self.name = name
        self.data = data
        self.callback = callback

    def __repr__(self):
        return self.name

    def execute(self):
        self.callback(self.data)


class Menu:
    """
    Menu textuel gérant des actions numérotées
    """

    def __init__(self, title, actions=list()):
        self.title = title
        self.actions = actions

    def loop(self):
        """
        lance la boucle d'affichage du menu
        :return: void
        """
        error = False
        while True:
            self.clear()
            print(self)

            if error:
                print("Saisie invalide!\n")

            try:
                choice = int(input('Votre choix : '))
                self.clear()
                self.actions[choice].execute()
            except IndexError:
                error = True
                continue
            except ValueError:
                break
            except KeyboardInterrupt:
                break
            else:
                error = False
                continue

    def add(self, action):
        """
        Ajoute une action au menu
        :param action: une action
        :return: void
        """
        self.actions.append(action)

    def getTitle(self):
        """
        Accesseur pour l'attribut title
        :return: string
        """
        return self.title

    @staticmethod
    def clear():
        """
        Efface la console (fonctionne sur Linux et Windows)
        :return: void
        """
        os.system("cls" if os.name == "nt" else "clear")

    def __repr__(self):
        """
        Redéfinition de la représentation en chaîne
        :return: string
        """
        string = "========== %s ==========\n\n" % self.title
        for idx, action in enumerate(self.actions):
            string += "[%s] - %s \n" % (idx, action)
        string += "\nAppuyer sur [Entrée] pour quitter...\n"
        return string


class Application:
    """
    Application de gestion de voyages en mode textuel
    """

    def __init__(self):
        self.city_service = CityService()
        self.travel_service = TravelService()
        self.menu = Menu("Menu principal", self.getActions())

    def getActions(self):
        action_showTravels = MenuAction("Consulter les voyages", self.all)
        action_deleteTravel = MenuAction("Supprimer un voyage", self.delete)
        action_addTravel = MenuAction("Ajouter un voyage", self.create)
        return [action_showTravels, action_deleteTravel, action_addTravel]

    def all(self, args):
        actions = []
        for travel in self.travel_service.all():
            actions.append(MenuAction(str(travel), self.show, travel.id))
        menu = Menu("Choisir un voyage", actions)
        menu.loop()

    def show(self, id):
        travel = self.travel_service.find(id)
        print("%s \n\nreview=%s)" % (travel, travel.review))
        input("\nAppuyez sur une touche pour continuer...")

    def delete(self, args):
        actions = []
        for travel in self.travel_service.all():
            actions.append(MenuAction(str(travel), self.travel_service.delete, travel.id))
        menu = Menu("Supprimer un voyage", actions)
        menu.loop()

    def create(self, args):
        travel = Travel()
        travel.input()

        while True:
            try:
                print("\n==== Nouveau transport ====\n")
                transport = Transport()
                transport.input()
                travel.transports.append(transport)
            except ValueError:
                break

        while True:
            try:
                print("\n==== Nouvel hébergement ====\n")
                accomodation = Accomodation()
                accomodation.input()
                travel.accomodations.append(accomodation)
            except ValueError:
                break

        self.travel_service.save(travel)

    def run(self):
        self.menu.loop()


if __name__ == '__main__':
    # Création et lancement de l'application
    app = Application()
    app.run()
