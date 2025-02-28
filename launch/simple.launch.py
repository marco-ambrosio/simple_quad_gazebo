import launch
import launch.actions
from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

import launch_ros.actions
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_share = FindPackageShare("simple_quad")

    gazebo = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource([FindPackageShare("gazebo_ros"), "/launch/gazebo.launch.py"])
    )

    robot_description = {
        "robot_description": launch.substitutions.Command(
            ["xacro ", PathJoinSubstitution([pkg_share, "urdf", "simple_quad.urdf.xacro"])]
        )
    }

    rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[robot_description],
    )

    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-entity", "simple_quad", "-topic", "robot_description", "-z", "0.25"],
        output="screen",
    )

    return LaunchDescription(
        [
            gazebo,
            rsp,
            spawn_entity,
        ]
    )
