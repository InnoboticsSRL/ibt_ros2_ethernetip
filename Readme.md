# Sick FlexySoft Ethernet IP

ROS 2 packages for Sick EthernetIP Gateway FX0-GENT00000

## How it works
```bash
ros2 service call /readInput awtube_interfaces/srv/GetAttrAll "clas: 0x72
instance: 1"
```
```bash
ros2 service call /setOutput awtube_interfaces/srv/SetAttrAll "clas: 0x72
instance: 1  
data:
- 255
- 0
- 0
- 0
- 0
- 0
- 0
- 0
- 0
- 0"
```

## Registers
![Input](./img/Input.png)

![Output](./img/Output.png)