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

        try:
            self.device = CIPDriver(self.hostname)
        except:
            self.get_logger().error('Could not find EtherNetIP devices')
            rclpy.shutdown()
    
    def setOutputCallback(self, request, response):
        byte_obj = struct.pack('B' * len(request.data), *request.data)
        with CIPDriver(self.hostname) as device:
            data = device.generic_message(
                service=b'\x01',            # setAttrAll
                class_code=request.clas,
                instance=request.instance,
                request_data=byte_obj
            )
            response.error = data.error if data.error else ""
            return response 
        
    def readInputCallback(self, request, response):
        with CIPDriver(self.hostname) as device:
            data = device.generic_message(
                service=b'\x01',            # getAttrAll
                class_code=request.clas,
                instance=request.instance
            )
            response.error = data.error if data.error else ""
            response.result = data.value
            return response
       

def main(args=None):
    rclpy.init(args=args)

    node = SickFlexySoftNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()