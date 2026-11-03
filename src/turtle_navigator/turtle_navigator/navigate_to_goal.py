import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class TurtleNavigator(Node):
    def __init__(self):
        super().__init__('turtle_navigator')
        
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0
        
        self.goal_x = -2.0
        self.goal_y = 8.0
        
        self.timer = self.create_timer(0.1, self.control_loop)
        self.get_logger().info(f'目标已设定：({self.goal_x}, {self.goal_y})，准备出发！')

    def pose_callback(self, msg):
        self.current_x = msg.x
        self.current_y = msg.y
        self.current_theta = msg.theta

    def control_loop(self):
        distance = math.sqrt((self.goal_x - self.current_x)**2 + (self.goal_y - self.current_y)**2)
        target_theta = math.atan2(self.goal_y - self.current_y, self.goal_x - self.current_x)
        
        angle_error = target_theta - self.current_theta
        angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))
        
        msg = Twist()
        
        if distance > 0.1:
            msg.linear.x = 1.0 * distance
            msg.angular.z = 2.0 * angle_error
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.get_logger().info('到达目标位置！')
            
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    navigator = TurtleNavigator()
    rclpy.spin(navigator)
    navigator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
