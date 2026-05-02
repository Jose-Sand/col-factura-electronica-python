# tests/test_transmitir_factura.py

import unittest
from unittest.mock import patch, Mock
from factura_electronica_python.transmitir_factura import transmitir_factura

class TestTransmitirFactura(unittest.TestCase):

    @patch('requests.post')
    def test_transmitir_factura_exitoso(self, mock_post):
        # Datos de prueba
        xml_firmado = b'<xml>...</xml>'
        url_hub_dian = 'https://hub.dian.gov.co'
        headers = {
            'Content-Type': 'application/xml',
            'Authorization': 'Bearer token_de_autenticacion'
        }
        
        # Respuesta simulada del hub DIAN
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = {'message': 'Factura transmitida exitosamente'}
        
        mock_post.return_value = response_mock
        
        # Llamada a la función de transmisión
        resultado, mensaje = transmitir_factura(xml_firmado, url_hub_dian, headers)
        
        # Verificaciones
        self.assertTrue(resultado)
        self.assertEqual(mensaje, 'Factura transmitida exitosamente')
        mock_post.assert_called_once_with(url_hub_dian, data=xml_firmado, headers=headers)

    @patch('requests.post')
    def test_transmitir_factura_error(self, mock_post):
        # Datos de prueba
        xml_firmado = b'<xml>...</xml>'
        url_hub_dian = 'https://hub.dian.gov.co'
        headers = {
            'Content-Type': 'application/xml',
            'Authorization': 'Bearer token_de_autenticacion'
        }
        
        # Respuesta simulada del hub DIAN
        response_mock = Mock()
        response_mock.status_code = 400
        response_mock.json.return_value = {'message': 'Error en la transmisión'}
        
        mock_post.return_value = response_mock
        
        # Llamada a la función de transmisión
        resultado, mensaje = transmitir_factura(xml_firmado, url_hub_dian, headers)
        
        # Verificaciones
        self.assertFalse(resultado)
        self.assertEqual(mensaje, 'Error en la transmisión')
        mock_post.assert_called_once_with(url_hub_dian, data=xml_firmado, headers=headers)

    @patch('requests.post')
    def test_transmitir_factura_excepcion(self, mock_post):
        # Datos de prueba
        xml_firmado = b'<xml>...</xml>'
        url_hub_dian = 'https://hub.dian.gov.co'
        headers = {
            'Content-Type': 'application/xml',
            'Authorization': 'Bearer token_de_autenticacion'
        }
        
        # Simulación de excepción
        mock_post.side_effect = requests.RequestException('Error de conexión')
        
        # Llamada a la función de transmisión
        resultado, mensaje = transmitir_factura(xml_firmado, url_hub_dian, headers)
        
        # Verificaciones
        self.assertFalse(resultado)
        self.assertEqual(mensaje, 'Error de conexión')
        mock_post.assert_called_once_with(url_hub_dian, data=xml_firmado, headers=headers)

if __name__ == '__main__':
    unittest.main()