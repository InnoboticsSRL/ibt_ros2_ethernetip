from setuptools import setup
import os
from glob import glob

package_name = 'ibt_ros2_ethernetip'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*launch.[pxy][yma]*'))
    ],
    install_requires=['setuptools','ethernetip'],
    zip_safe=True,
    maintainer='Mattia Dei Rossi',
    maintainer_email='mattia.deirossi@innobotics.it',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ibt_ros2_ethernetip = ibt_ros2_ethernetip.ibt_ros2_ethernetip_node:main'
        ],
    },
)
