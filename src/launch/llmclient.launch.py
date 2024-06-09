from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='llm_chat2',
            namespace='llm_chat2',
            executable='client',
            name='client',
            arguments=['-message','hello']
        )
    ])