Gazeb set up

package.xml file :

```
<build_depend>ros_gz_sim</build_depend>
<exec_depend>ros_gz_sim</exec_depend>

```

Cmakelist.txt

```
find_package(ros_gz_sim REQUIRED)

ament_target_dependencies(
  your_executable_target_name
  ros_gz_sim
)

```



**GZ_SIM_RESOURCE_PATH**

```shell
export GZ_SIM_RESOURCE_PATH="PATH/models"
```

check the path

```
echo $GZ_SIM_RESOURCE_PATH
```



install bridges:

```
ros_gz_image
ros_gz_bridge
```



to use the sdf file without need for urdf file install the following pkgs

```
sudo apt install ros-humble-sdformat-urdf

```



References:

1- https://www.youtube.com/watch?v=KVe2u_2igkc

2- https://www.youtube.com/watch?v=fH4gkIFZ6W8

4- https://github.com/joshnewans/articubot_one/commit/e8a355fe8eb52c5a40a5240347bc204350a61266#diff-65ffb387cac03394885d419fc3bc09dc5dbd26776bb60a01fba0de06399011ac

3- https://gazebosim.org/docs/latest/migrating_gazebo_classic_ros2_packages/
