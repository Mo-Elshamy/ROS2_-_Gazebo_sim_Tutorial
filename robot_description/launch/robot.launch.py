import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch.actions import AppendEnvironmentVariable
from launch_ros.actions import Node
from math import radians

def generate_launch_description():

    #setup project path
    pkg_description = get_package_share_directory('robot_description')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    bridge_params = os.path.join(pkg_description,'params','ros_bridge.yaml')
    
    #load SDF file from description pkg (sdformat_pkg should be installed)
    sdf_file = os.path.join(pkg_description, 'models' , 'waffle','model.sdf' )
    with open(sdf_file, 'r') as infp:
        robot_desc = infp.read()
    
    #set enviroment path   
    set_env_vars_resources = AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        os.path.join(get_package_share_directory('robot_description'),
                     'models'))
    
       
    #setup to launch simulator and gazebo world
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim ,'launch', 'gz_sim.launch.py')),
        launch_arguments = {'gz_args': PathJoinSubstitution ([
            pkg_description,
            'worlds',
            'turtlebot3_world.sdf',
            # 'empty_world.sdf',
        ])}.items(),
    )

    
    #Spawn the robot into Gazebo
    spawn_robot_node = Node(
        package='ros_gz_sim',
        executable= 'create',
        arguments= [
            '-name', 'turtlebot3_waffle',
            '-topic', 'robot_description',
        ],
        output = 'screen'
    )
    
    
    #joint state publisher to publish joint state
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='both'
    )
    
    
    #takes the description and joint angels as input and publishes the 3D pose od the robot links
    robot_state_publisher_node = Node(
        package = 'robot_state_publisher',
        executable = 'robot_state_publisher',
        name = 'robot_state_publisher',
        output='both',
        parameters=[
            {'use_sime_time': True},
            {'robot_description': robot_desc},
        ]
    )
    
    
    #bridge ros topic and gazebo meesages 
    bridge = Node(
        package = 'ros_gz_bridge',
        executable = 'parameter_bridge',
        parameters = [{
            'config_file': bridge_params,
            'qos_overrides./tf_static.publisher.durability': 'transient_local',
        }],
        output = 'screen',
    )    

    start_gazebo_ros_image_bridge_cmd = Node(
        package='ros_gz_image',
        executable='image_bridge',
        arguments=['/camera/image_raw'],
        output='screen',
    )
    
    # Rviz2
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        name='sim_rviz2',
        arguments=['-d' + os.path.join(pkg_description, 'rviz', 'rviz.rviz')]
    )
           
    
    return LaunchDescription([
        gz_sim,
        spawn_robot_node,
        robot_state_publisher_node,
        joint_state_publisher_node,
        bridge,
        start_gazebo_ros_image_bridge_cmd,
        set_env_vars_resources,
        rviz_node,
    ])
    
    
    
    

