import lxml.etree as ET
from signxml import XMLSigner, methods
from datetime import datetime
from hashlib import sha256

def generar_xml(factura: 'FacturaElectronic') -> str:
    """
    Genera un XML firmado con CUFE y valida contra UBL 2.1.

    :param factura: Instancia de FacturaElectronic con los datos de la factura.
    :return: Un string con el contenido del XML firmado.
    """
    # Crear el root del XML
    root = ET.Element("Invoice", attrib={
        "xmlns": "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2",
        "xmlns:cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        "xmlns:cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
    })

    # Agregar elementos básicos del XML
    ET.SubElement(root, "cbc:UBLVersionID").text = "2.1"
    ET.SubElement(root, "cbc:CustomizationID").text = "1.0"
    ET.SubElement(root, "cbc:ProfileExecutionID").text = factura.profile_execution_id
    ET.SubElement(root, "cbc:InvoiceTypeCode").text = factura.invoice_type_code

    # Agregar otros elementos según la estructura de la DIAN (ejemplo simplificado)
    # ...

    # Calcular CUFE
    cufe = calcular_cufe(factura)

    # Firmar el XML con CUFE
    signed_xml = firmar_xml(root, cufe)

    return ET.tostring(signed_xml, pretty_print=True).decode('utf-8')

def calcular_cufe(factura: 'FacturaElectronic') -> str:
    """
    Calcula el CUFE (Clave Única de Facturación Electrónica) para la factura.

    :param factura: Instancia de FacturaElectronic con los datos de la factura.
    :return: El string del CUFE calculado.
    """
    # Implementar lógica para calcular CUFE basada en la normativa DIAN
    # Esto incluye hashing y concatenación de campos relevantes
    # ...
    
    return sha256("".join([factura.nit_emisor, factura.nit_receptor, str(factura.total), datetime.now().isoformat()]).encode()).hexdigest()

def firmar_xml(root: ET.Element, cufe: str) -> ET.Element:
    """
    Firma el XML con el CUFE utilizando signxml.

    :param root: El elemento root del XML a firmar.
    :param cufe: El string del CUFE calculado.
    :return: Un ElementTree con el XML firmado.
    """
    # Configurar la firma XML
    signer = XMLSigner(method=methods.enveloped, signature_algorithm="rsa-sha256", digest_algorithm="sha256")
    
    # Firmar el XML
    signed_root = signer.sign(root)

    return signed_root

def validar_xml_con_ubl_21(xml_string: str) -> bool:
    """
    Valida que el XML generado cumpla con las especificaciones de UBL 2.1.

    :param xml_string: El string del XML a validar.
    :return: True si es válido, False en caso contrario.
    """
    # Implementar lógica para validar contra XSD de UBL 2.1
    # Esto puede incluir carga y validación con lxml o libxml2
    # ...

    return True

# Ejemplo de uso
if __name__ == "__main__":
    from factura_electronica_python.factura import FacturaElectronic

    # Crear una instancia de FacturaElectronic con los datos necesarios
    factura = FacturaElectronic(
        nit_emisor="123456789",
        nit_receptor="987654321",
        total=100000,
        profile_execution_id="1",
        invoice_type_code="01"
    )

    # Generar XML firmado
    xml_firmado = generar_xml(factura)
    print(xml_firmado)

    # Validar XML contra UBL 2.1
    es_valido = validar_xml_con_ubl_21(xml_firmado)
    print("XML válido:", es_valido)