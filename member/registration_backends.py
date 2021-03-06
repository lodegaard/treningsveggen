from django.conf import settings
from django.contrib.auth import authenticate, login, get_backends

from django_facebook import signals
from django_facebook.api import get_persistent_graph
from django_facebook.registration_backends import NooptRegistrationBackend
from django_facebook.utils import get_user_model

from .exceptions import IllegalUserException 

import logging
log = logging.getLogger(__name__)

class FacebookRegistrationBackend(NooptRegistrationBackend):

    """
    A backend compatible with Django Registration
    It is extremly simple and doesn't handle things like redirects etc
    (These are already handled by Django Facebook)
    """

    def register(self, request, form=None, **kwargs):
        """
        Create and immediately log in a new user.

        """
        log.error('Trying to create a new user with username: {}'.format(kwargs['username']))
    
        # Get the groups the user is a member of
        graph = get_persistent_graph(request)
        fb_info = graph.get('me')
        group_members = graph.get('{}/members'.format(settings.TRENINGSVEGGEN_FB_GROUP_ID))
        
        for group_member in group_members['data']:
            if fb_info['id'] == group_member['id']:
                #fb_info = 'User {} with ID {} is member'.format(request.user.first_name, fb_info['id'])
                username, email, password = kwargs['username'], kwargs[
                    'email'], kwargs['password1']
                # Create user doesn't accept additional parameters,
                new_user = get_user_model(
                ).objects.create_user(username, email, password)
        
                signals.user_registered.send(sender=self.__class__,
                                             user=new_user,
                                             request=request)
                authenticated_user = self.authenticate(request, username, password)
                return authenticated_user
        
        raise IllegalUserException

    def authenticate(self, request, username, password):
        # authenticate() always has to be called before login(), and
        # will return the user we just created.
        authentication_details = dict(username=username, password=password)
        user = authenticate(**authentication_details)
        login(request, user)

        if user is None or not user.is_authenticated():
            backends = get_backends()
            msg_format = 'Authentication using backends %s and data %s failed'
            raise ValueError(msg_format % (backends, authentication_details))

        return user

