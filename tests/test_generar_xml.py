# tests/test_generar_xml.py

import unittest
from factura_electronica_python.generar_xml import FacturaElectronic, generar_xml_firmado
from lxml import etree

class TestGenerarXML(unittest.TestCase):

    def setUp(self):
        # Datos de ejemplo para una factura electrónica
        self.datos_factura = {
            "NitEmisor": "123456789",
            "NombreEmisor": "Empresa Ejemplo",
            "NitReceptor": "987654321",
            "NombreReceptor": "Cliente Ejemplo",
            "Total": 100000,
            "FechaEmision": "2023-10-01T10:00:00"
        }

    def test_generar_xml(self):
        # Generar el XML firmado
        xml_firmado = generar_xml_firmado(self.datos_factura)
        
        # Parsear el XML firmado
        root = etree.fromstring(xml_firmado.encode('utf-8'))
        
        # Verificar que el elemento raíz sea Factura
        self.assertEqual(root.tag, "{http://www.dian.gov.co/contratos/facturaelectronica/v1}Factura")
        
        # Verificar la existencia de elementos importantes
        self.assertIsNotNone(root.find(".//{http://www.dian.gov.co/contratos/facturaelectronica/v1}NitEmisor"))
        self.assertIsNotNone(root.find(".//{http://www.dian.gov.co/contratos/facturaelectronica/v1}NombreEmisor"))
        self.assertIsNotNone(root.find(".//{http://www.dian.gov.co/contratos/facturaelectronica/v1}Total"))

    def test_validar_xml_ubl_2_1(self):
        # Generar el XML firmado
        xml_firmado = generar_xml_firmado(self.datos_factura)
        
        # Parsear el XML firmado
        root = etree.fromstring(xml_firmado.encode('utf-8'))
        
        # Validar contra el esquema UBL 2.1
        with open("factura_electronica_python/esquemas/UBL-Invoice-2.1.xsd", "rb") as xsd_file:
            xmlschema_doc = etree.parse(xsd_file)
            xmlschema = etree.XMLSchema(xmlschema_doc)
        
        self.assertTrue(xmlschema.validate(root), "El XML no cumple con el esquema UBL 2.1")

if __name__ == '__main__':
    unittest.main()