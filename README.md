# ROS 2 自动导航与闭环控制项目

本项目基于 ROS 2 (Jazzy) 构建，包含两个基础控制节点：
1. `my_turtle_controller`：基于发布/订阅模型，实现海龟画圆。
2. `turtle_navigator`：基于比例控制（P-Control）的闭环导航，自动导航至指定坐标。

## 项目结构思维导图

```text
ROS 2 闭环导航程序 (navigate_to_goal.py)
│
├── 1. 依赖与初始化 (Imports & Initialization)
│   ├── rclpy / Node：ROS 2 基础运行环境与节点基类
│   ├── Twist：速度指令消息类型 (linear, angular)
│   ├── Pose：位姿状态消息类型 (x, y, theta)
│   └── math：数学计算库 (sqrt, atan2)
│
├── 2. 节点实例化与通信接口 (Communication Interfaces)
│   ├── 节点注册：super().__init__('turtle_navigator')
│   ├── 发布者 (Publisher)：向 /turtle1/cmd_vel 发送 Twist 控制指令
│   ├── 订阅者 (Subscriber)：监听 /turtle1/pose 接收实时 Pose 状态
│   └── 定时器 (Timer)：以 10Hz (0.1s) 频率触发控制逻辑
│
├── 3. 状态数据管理 (State Management)
│   ├── 当前状态变量：current_x, current_y, current_theta (由回调更新)
│   └── 目标状态变量：goal_x, goal_y (预设常量)
│
├── 4. 数据流与回调函数 (Data Flow & Callbacks)
│   ├── [感知] pose_callback(msg)
│   │   └── 动作：将接收到的 msg 数据实时覆写至当前状态变量
│   │
│   └── [控制] control_loop() (周期性执行)
│       ├── 步骤 A：计算欧氏距离 (Euclidean Distance)
│       ├── 步骤 B：计算目标方位角 (Target Angle)
│       ├── 步骤 C：计算角度误差并归一化 (Angle Error & Normalization)
│       └── 步骤 D：比例控制与指令生成 (P-Control & Action)
│           ├── 条件 1：distance > 0.1 -> 发送比例速度指令
│           └── 条件 2：distance <= 0.1 -> 停止并输出日志
│
└── 5. 主程序入口 (Main Execution)
    ├── rclpy.init()：初始化 ROS 2 环境
    ├── 实例化 Node：TurtleNavigator()
    ├── rclpy.spin()：事件循环阻塞
    └── 资源清理：destroy_node() & shutdown()
