from setuptools import setup, find_packages

setup(
    name='geospatial_rd_analysis',
    version='0.0.1',
    description='A package that performs geospatial operations',
    author='Jaime Polanco-Jimenez',
    author_email='jaime.polanco@javeriana.edu.co',
    packages=find_packages(),
    install_requires=['numpy', 'geopandas>=0.9.0', 'shapely>=1.7.0'  ],
    entry_points={'console_scripts': ['my_function=geospatial_rd_analysis.rd_distance:spatial_analysis']},
)
