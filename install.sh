#!/bin/bash  
cd ../../
rosdep install -i --from-path src --rosdistro foxy -y
colcon build --packages-select game_engine