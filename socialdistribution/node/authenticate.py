import base64

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from author.models import Author

class AuthenticateCheck:
    def process_request(self, request):
        '''
        This is a helper function used by 'basicauth' that determines if
        they have provided proper http-authorization. It
        returns the json requested, otherwise responding with a 401.
        '''
        if not request.path.startswith('/api'):
            return

        while(1):
            if 'HTTP_AUTHORIZATION' in request.META:
                auth = request.META['HTTP_AUTHORIZATION'].split()
                if len(auth) == 2:
                    # NOTE: We are only support basic authentication for now.
                    #
                    if auth[0].lower() == "basic":
                        try:
                            user, host, passwd = base64.b64decode(auth[1]).split(':')
                        except:
                            break

                    if passwd != "team6":
                        break

                    #Todo, authenticate the host
                
                    #authenticate the user, else make a new account
                    if len(User.objects.filter(username=user+" "+host)) > 0:
                        request.user = authenticate(username=user+" "+host, password=passwd)
                    else:
                        user = User.objects.create_user(username=user+" "+host,
                                                password=passwd)
                        author = Author.objects.create(user=user, host=host)
                        request.user = authenticate(username=user, password=passwd)
                    return 
                else:
                    break

        # Either they did not provide an authorization header or
        # something in the authorization attempt failed. Send a 401
        # back to them to ask them to authenticate.
        #
        return HttpResponse('{"message": "Authentication Failed"}', \
            content_type='application/json', status=401)