import struct
import rclpy
from rclpy.node import Node
from pycomm3 import CIPDriver
from ibt_ros2_interfaces.srv import GetAttrAll, SetAttrAll

class SickFlexySoftNode(Node):

    def __init__(self):
        super().__init__('ibt_ethernetip')
        self.declare_parameters(
            namespace='',
            parameters=[
                ('hostname', ''),
            ])
        self.hostname = self.get_parameter('hostname').get_parameter_value().string_value
        self.setOutput = self.create_service(SetAttrAll, 'setOutput', self.setOutputCallback)
        self.readInput = self.create_service(GetAttrAll, 'readInput', self.readInputCallback)
        self.get_logger().info("EtherNet node IP ready!")
    
    def setOutputCallback(self, request, response):
        byte_obj = struct.pack('B' * len(request.data), *request.data)
        try:
            with CIPDriver(self.hostname) as device:
                data = device.generic_message(
                    service=b'\x01',            # setAttrAll
                    class_code=request.clas,
                    instance=request.instance,
                    request_data=byte_obj
                )
                response.result_code = 0

        except Exception as e:
            self.get_logger().error(f"SetAttrAll error: {e}")
            response.result_code = 1
        return response

    def readInputCallback(self, request, response):
        try:

            with CIPDriver(self.hostname) as device:
                data = device.generic_message(
                    service=b'\x01',            # getAttrAll
                    class_code=request.clas,
                    instance=request.instance
                )
                response.result_code = 0
                response.result = list(data.value) if data.value is not None else []

        except Exception as e:
            self.get_logger().error(f"GetAttrAll error: {e}")
            response.result_code = 1
            response.result = []
        return response

def main(args=None):
    rclpy.init(args=args)

    node = SickFlexySoftNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()