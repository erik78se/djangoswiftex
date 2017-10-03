from django.http import HttpResponse
from django.http import JsonResponse
import logging
from swiftclient.service import SwiftService, SwiftError


#export ST_AUTH_VERSION=3
#export OS_USERNAME=testuser
#export OS_USER_DOMAIN_NAME=admin_domain
#export OS_PASSWORD=1234
#export OS_PROJECT_NAME=admin
#export OS_PROJECT_DOMAIN_NAME=admin_domain
#export OS_AUTH_URL=http://192.168.1.173:5000/v3


logging.basicConfig(level=logging.ERROR)
logging.getLogger("requests").setLevel(logging.CRITICAL)
logging.getLogger("swiftclient").setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)


def index_view(request):
    return HttpResponse("Hello, world. You're at the basicfrontend app index.")

def list_view(request):
    # lowercase important
    localconfig = { 'st_auth_version': 3,
                    'os_user_domain_name': 'admin_domain',
                    'os_username': 'testuser',
                    'os_password': '1234',
                    'os_auth_url': 'http://192.168.1.173:5000/v3'}

    container = 'testcontainer'
    minimum_size = 10 * 1024 ** 2
    items = []
    with SwiftService(options=localconfig) as swift:
        try:
            list_parts_gen = swift.list(container=container)
            for page in list_parts_gen:
                if page["success"]:
                    for item in page["listing"]:

                        i_size = int(item["bytes"])
                        if i_size > minimum_size:
                            i_name = item["name"]
                            i_etag = item["hash"]
                            print(
                                "%s [size: %s] [etag: %s]" %
                                (i_name, i_size, i_etag)
                            )
                            items.append((i_name, i_size, i_etag))
                else:
                    raise page["error"]

        except SwiftError as e:
            logger.error(e.value)

    print(items)
    return JsonResponse(items, safe=False)



