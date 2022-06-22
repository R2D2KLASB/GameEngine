# Game Engine

Voor de codestandaard, klik [hier](https://github.com/R2D2KLASB/Info/blob/main/CodeStandaard.md)

# Install

The install.sh script should download automatically the dependencies and build the ros2 package.

```
cd "PATH-TO-ROS2-ENVIROMENT/src"
git clone git@github.com:R2D2KLASB/Beeldverwerking.git
cd GameEngine
./install.sh
. ../../install/setup.bash
```


# Run

LOCAL( No ROS2 ):
```
ros2 run game_engine local console console
ros2 run game_engine local ai ai
ros2 run game_engine local console ai
ros2 run game_engine local ai console
```
LAN( Over ROS2 ):
```
ros2 run game_engine lan console A
ros2 run game_engine lan console B
ros2 run game_engine lan ai A
ros2 run game_engine lan ai B
```

Don't forget to source your ROS 2 installation before running an package!
```
. ../../install/setup.bash
```
