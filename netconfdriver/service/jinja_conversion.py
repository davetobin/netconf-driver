import os
import logging
from ignition.service.templating import ResourceTemplateContextService, Jinja2TemplatingService
from tempfile import NamedTemporaryFile

logger = logging.getLogger(__name__)

# TEMPLATE_PATH = "/netconf-descriptor1/Lifecycle/netconf/template/"
TEMPLATE_PATH = "/template/"
DEFAULT_OPERATION = "merge"

def from_pkg(resource_properties, driver_files, method_name):
    try:
        template_path = driver_files.root_path
        template_path = driver_files.root_path + TEMPLATE_PATH
        template_name = os.listdir(template_path)
        for template in template_name:
            split_template = template.split('.')[0].lower()
            if(split_template == method_name):
                template_name = template
        template_path = template_path + template_name
        f = open(template_path, "r")
        content = f.read()
        resource_context_service = ResourceTemplateContextService()
        templating_service = Jinja2TemplatingService()
        return templating_service.render(content,
                resource_context_service.build(system_properties={}, resource_properties=resource_properties,
                                           request_properties={}, deployment_location={}))
    except Exception as e:
        return None

def to_string(resource_properties):
    try:
        value = None
        default = DEFAULT_OPERATION
        for item in list(resource_properties.keys()):
            if item == 'defaultOperation':
                value = resource_properties[item]
        logging.info('value: %s', value)
        if value == "" or value is None:
            return default
        else:
            return value
    except Exception as e:
        return None
    
def to_rsa_path(resource_properties):
    try:
        key_property_processor = KeyPropertyProcessor(resource_properties)
        key_path = key_property_processor.process_key_properties()
        if key_path is not None:
            return key_path
        elif key_path is None:
            return None
    except Exception as e:
        logger.error('Unexpected exception {0}'.format(e))
        return None
    
class KeyPropertyProcessor():
    def __init__(self, resource_properties):
        self.properties = resource_properties
        self.key_files = []

#   Process (input) key properties by writing the private key out to a file in tmp

    def process_key_properties(self):
        key_path = self.process_keys(self.properties)
        return key_path

    def process_keys(self, properties):
        properties = self.properties 
        for prop in properties.get_keys().items_with_types():
            key_path = self.write_private_key(properties, prop[0], prop[1])
            return key_path

    def write_private_key(self, properties, key_prop_name, private_key):
        
        with NamedTemporaryFile(delete=False, mode='w') as private_key_file:
            
            private_key_value = private_key.get('privateKey', None)
            private_key_file.write(private_key_value)
            private_key_file.flush()
            self.key_files.append(private_key_file)
            return private_key_file.name

#   Remove any private key files generated during the run.
  
    def clear_key_files(self):
        for key_file in self.key_files:
            logger.debug('Removing private key file {0}'.format(key_file.name))
            os.unlink(key_file.name)