import rclpy
from rclpy.node import Node
from ibt_ros2_interfaces.srv import GetAttrAll
import json

class SickFlexySoftReader(Node):
    def __init__(self):
        super().__init__('sick_flexysoft_reader')
        self.cli = self.create_client(GetAttrAll, '/sick_gateway/readInput')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Servizio non disponibile, attendo...')
        self.req = GetAttrAll.Request()
        self.req.clas = 0x72
        self.req.instance = 1

        # read from file json and load into signals_map
        with open('/home/mattia/ibt_ros2_ethernetip/test/mapping.json', 'r') as f:
            self.signals_map = json.load(f)["DigitalSignals"]

        self.timer = self.create_timer(0.5, self.call_service)

    def call_service(self):
        self.future = self.cli.call_async(self.req)
        self.future.add_done_callback(self.handle_response)

    def handle_response(self, future):
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().error(f'Chiamata servizio fallita: {e}')
            return

        # response.result è una lista di interi (bytes)
        buffer = bytes(response.result)

        # Legge i bit dei segnali di interesse
        self.get_logger().info(f"--- Ricevuto buffer di {len(buffer)} bytes ---")
        for name in self.signals_map:
            byte_idx = self.signals_map[name]["byteIndex"]
            bit_idx = self.signals_map[name]["bitIndex"]
            if byte_idx >= len(buffer):
                self.get_logger().warn(f"Byte index {byte_idx} fuori range per segnale {name}")
                continue
            byte_value = buffer[byte_idx]
            bit_value = (byte_value >> bit_idx) & 1
            self.get_logger().info(f"{name}: {bit_value}")


def main(args=None):
    rclpy.init(args=args)
    node = SickFlexySoftReader()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
