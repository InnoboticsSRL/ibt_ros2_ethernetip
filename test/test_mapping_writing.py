import rclpy
from rclpy.node import Node
from ibt_ros2_interfaces.srv import SetAttrAll  
import asyncio

class SickFlexySoftWriter(Node):
    def __init__(self):
        super().__init__('sick_flexysoft_writer')
        self.cli = self.create_client(SetAttrAll, '/sick_gateway/setOutput')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Servizio SetAttrAll non disponibile, attendo...')

        # Parametri di classe e istanza
        self.clas = 0x72
        self.instance = 1
        self.data_buffer = bytearray(range(50))
        self.value_to_set = 0 

        self.timer = self.create_timer(1.0, self.send_next_chunk)

    def send_next_chunk(self):

        req = SetAttrAll.Request()
        req.clas = self.clas
        req.instance = self.instance
        req.data = [self.value_to_set] * 50

        self.value_to_set = not self.value_to_set

        self.future = self.cli.call_async(req)
        self.future.add_done_callback(self.handle_response)

    def handle_response(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'Response dal servizio: {response.result_message}')
        except Exception as e:
            self.get_logger().error(f'Chiamata servizio fallita: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = SickFlexySoftWriter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
