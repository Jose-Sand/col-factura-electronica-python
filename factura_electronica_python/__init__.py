# factura_electronica_python/__init__.py

from .factura import FacturaElectronica
from .firmado import firmar_xml_con_cufe
from .validacion import validar_contrato_ubl_21
from .transmision import transmitir_factura_al_hub_dian

__all__ = [
    'FacturaElectronica',
    'firmar_xml_con_cufe',
    'validar_contrato_ubl_21',
    'transmitir_factura_al_hub_dian'
]
```

```python
# factura_electronica_python/factura.py

from lxml import etree
import logging

logger = logging.getLogger(__name__)

class FacturaElectronica:
    """
    Clase que representa una factura electrónica y permite su generación en formato XML.
    
    Atributos:
        emisor (dict): Información del emisor de la factura.
        receptor (dict): Información del receptor de la factura.
        items (list of dict): Lista de items o productos en la factura.
    """
    
    def __init__(self, emisor, receptor, items):
        self.emisor = emisor
        self.receptor = receptor
        self.items = items
    
    def generar_xml(self):
        """
        Genera el XML de la factura electrónica.
        
        Returns:
            str: El contenido del XML generado.
        """
        # Creación del root del XML
        factura_root = etree.Element('Invoice', nsmap={
            'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
            'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'
        })
        
        # Agregar información del emisor
        emisor_element = etree.SubElement(factura_root, 'cac:AccountingSupplierParty')
        party_identification = etree.SubElement(emisor_element, 'cac:PartyIdentification')
        id_element = etree.SubElement(party_identification, 'cbc:ID', schemeName='NIT')
        id_element.text = self.emisor['nit']
        
        # Agregar información del receptor
        receptor_element = etree.SubElement(factura_root, 'cac:AccountingCustomerParty')
        party_identification = etree.SubElement(receptor_element, 'cac:PartyIdentification')
        id_element = etree.SubElement(party_identification, 'cbc:ID', schemeName='NIT')
        id_element.text = self.receptor['nit']
        
        # Agregar items
        for item in self.items:
            item_line = etree.SubElement(factura_root, 'cac:InvoiceLine')
            line_extension_amount = etree.SubElement(item_line, 'cbc:LineExtensionAmount', currencyID='COP')
            line_extension_amount.text = str(item['precio_unitario'] * item['cantidad'])
            
            description = etree.SubElement(item_line, 'cbc:Description')
            description.text = item['descripcion']
        
        # Convertir el XML a string
        xml_string = etree.tostring(factura_root, pretty_print=True, encoding='utf-8', xml_declaration=True)
        return xml_string.decode('utf-8')
```

```python
# factura_electronica_python/firmado.py

from signxml import xmldsig
import logging

logger = logging.getLogger(__name__)

def firmar_xml_con_cufe(xml_content, certificado_path, clave_privada_path):
    """
    Firma el XML de la factura electrónica con CUFE.
    
    Args:
        xml_content (str): Contenido del XML a firmar.
        certificado_path (str): Ruta al archivo del certificado digital.
        clave_privada_path (str): Ruta al archivo de la clave privada.
        
    Returns:
        str: El contenido del XML firmado.
    """
    try:
        # Crear objeto etree desde el contenido XML
        tree = etree.fromstring(xml_content.encode('utf-8'))
        
        # Cargar certificado y clave privada
        with open(certificado_path, 'rb') as cert_file:
            cert_data = cert_file.read()
        with open(clave_privada_path, 'rb') as key_file:
            key_data = key_file.read()
        
        # Firmar el XML
        signed_xml = xmldsig.sign(tree, 
                                  sign_algorithm='http://www.w3.org/2001/04/xmldsig-more#rsa-sha256',
                                  digest_algorithm='http://www.w3.org/2001/04/xmlenc#sha256',
                                  key=key_data,
                                  cert=cert_data)
        
        # Convertir el XML firmado a string
        signed_xml_string = etree.tostring(signed_xml, pretty_print=True, encoding='utf-8', xml_declaration=True)
        return signed_xml_string.decode('utf-8')
    except Exception as e:
        logger.error(f"Error al firmar el XML: {str(e)}")
        raise
```

```python
# factura_electronica_python/validacion.py

import os
from lxml import etree
import logging

logger = logging.getLogger(__name__)

def validar_contrato_ubl_21(xml_content, schema_path):
    """
    Valida el XML de la factura electrónica contra el contrato UBL 2.1.
    
    Args:
        xml_content (str): Contenido del XML a validar.
        schema_path (str): Ruta al archivo del esquema XSD.
        
    Returns:
        bool: True si el XML es válido, False en caso contrario.
    """
    try:
        # Cargar el esquema
        with open(schema_path, 'rb') as schema_file:
            schema_doc = etree.parse(schema_file)
            schema = etree.XMLSchema(schema_doc)
        
        # Parsear el XML a validar
        xml_doc = etree.fromstring(xml_content.encode('utf-8'))
        
        # Validar el XML contra el esquema
        if not schema.validate(xml_doc):
            logger.error(f"Errores de validación: {schema.error_log}")
            return False
        
        return True
    except Exception as e:
        logger.error(f"Error al validar el XML: {str(e)}")
        raise
```

```python
# factura_electronica_python/transmision.py

import requests
import logging

logger = logging.getLogger(__name__)

def transmitir_factura_al_hub_dian(xml_content, url_hub):
    """
    Transmite el XML de la factura electrónica al hub habilitado de la DIAN.
    
    Args:
        xml_content (str): Contenido del XML firmado a transmitir.
        url_hub (str): URL del endpoint del hub habilitado.
        
    Returns:
        dict: Respuesta de la transmisión en formato JSON.
    """
    try:
        # Preparar los datos para enviar
        headers = {'Content-Type': 'application/xml'}
        response = requests.post(url_hub, data=xml_content.encode('utf-8'), headers=headers)
        
        # Verificar la respuesta del servidor
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error en la transmisión: {response.status_code} - {response.text}")
            raise Exception(f"Error en la transmisión: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Error al transmitir el XML: {str(e)}")
        raise