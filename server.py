#
# Serveur de l'application
#

from mako.lookup import TemplateLookup
from services import CityService, TravelService
from models import Travel, City, Transport, Accomodation, Session
import cherrypy
import os

# Emplacement local et emplacements des templates
_current_dir = os.path.abspath(os.path.dirname(__file__))
_template_dir = os.path.join(_current_dir, 'templates')
_module_dir = os.path.join(_template_dir, 'mako_modules')

mylookup = TemplateLookup(
    directories=[_template_dir],
    module_directory=_module_dir,
    input_encoding='utf-8',
    output_encoding='utf-8',
    encoding_errors='replace'
)

# Templates de l'application
_home = mylookup.get_template('page_home.mako.html')
_travel = mylookup.get_template('page_travel.mako.html')
_travels = mylookup.get_template('page_travels.mako.html')
_backend = mylookup.get_template('page_backend.mako.html')
_backend_travels = mylookup.get_template('page_backend_travels.mako.html')
_backend_cities = mylookup.get_template('page_backend_cities.mako.html')


class Controller:
    """
    Contrôleur par défaut (héritage)
    """

    # Messages
    _creation_success = 'Création réussie !'
    _creation_error = 'Erreur lors de la création !'
    _deletion_success = 'Suppression réussie !',
    _deletion_error = 'Erreur lors de la suppression !'
    _loading_success = 'Chargement réussi !'
    _loading_error = 'Erreur lors du chargement !'

    def __init__(self):
        self.message = None
        self.title = ''
        self.travel_service = TravelService()
        self.city_service = CityService()

    def setMessage(self, message):
        self.message = message

    def setTitle(self, title):
        self.title = title

    def render(self, view, **kwargs):
        return view.render_unicode(title=self.title, message=self.message, **kwargs)

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
        self.setTitle('Accueil')
        return self.render(_home)

    @cherrypy.expose
    def travel(self, travel_id=None):
        try:
            travel = self.travel_service.find(travel_id)
        except:
            raise cherrypy.NotFound

        self.setTitle('Fiche voyage')
        return self.render(_travel, travel=travel)

    @cherrypy.expose
    def travels(self, sorting=None):
        # Tri par capital
        if sorting == 'capitals':
            travels = self.travel_service.all_capitals()
            self.setTitle('Liste des voyages concernant une capitale')
        # Tri par budget
        elif sorting == 'budget':
            travels = self.travel_service.all_by_budget()
            self.setTitle('Liste des voyages triés par budget')
        # Tri par durée de transport
        elif sorting == 'transport_duration':
            travels = self.travel_service.all_by_transport_duration()
            self.setTitle('Liste des voyages triés par durée de transport')
        # Tri par défaut
        else:
            travels = self.travel_service.all()
            self.setTitle('Liste des voyages')

        if len(travels) == 0:
            raise cherrypy.NotFound
        else:
            return self.render(_travels, travels=travels)


class BackendController(Controller):
    """
    Contrôleur de la partie backend
    """

    @cherrypy.expose
    def index(self):
        self.setTitle('Menu administration')
        return self.render(_backend)

    @cherrypy.expose
    def travels(self, travel_id=None, city_id=None, start=None, end=None, review=None, accomodation_name=None,
                accomodation_type=None, accomodation_price=None, transport_type=None, transport_price=None,
                transport_duration=None, save=None, delete=None):

        # Récupération du voyage si son id est précisé
        if travel_id is None:
            travel = None
        else:
            travel = self.travel_service.find(travel_id)

        # On a cliqué sur le bouton de suppression
        if delete is not None:
            self.setMessage(self._deletion_success)
            try:
                self.travel_service.delete(travel.id)
            except:
                self.setMessage(self._deletion_error)
        # On a cliqué sur le bouton de sauvegarde
        elif save is not None:
            self.setMessage(self._creation_success)
            try:
                self.travel_service.create(city_id, start, end, review, accomodation_name, accomodation_type,
                                           accomodation_price, transport_type, transport_price, transport_duration)
            except:
                self.setMessage(self._creation_error)

        # Récupération des données
        self.setTitle('Gérer les voyages')
        travels = self.travel_service.all()
        cities = self.city_service.all()

        return self.render(_backend_travels, cities=cities, travels=travels, travel=travel)

    @cherrypy.expose
    def cities(self, city_id=None, name=None, is_capital=None, country=None, capital_id=None, delete=None, save=None):
        # Récupération de la ville si son id est précisé
        if city_id is None:
            city = None
        else:
            city = self.travel_service.find(city_id)

        # On a cliqué sur le bouton de suppression
        if delete is not None:
            self.setMessage(self._deletion_success)
            try:
                self.travel_service.delete(city.id)
            except:
                self.setMessage(self._deletion_error)
        # On a cliqué sur le bouton de sauvegarde
        elif save is not None:
            self.setMessage(self._creation_success)
            try:
                self.city_service.create(name, is_capital, country, capital_id)
            except:
                self.setMessage(self._creation_error)

        # Récupération des données
        self.setTitle('Gérer les villes')
        capitals = self.city_service.all_capitals()
        cities = self.city_service.all()

        return self.render(_backend_cities, cities=cities, capitals=capitals, city=city)


def validate_password(real, username, password):
    """
    Fonction de vérification du login / mot de passe

    :param real:
    :param username: string
    :param password: string
    :return: boolean
    """
    if username == 'admin' and password == 'admin':
        return True
    else:
        return False


if __name__ == '__main__':
    # Configuration générale de CherryPy
    global_conf = {
        'global': {
            'autoreload.on': False,
            'server.socket_host': '127.0.0.1',
            'server.socket_port': 8080,
            'server.protocol_version': 'HTTP/1.1',
            'server.thread_pool': 5,
            'tools.encode.encoding': 'utf-8',
            'log.error_file': os.path.join(_current_dir, 'error.log'),
            'log.screen': True
        }
    }

    # Mise à jour de la configuration de CherryPy
    cherrypy.config.update(global_conf)

    # Configuration de l'application
    app_conf = {
        '/backend': {
            'tools.auth_basic.on': True,
            'tools.auth_basic.realm': '127.0.0.1',
            'tools.auth_basic.checkpassword': validate_password
        },
        '/assets': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(_current_dir, 'assets')
        },
        '/assets/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(_current_dir, 'assets/css'),
            'tools.staticdir.content_types': {'css': 'text/css'}
        },
        '/assets/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(_current_dir, 'assets/js'),
            'tools.staticdir.content_types': {'js': 'application/javascript'}
        }
    }

    # Lancement du serveur
    cherrypy.quickstart(FrontendController(), '/', config=app_conf)
