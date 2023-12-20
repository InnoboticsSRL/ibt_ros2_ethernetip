from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='sick_flexysoft_ethernetip',
            executable='sick_flexysoft',
            name='sick_flexysoft',
            output='screen',
            emulate_tty=True,
            parameters=[
                {'hostname': '192.168.250.251'},
                {'broadcast': '192.168.255.255'}
            ]
        )
    ])