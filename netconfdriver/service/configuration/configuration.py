import sys
import logging
from ncclient import manager
logger = logging.getLogger(__name__)
    
class NetconfConfigError(Exception):
    pass

class Configuration():
    def netconf_connect(host, port, user, password,rsa_key_path,kwargs):
        logger.debug(f'host:{host},port:{port},user:{user},password:{password},rsa_key_path:{rsa_key_path},kwargs:{kwargs}')
        try:
            for key in kwargs:
                key = kwargs[key]
            conn =  manager.connect(host=host,
                                port=port,
                                username=user,
                                password=password,
                                key_filename=rsa_key_path,
                                hostkey_verify=False,
                                **kwargs)
            logger.debug('Connected ...')
            return conn
        except Exception as e:
            logger.error('Unexpected exception {0}'.format(e))
            raise NetconfConfigError(str(e)) from e
        
    def netconf_edit(conn,package_properties,default_operation):
        try:
            edit_config_details = conn.edit_config(config=package_properties, target="running", default_operation=default_operation)
            logger.debug('config_details = %s', edit_config_details)
        except Exception as e:
            logger.error('Unexpected exception {0}'.format(e))
            raise NetconfConfigError(str(e)) from e
        
    def netconf_disconnect(conn):
        try:
            logger.debug('Close session...')
            conn.close_session()
        except Exception as e:
            logger.error('Unexpected exception {0}'.format(e))
            raise NetconfConfigError(str(e)) from e