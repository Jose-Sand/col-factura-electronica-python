```markdown
# SDK de Facturación Electrónica para Python

## Descripción

Este proyecto proporciona un SDK de facturación electrónica para Python, diseñado para resolver la falta de herramientas actualizadas y con tipos TypeScript para la facturación electrónica DIAN. El SDK incluye funcionalidades clave para generar XML firmados con CUFE, validar contra UBL 2.1 y transmitir las facturas al hub habilitado por la DIAN.

## Badges

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- **Generación automática de XML firmado con CUFE**: Crea archivos XML que cumplen con los requisitos de la DIAN y están correctamente firmados.
- **Validación contra UBL 2.1**: Asegura que los documentos generados sean compatibles con el estándar UBL 2.1.
- **Transmisión al hub habilitado de la DIAN**: Envía las facturas electrónicas directamente al sistema de la DIAN.

## Instalación

Para instalar el SDK, puedes utilizar pip:

```bash
pip install .
```

o desde un archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Uso con Ejemplos

### Generar XML Firmado

```python
from factura_electronica_python import generar_xml

# Datos de la factura
factura_data = {
    "tipo": "Factura",
    "numero": "123456789",
    # Otros datos necesarios para la factura
}

xml_firmado = generar_xml(factura_data)
print(xml_firmado)
```

### Transmitir Factura

```python
from factura_electronica_python import transmitir_factura

# Ruta del archivo XML firmado
ruta_xml = "factura.xml"

transmitir_factura(ruta_xml)
```

## Estructura del Proyecto

- `factura_electronica_python/__init__.py`: Inicialización del módulo.
- `factura_electronica_python/generar_xml.py`: Contiene la lógica para generar XML firmado.
- `factura_electronica_python/transmitir_factura.py`: Maneja la transmisión de facturas al hub habilitado.
- `tests/test_generar_xml.py`: Pruebas unitarias para la generación de XML.
- `tests/test_transmitir_factura.py`: Pruebas unitarias para la transmisión de facturas.
- `requirements.txt`: Lista de dependencias necesarias.
- `setup.py`: Script de instalación del paquete.

## Contribución

Si deseas contribuir al proyecto, puedes seguir estos pasos:

1. Fork el repositorio.
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -m "Añade nueva funcionalidad"').
4. Pushea tus cambios (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Para más detalles, consulta el archivo [LICENSE](LICENSE).

---

**Nota**: Este SDK ha sido desarrollado para facilitar la integración de facturación electrónica en aplicaciones Python, especialmente dirigidas al mercado latinoamericano y colombiano.
```