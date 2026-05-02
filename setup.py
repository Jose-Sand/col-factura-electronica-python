# setup.py

from setuptools import setup, find_packages

setup(
    name='factura-electronica-python',
    version='0.1.0',
    description='SDK para facturación electrónica en Colombia con CUFE, UBL 2.1 y transmisión al hub DIAN',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/factura-electronica-python',
    author='Tu Nombre',
    author_email='tuemail@example.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='factura electronica dian cufe ubl2.1 transmision',
    packages=find_packages(),
    install_requires=[
        'lxml>=4.6.0',
        'signxml>=2.7.0',
        'requests>=2.25.1'
    ],
    extras_require={
        'dev': ['pytest', 'coverage'],
    },
    package_data={
        'factura_electronica_python': ['data/*.xsd', 'data/*.pem'],
    },
    python_requires='>=3.7, <4',
)