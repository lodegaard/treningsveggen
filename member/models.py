from django.conf import settings
from django.db import models
from django_facebook.models import FacebookModel

import logging
logger = logging.getLogger(__name__)


try:
    # There can only be one custom user model defined at the same time
    if getattr(settings, 'AUTH_USER_MODEL', None) == 'member.FacebookMember':
        from django.contrib.auth.models import AbstractUser, UserManager
        class FacebookMember(AbstractUser, FacebookModel):
            '''
            The django 1.5 approach to adding the facebook related fields
            '''
            objects = UserManager()
            # add any customizations you like
            state = models.CharField(max_length=255, blank=True, null=True)
except ImportError as e:
    logger.info('Couldnt setup FacebookUser, got error %s', e)
    pass
