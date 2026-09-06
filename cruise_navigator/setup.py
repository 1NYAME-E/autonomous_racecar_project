from setuptools import find_packages, setup

package_name = 'cruise_navigator'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch',
         ['launch/cruise_control.launch.py']), 
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='gloria.otieno@ashesi.edu.gh',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'wall_follower = cruise_navigator.wall_follower:main',
            'initial_turn = cruise_navigator.initial_turn:main',
        ],
    },
)
