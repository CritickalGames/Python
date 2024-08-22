from setuptools import setup, find_packages
#! pendiente de finalización. Preguntar a GPT como hacer un setup.py
setup(
    name='dividendos',  # Nombre de tu paquete
    version='0.1',       # Versión del paquete
    packages=find_packages(),  # Encuentra todos los paquetes automáticamente
    install_requires=[   # Lista de dependencias
        # 'numpy', 'requests', ... (si tienes dependencias externas)
    ],
    author='Zgtale',
    author_email='zgtale1@hotmail.com',
    description='Gestiona tus dividendos',
    long_description=open('README.md').read(),  # Contenido de README.md
    long_description_content_type='text/markdown',
    url='https://github.com/CritickalGames/Python/tree/main/dividendos',  # URL del proyecto (si tienes)
    classifiers=[        # Clasificadores de PyPI
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',  # Versión mínima de Python requerida
)