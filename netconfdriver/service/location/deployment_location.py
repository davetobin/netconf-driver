import logging
from ignition.utils.propvaluemap import PropValueMap
from ignition.locations.exceptions import InvalidDeploymentLocationError
from ignition.locations.utils import get_property_or_default
from netconfdriver.service.configuration.configuration import *

logger = logging.getLogger(__name__)

class NetConfDeploymentLocation:
    """
    Netconf deployment location

    Attributes:
      name (str): name of the location
    """

    HOST = 'host'
    PORT = 'port'
    PROPERTIES = 'properties'
    USERNAME = 'username'
    PASSWORD = 'password'
    TIMEOUT = 'timeout'

    @staticmethod
    def from_dict(dl_data):
        """
        Creates an Netconf deployment location to dictionary format

        Args:
            dl_data (dict): the deployment location data.
        Returns:
            an NetConfDeploymentLocation instance
        """
        properties = dl_data.get(NetConfDeploymentLocation.PROPERTIES)
        if properties is None:
            raise InvalidDeploymentLocationError(f'Deployment location Properties missing \'{NetConfDeploymentLocation.PROPERTIES}\' value')
        timeout = get_property_or_default(
            properties, NetConfDeploymentLocation.TIMEOUT, error_if_not_found=False)
        host = get_property_or_default(properties, NetConfDeploymentLocation.HOST, error_if_not_found=True)
        port = get_property_or_default(properties, NetConfDeploymentLocation.PORT, error_if_not_found=True)
        username = get_property_or_default(properties, NetConfDeploymentLocation.USERNAME, error_if_not_found=True)
        password = get_property_or_default(properties, NetConfDeploymentLocation.PASSWORD, error_if_not_found=True)
        kwargs = {}
        if timeout is not None:
            kwargs['timeout'] = timeout
        return NetConfDeploymentLocation(host, username, password, port, **kwargs)

    def __init__(self, host, username, password, port,**kwargs):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.kwargs = kwargs
        self.timeout = kwargs.get('timeout')

    def to_dict(self):
        """
        Produces a dictionary copy of the deployment location

        Returns:
            the deployment location configuration as a dictionary. For example:

            {
                'name': 'Test',
                'properties': {
                    ...
                }
            }
        """
        return {
            NetConfDeploymentLocation.HOST: self.host,
            NetConfDeploymentLocation.USERNAME: self.username,
            NetConfDeploymentLocation.PASSWORD: self.password,
            NetConfDeploymentLocation.PORT: self.port,
            NetConfDeploymentLocation.TIMEOUT: self.timeout,
        }

    def connect(self,package_properties,default_operation,rsa_key_path):
        response = Configuration.netconf_connect(self.host, self.port, self.username, self.password, rsa_key_path, self.kwargs)
        Configuration.netconf_edit(response,package_properties,default_operation)
        Configuration.netconf_disconnect(response)

    def close(self):
        pass