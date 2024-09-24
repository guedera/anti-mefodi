import rclpy
from rclpy.node import Node
from rclpy.qos import ReliabilityPolicy, QoSProfile
from geometry_msgs.msg import Twist
from pacote_simulado.laser import Laser
from pacote_simulado.odom import Odom
import numpy as np
# Adicione aqui os imports necessários

class Fugitivo(Node,Laser,Odom): # Mude o nome da classe

    def __init__(self):
        super().__init__('fugitivo_node') # Mude o nome do nó
        Laser.__init__(self)
        Odom.__init__(self)

        self.timer = self.create_timer(0.25, self.control)

        self.state_machine = {
            'para': self.para,
            'ajusta': self.ajusta,
            'segue': self.segue,
        }

        # Inicialização de variáveis
        self.twist = Twist()
        self.robot_state = 'segue'
        #variaveis inicializadas no laser e no odom

        # Subscribers
        ## Coloque aqui os subscribers
        #inscrição feita no laser.py
        #inscrição feita no odom.py

        # Publishers
        ## Coloque aqui os publishers
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)

    def para(self):
        return
    
    def ajusta(self):
        erro = self.goal_yaw - self.yaw
        erro = np.arctan2(np.sin(erro), np.cos(erro))

        if erro > np.deg2rad(2):
            #vira esquerda
            self.twist.angular.z = 0.35
        elif erro < np.deg2rad(-2):
            #vira a direita
            self.twist.angular.z = -0.35
        else:
            self.robot_state = 'segue'

    
    def segue(self):
        self.twist.linear.x = 0.45

        #psaiu
        if (np.min(self.front) > 2) and (np.min(self.left) > 1) and (np.min(self.right) > 1):
            self.robot_state = 'para'

        #parede na frente
        if np.min(self.front) < 0.6:

            #parede na esquerda
            if (np.min(self.right) > 0.7) and (np.min(self.left) < 0.7):
                self.goal_yaw = self.yaw - np.pi/2

            #parede na direita
            if(np.min(self.right) < 0.7) and (np.min(self.left) > 0.7):
                self.goal_yaw = self.yaw + np.pi/2

            #deadand
            if (np.min(self.right) < 0.7) and (np.min(self.left) < 0.7):
                self.goal_yaw = self.yaw + np.pi
            
            #só tem parede na frente
            if (np.min(self.right) > 0.7) and (np.min(self.left) > 0.7):
                self.goal_yaw = self.yaw + np.pi/2
                
            self.robot_state = 'ajusta'
        
    def control(self):
        self.twist = Twist()
        print(f'Estado Atual: {self.robot_state}')
        self.state_machine[self.robot_state]()

        self.cmd_vel_pub.publish(self.twist)
        
            
def main(args=None):
    rclpy.init(args=args)
    ros_node = Fugitivo() # Mude o nome da classe

    rclpy.spin(ros_node)

    ros_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()