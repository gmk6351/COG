'''
Middleware that intercepts the request/response during user authentication in order to:
a) enforce an IdP whitelist
b) detects the possible authentication errors,
and redirect to the authentication page with informative error messages.
'''

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from cog.plugins.esgf.idp_whitelist import LocalWhiteList

class LoginMiddleware(object):

    def __init__(self):

        # initialize the white list service
        self.whitelist = LocalWhiteList(settings.IDP_WHITELIST)

        # login URLs
        self.url1 = "/login/"
        self.url2 = "/openid/login/"


    def process_request(self, request):
        '''
        Method called before processing of the view.
        Used to intercept the openid login request before it is sent to the remote IdP.
        '''

        # intercept only these requests
        if request.path == self.url2:

            # DEBUG
            #print 'OpenID login request: %s' % request

            openid_identifier = request.REQUEST.get('openid_identifier', None)
            next = request.REQUEST.get('next', "/") # preserve 'next' redirection after successful login
            if openid_identifier is not None:

                # invalid OpenID
                if not openid_identifier.lower().startswith('https'):
                    return HttpResponseRedirect(reverse('openid-login')+"?message2=invalid_openid&next=%s&openid=%s" % (next, openid_identifier))

                # invalid IdP
                if not self.whitelist.trust(openid_identifier):
                    return HttpResponseRedirect(reverse('openid-login')+"?message2=invalid_idp&next=%s&openid=%s" % (next, openid_identifier) )

        # keep on processing this request
        return None


    def process_response(self, request, response):
        '''
        Method called after processing of the view.
        Used to intercept the login response in case of errors.
        '''

        # request parameters to include when redirecting
        next = request.REQUEST.get('next', "/") # preserve 'next' redirection after successful login
        openid_identifier = request.REQUEST.get('openid_identifier', None)
        username = request.REQUEST.get('username', None)

        # process errors from openid authentication
        if request.path == self.url2:

            if request.method=='POST' and not request.user.is_authenticated():
                if response.status_code == 500:
                    if 'OpenID discovery error' in response.content:
                        return HttpResponseRedirect(reverse('openid-login')+"?message2=openid_discovery_error&next=%s&openid=%s" % (next, openid_identifier) )

        # process errors from standard authentication
        elif request.path == self.url1:

            if request.method=='POST' and not request.user.is_authenticated():
                return HttpResponseRedirect(reverse('login')+"?message1=login_failed&next=%s&username=%s" % (next, username) )

        return response
