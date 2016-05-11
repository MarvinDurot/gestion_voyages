#
# Serveur de l'application
#

from services import CityService, TravelService
import cherrypy
import os.path

# Identifiants de l'administrateur
USERNAME = 'admin'
PASSWORD = 'admin'


class Controller:
    """
    Contrôleur par défaut (héritage)
    """

    def __init__(self):
        self.vars = {
            'message': None,
            'title': 'Sans titre'
        }

    def setMessage(self, message):
        self.vars.message = message

    def setTitle(self, title):
        self.vars.title = title

    def getVars(self):
        return self.vars

    @cherrypy.expose
    def default(self):
        raise cherrypy.NotFound


class FrontendController(Controller):
    """
    Contrôleur partie frontend
    """

    def __init__(self):
        self.backend = BackendController()
        super(self.__class__, self).__init__()

    @cherrypy.expose
    def index(self):
        return '''<p>Page d'acceuil</p>'''

    @cherrypy.expose
    def travel(self, travel_id=None):
        try:
            travel = TravelService.find(travel_id)
        except:
            raise cherrypy.NotFound

        return '''<p>Affichage d'un voyage : %s</p>''' % travel

    @cherrypy.expose
    def travels(self, sorting=None):
        if sorting == 'capital':
            return '''<p>Affichage des voyages concernant une capitale</p>'''
        elif sorting == 'price':
            return '''<p>Affichage des voyages par budget</p>'''
        elif sorting == 'duration':
            return '''<p>Affichage des voyages par durée de transport</p>'''
        else:
            return '''<p>Affichage des voyages par défaut</p>'''


class BackendController(Controller):
    """
    Contrôleur de la partie backend
    """

    def __init__(self):
        self._cp_config = {
            'tools.auth_basic.on': True,
            'tools.auth_basic.realm': 'localhost',
            'tools.auth_basic.checkpassword': self.validate_password
        }
        super(self.__class__, self).__init__()

    @staticmethod
    def validate_password(real, username, password):
        if username == USERNAME and password == PASSWORD:
            return True
        else:
            return False

    @cherrypy.expose
    def index(self):
        return '''<p>Page d'administration</p>'''

    @cherrypy.expose
    def travels(self):
        # TODO : traiter l'ajout et la suppression de voyages
        return '''<p>Page de gestion des voyages</p>'''

    @cherrypy.expose
    def cities(self):
        # TODO : traiter l'ajout et la suppression de villes
        return '''<p>Page de gestion des villes</p>'''


if __name__ == '__main__':
    app = FrontendController()
    conf = os.path.join(os.path.dirname(__file__), '/config/server.conf')
    cherrypy.quickstart(app, '/', config=conf)
