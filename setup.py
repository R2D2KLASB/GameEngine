from setuptools import setup

package_name = 'game_engine'
Engine = 'game_engine/Engine'
Nodes = 'game_engine/Nodes'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name,Engine,Nodes],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='njenneboer',
    maintainer_email='njenneboer@todo.todo',
    description='GameEngine for BattleShip',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'start = game_engine.start:main',
            'test = game_engine.test:main'
        ],
    },
)
