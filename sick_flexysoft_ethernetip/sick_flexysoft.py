import ethernetip
import socket
import struct
import rclpy
from rclpy.node import Node
from awtube_interfaces.srv import GetAttrAll, SetAttrAll

class SickFlexySoftNode(Node):

    def __init__(self):
        super().__init__('sick_flexysoft')
        self.declare_parameters(
            namespace='',
            parameters=[
                ('hostname', ''),
                ('broadcast', '')
            ])
        self.hostname = self.get_parameter('hostname').get_parameter_value().string_value
        self.broadcast = self.get_parameter('broadcast').get_parameter_value().string_value
        self.setOutput = self.create_service(SetAttrAll, 'setOutput', self.setOutputCallback)
        self.readInput = self.create_service(GetAttrAll, 'readInput', self.readInputCallback)

        self.initEthIP()
    
    def setOutputCallback(self, request, response):
        byte_obj = struct.pack('B' * len(request.data), *request.data)
        response.result_code = self.C1.setAttrAll(request.clas, request.instance, byte_obj)[0]
        return response
        
    def readInputCallback(self, request, response):
        r = self.C1.getAttrAll(request.clas, request.instance)
        response.result_code = r[0]
        response.result = r[1]
        return response
    
    def initEthIP(self):
        self.EIP = ethernetip.EtherNetIP(self.hostname)
        self.C1 = self.EIP.explicit_conn(self.hostname)
        listOfNodes = self.C1.scanNetwork(self.broadcast, 5)
        print("Found ", len(listOfNodes), " nodes")
        for node in listOfNodes:
            name = node.product_name.decode()
            sockinfo = ethernetip.SocketAddressInfo(node.socket_addr)
            ip = socket.inet_ntoa(struct.pack("!I", sockinfo.sin_addr))
            print(ip, " - ", name)

        pkt = self.C1.listID()
        if pkt is not None:
            print("Product name: ", pkt.product_name.decode())

        pkt = self.C1.listServices()
        print("ListServices:", str(pkt))
        self.C1.registerSession()


def main(args=None):
    rclpy.init(args=args)

    node = SickFlexySoftNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()