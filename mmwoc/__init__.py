'''
import os
from twisted.application import service, internet
from twisted.web import static, server
from mmwoc import mmwoc

def getWebService():
    """
    Return a service suitable for creating an application object.

    This service is a simple web server that serves files on port 8080 from
    underneath the current working directory.
    """
    # create a resource to serve static files
    fileServer = server.Site(mmwoc.mmwoc())
    return internet.TCPServer(8080, fileServer)

# this is the core part of any tac file, the creation of the root-level
# application object
application = service.Application("Watmedia")

# attach the service to its parent application
service = getWebService()
service.setServiceParent(application)
'''