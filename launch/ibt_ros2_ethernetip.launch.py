from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument


def generate_launch_description():

    ns = LaunchConfiguration('ns')
    ip = LaunchConfiguration('ip')

    declare_namespace = DeclareLaunchArgument('ns', default_value='sick_gateway', description='Namespace for the node')
    declare_ip = DeclareLaunchArgument(
        'ip', default_value='192.168.250.250', description='IP address of the device')

    node = Node(
        package='ibt_ros2_ethernetip',
        executable='ibt_ros2_ethernetip',
        name='ibt_ros2_ethernetip_node',
        namespace=ns,
        output='screen',
        emulate_tty=True,
        parameters=[
                {'hostname': ip},
        ]
    )

    return LaunchDescription([
        declare_ip,
        declare_namespace,

        node
    ])
