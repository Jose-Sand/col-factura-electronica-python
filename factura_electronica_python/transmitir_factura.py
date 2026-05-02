# factura_electronica_python/transmitir_factura.py
import requests
from .generar_xml import generar_xml_firmado

def transmitir_factura(factura: FacturaElectronica, url_hub_dian: str) -> dict:
    """
    Transmite una factura electrónica al hub habilitado de la DIAN.

    :param factura: Instancia de FacturaElectronic con los datos de la factura.
    :param url_hub_dian: URL del endpoint del hub habilitado de la DIAN.
    :return: Respuesta JSON del servicio de transmisión.
    :raises ValueError: Si el XML no puede ser generado o firmado.
    :raises requests.exceptions.RequestException: Si ocurre un error durante la transmisión HTTP.
    """
    try:
        # Generar XML firmado con CUFE
        xml_firmado = generar_xml_firmado(factura)
        
        # Preparar headers para la transmisión
        headers = {
            'Content-Type': 'application/xml',
            'Authorization': f'Bearer {factura.token_autorizacion}'
        }
        
        # Realizar la petición POST al hub de la DIAN
        response = requests.post(url_hub_dian, data=xml_firmado, headers=headers)
        response.raise_for_status()  # Lanzar excepción si hay un error HTTP
        
        # Devolver la respuesta JSON del servicio
        return response.json()
    
    except ValueError as ve:
        raise ValueError("Error al generar o firmar el XML: {ve}".format(ve=ve))
    except requests.exceptions.RequestException as re:
        raise requests.exceptions.RequestException(f"Error de transmisión a la DIAN: {re}")