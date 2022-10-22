# coding=utf-8

import sys
import logging
import time

from pymycobot.log import setup_logging
from pymycobot.error import calibration_parameters
from pymycobot.common import ProtocolCode, DataProcessor


class MyCobotCommandGenerator(DataProcessor):
    """MyCobot Python API
    Annotations:
        * = Chain operation
        x = ??? 

    Supported methods:

        # Overall status
            version()
            power_on()
            power_off()
            is_power_on()
            release_all_servos()
            is_controller_connected()

        # MDI mode and operation
            get_angles()
            send_angle()
            send_angles()
            get_coords()
            send_coords()
            is_in_position()
            is_moving() x

        # JOG mode and operation
            jog_angle()
            jog_coord()
            jog_stop()
            set_encoder()
            get_encoder()
            set_encoders()
            pause()
            resume()
            stop()
            is_paused()

        # Running status and Settings
            get_encoder()
            set_encoder()
            get_encoders()
            set_encoders()
            get_speed()
            set_speed() *
            get_joint_min_angle()
            get_joint_max_angle()

        # Servo control
            is_servo_enable()
            is_all_servo_enable()
            set_servo_data()
            get_servo_data()
            set_servo_calibration()
            release_servo()
            focus_servo()

        # Atom IO
            set_color() *
            set_pin_mode()
            set_digital_output()
            get_digital_input()
            set_pwm_mode() x
            set_pwm_output()
            get_gripper_value()
            set_gripper_state() *
            set_gripper_value()
            set_gripper_ini()
            is_gripper_moving()

        # Basic
            set_basic_output()
            get_basic_input()
    """

    def __init__(self, debug=False):
        """
        Args:
            debug    : whether show debug info
        """
        self._version = sys.version_info[:2][0]
        self.debug = debug
        setup_logging(self.debug)
        self.log = logging.getLogger(__name__)

    def _mesg(self, genre, *args, **kwargs):
        """
        Args:
            genre: command type (Command)
            *args: other data.
                   It is converted to octal by default.
                   If the data needs to be encapsulated into hexadecimal,
                   the array is used to include them. (Data cannot be nested)
            **kwargs: support `has_reply`
                has_reply: Whether there is a return value to accept.
        """
        command_data = self._process_data_command(args)

        if genre == 178:
            # 修改wifi端口
            command_data = self._encode_int16(command_data)
            
        elif genre in [76, 77]:
            command_data = [command_data[0]] + self._encode_int16(command_data[1])
        elif genre == 115:
            command_data = [command_data[1],command_data[3]]

        LEN = len(command_data) + 2
        command = [
            ProtocolCode.HEADER,
            ProtocolCode.HEADER,
            LEN,
            genre,
            command_data,
            ProtocolCode.FOOTER,
        ]

        real_command = self._flatten(command)
        has_reply = kwargs.get("has_reply", False)
        return real_command, has_reply

    # System status
    def get_robot_version(self):  # TODO: test method <2021-03-11, yourname> #
        """Get cobot version

        Return:
            mycobot   : 1
            mycobotPro: 101
        """
        return self._mesg(ProtocolCode.ROBOT_VERSION, has_reply=True)
    
    def get_system_version(self):
        """get system version"""
        return self._mesg(ProtocolCode.SOFTWARE_VERSION, has_reply = True)

    def get_robot_id(self):
        """get robot id"""
        return self._mesg(ProtocolCode.GET_ROBOT_ID, has_reply = True)
    
    def set_robot_id(self, id):
        """set robot id
        
        Args:
            id(int): 0 ~ 255
        """
        return self._mesg(ProtocolCode.SET_ROBOT_ID, id)

    # Overall status
    def power_on(self):
        """Open communication with Atom."""
        return self._mesg(ProtocolCode.POWER_ON)

    def power_off(self):
        """Close communication with Atom."""
        return self._mesg(ProtocolCode.POWER_OFF)

    def is_power_on(self):
        """Adjust robot arm status

        Return:
            1 - power on
            0 - power off
            -1 - error data
        """
        return self._mesg(ProtocolCode.IS_POWER_ON, has_reply=True)

    def release_all_servos(self):
        return self._mesg(ProtocolCode.RELEASE_ALL_SERVOS)

    def is_controller_connected(self):
        """Wether connected with Atom."""
        return self._mesg(ProtocolCode.IS_CONTROLLER_CONNECTED, has_reply=True)

    def read_next_error(self):
        """Robot Error Detection
        
        Return:
            list len 7.
            0 : No abnormality
            1 : Communication disconnected
            2 : Unstable communication
            3 : Servo abnormality
        """
        return self._mesg(ProtocolCode.READ_NEXT_ERROR, has_reply=True)    
    
    def set_free_mode(self, flag):
        """set to free mode
        
        Args:
            flag: 0/1
        """
        return self._mesg(ProtocolCode.SET_FREE_MODE, flag)

    def is_free_mode(self):
        """Check if it is free mode
        
        Return:
            0/1
        """
        return self._process_single(self._mesg(ProtocolCode.IS_FREE_MODE, has_reply=True))

    # MDI mode and operation
    def get_angles(self):
        """ Get the degree of all joints.

        Return:
            list: A float list of all degree.
        """
        return self._mesg(ProtocolCode.GET_ANGLES, has_reply=True)

    def send_angle(self, id, degree, speed):
        """Send one degree of joint to robot arm.

        Args:
            id : Joint id(genre.Angle)\n
                    For mycobot: int 1-6.\n
                    For mypalletizer: int 1-4.
                    For mypalletizer 340: int 1-3.
            degree : degree value(float)(about -170 ~ 170).
            speed : (int) 0 ~ 100
        """
        # self.calibration_parameters(id=id, degree=degree, speed=speed)
        return self._mesg(ProtocolCode.SEND_ANGLE, id, [self._angle2int(degree)], speed)

    # @check_parameters(Command.SEND_ANGLES)
    def send_angles(self, degrees, speed):
        """Send the degrees of all joints to robot arm.

        Args:
            degrees: a list of degree values(List[float]).\n
                        for mycobot: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0].\n
                        for mypalletizer: [0.0, 0.0, 0.0, 0.0]
                        for mypalletizer 340: [0.0, 0.0, 0.0]
            speed : (int) 0 ~ 100
        """
        # self.calibration_parameters(degrees=degrees, speed=speed)
        degrees = [self._angle2int(degree) for degree in degrees]
        return self._mesg(ProtocolCode.SEND_ANGLES, degrees, speed)

    def get_coords(self):
        """Get the coords from robot arm, coordinate system based on base.

        Return:
            list : A float list of coord 
                for mycobot: [x, y, z, rx, ry, rz]\n
                for mypalletizer: [x, y, z, θ]
                for mypalletizer 340: [x, y, z]
        """
        return self._mesg(ProtocolCode.GET_COORDS, has_reply=True)

    def send_coord(self, id, coord, speed):
        """Send one coord to robot arm. 

        Args:
            id(int) : coord id(genre.Coord)\n
                        For mycobot: int 1-6.\n
                        For mypalletizer: int 1-4.
                        For mypalletizer 340: int 1-3.
            coord(float) : coord value, mm
            speed(int) : 0 ~ 100
        """
        # self.calibration_parameters(id=id, speed=speed)
        value = self._coord2int(coord) if id <= 3 else self._angle2int(coord)
        return self._mesg(ProtocolCode.SEND_COORD, id, [value], speed)

    def send_coords(self, coords, speed, mode=None):
        """Send all coords to robot arm.

        Args:
            coords: a list of coords value(List[float]).
                        for mycobot :[x(mm), y, z, rx(angle), ry, rz]\n
                        for mypalletizer: [x, y, z, θ]
                        for mypalletizer 340: [x, y, z]
            speed : (int) 0 ~ 100
            mode : (int) 0 - angluar, 1 - linear (mypalletizer 340 does not require this parameter)
        """
        # self.calibration_parameters(coords=coords, speed=speed)
        coord_list = []
        for idx in range(3):
            coord_list.append(self._coord2int(coords[idx]))
        for angle in coords[3:]:
            coord_list.append(self._angle2int(angle))
        # print(coord_list)
        if mode is not None:
            return self._mesg(ProtocolCode.SEND_COORDS, coord_list, speed, mode)
        else:
            return self._mesg(ProtocolCode.SEND_COORDS, coord_list, speed)

    def is_in_position(self, data, id=0):
        """Judge whether in the position. (mypalletizer 340 does not have this interface)

        Args:
            data: A data list, angles or coords.
                    for mycobot: len 6.
                    for mypalletizer: len 4
            id: 1 - coords, 0 - angles

        Return:
            1 - True\n
            0 - False\n
            -1 - Error
        """
        if id == 1:
            # self.calibration_parameters(coords=data)
            data_list = []
            for idx in range(3):
                data_list.append(self._coord2int(data[idx]))
            for idx in range(3, 6):
                data_list.append(self._angle2int(data[idx]))
        elif id == 0:
            # self.calibration_parameters(degrees=data)
            data_list = [self._angle2int(i) for i in data]
        else:
            raise Exception("id is not right, please input 0 or 1")

        return self._mesg(ProtocolCode.IS_IN_POSITION, data_list, id, has_reply=True)

    def is_moving(self):
        """Detect if the robot is moving

        Return:
            0 - not moving
            1 - is moving
            -1 - error data
        """
        return self._mesg(ProtocolCode.IS_MOVING, has_reply=True)

    # JOG mode and operation
    def jog_angle(self, joint_id, direction, speed):
        """Jog control angle.

        Args:
            joint_id: int
                    For mycobot: int 1-6.\n
                    For mypalletizer: int 1-4.
                    For mypalletizer 340: int 1-3.
            direction: 0 - decrease, 1 - increase
            speed: int (0 - 100)
        """
        return self._mesg(ProtocolCode.JOG_ANGLE, joint_id, direction, speed)

    def jog_coord(self, coord_id, direction, speed):
        """Jog control coord.

        Args:
            coord_id: int
                    For mycobot: int 1-6.\n
                    For mypalletizer: int 1-4.
                    For mypalletizer 340: int 1-3.
            direction: 0 - decrease, 1 - increase
            speed: int (0 - 100)
        """
        return self._mesg(ProtocolCode.JOG_COORD, coord_id, direction, speed)
    
    def jog_absolute(self, joint_id, angle, speed):
        """Jog absolute angle. (mypalletizer 340 does not have this interface)

        Args:
            joint_id: int
                    For mycobot: int 1-6.\n
                    For mypalletizer: int 1-4.
            angle: -180 ~ 180
            speed: int (0 - 100)
        """
        return self._mesg(ProtocolCode.JOG_ABSOLUTE, joint_id, [self._angle2int(angle)], speed)
    
    def jog_increment(self, joint_id, increment, speed):
        """step mode

        Args:
            joint_id: int 1-6.
            increment: 
            speed: int (0 - 100)
        """
        return self._mesg(ProtocolCode.JOG_INCREMENT, joint_id, [self._angle2int(increment)], speed)

    def jog_stop(self):
        """Stop jog moving"""
        return self._mesg(ProtocolCode.JOG_STOP)

    def pause(self):
        """Pause movement"""
        return self._mesg(ProtocolCode.PAUSE)

    def is_paused(self):
        """Judge whether the manipulator pauses or not.

        Return:
            1 - paused
            0 - not paused
            -1 - error
        """
        return self._mesg(ProtocolCode.IS_PAUSED, has_reply=True)

    def resume(self):
        """Recovery movement"""
        return self._mesg(ProtocolCode.RESUME)

    def stop(self):
        """Stop moving"""
        return self._mesg(ProtocolCode.STOP)

    def set_encoder(self, joint_id, encoder):
        """Set a single joint rotation to the specified potential value. (mypalletizer 340 does not have this interface)

        Args:
            joint_id: int
                for mycobot: Joint id 1 - 6
                for mypalletizer: Joint id 1 - 4
                for mycobot gripper: Joint id 7
            encoder: The value of the set encoder.
        """
        return self._mesg(ProtocolCode.SET_ENCODER, joint_id, [encoder])

    def get_encoder(self, joint_id):
        """Obtain the specified joint potential value. (mypalletizer 340 does not have this interface)

        Args:
            joint_id: (int) 1 ~ 6

        Returns:
            encoder: 0 ~ 4096
        """
        return self._mesg(ProtocolCode.GET_ENCODER, joint_id, has_reply=True)

    def set_encoders(self, encoders, sp):
        """Set the six joints of the manipulator to execute synchronously to the specified position. (mypalletizer 340 does not have this interface)

        Args:
            encoders: A encoder list, length 6.
            sp: speed 0 ~ 100
        """
        return self._mesg(ProtocolCode.SET_ENCODERS, encoders, sp)

    def get_encoders(self):
        """Get the six joints of the manipulator (mypalletizer 340 does not have this interface)

        Return:
            The list of encoders
        """
        return self._mesg(ProtocolCode.GET_ENCODERS, has_reply=True)

    # Running status and Settings
    def get_speed(self):
        """Get speed

        Return: 
            int
        """
        return self._mesg(ProtocolCode.GET_SPEED, has_reply=True)

    def set_speed(self, speed):
        """Set speed value

        Args:
            speed (int) - 0 ~ 100
        """
        # self.calibration_parameters(speed=speed)
        return self._mesg(ProtocolCode.SET_SPEED, speed)

    """
    def get_feed_override(self):
        return self._process_single(
            self._mesg(Command.GET_FEED_OVERRIDE, has_reply=True)
        )
    """
    def get_acceleration(self):
        return self._process_single(
            self._mesg(ProtocolCode.GET_ACCELERATION, has_reply=True)
        )

    def set_acceleration(self, acc):
        """Set speed for all moves
        
        Args:
            acc: int
        """
        return self._mesg(ProtocolCode.SET_ACCELERATION, acc)

    def get_joint_min_angle(self, joint_id):
        """Gets the minimum movement angle of the specified joint

        Args: 
            joint_id: (int)

        Return:
            angle value(float)
        """
        # self.calibration_parameters(id=joint_id)
        return self._mesg(ProtocolCode.GET_JOINT_MIN_ANGLE, joint_id, has_reply=True)

    def get_joint_max_angle(self, joint_id):
        """Gets the maximum movement angle of the specified joint
        
        Args:
            joint_id: (int)

        Return:
            angle value(float)
        """
        # self.calibration_parameters(id=joint_id)
        return self._mesg(ProtocolCode.GET_JOINT_MAX_ANGLE, joint_id, has_reply=True)

    # Servo control
    def is_servo_enable(self, servo_id):
        """Determine whether all steering gears are connected

        Args:
            servo_id: (int) 1 ~ 6

        Return:
            0 - disable
            1 - enable
            -1 - error
        """
        return self._mesg(ProtocolCode.IS_SERVO_ENABLE, servo_id, has_reply=True)

    def is_all_servo_enable(self):
        """Determine whether the specified steering gear is connected

        Return:
            0 - disable
            1 - enable
            -1 - error
        """
        return self._mesg(ProtocolCode.IS_ALL_SERVO_ENABLE, has_reply=True)

    def set_servo_data(self, servo_id, data_id, value):
        """Set the data parameters of the specified address of the steering gear

        Args:
            servo_id: Serial number of articulated steering gear, 1 - 6.
            data_id: Data address.
            value: 0 - 4096
        """
        return self._mesg(ProtocolCode.SET_SERVO_DATA, servo_id, data_id, value)

    def get_servo_data(self, servo_id, data_id):
        """Read the data parameter of the specified address of the steering gear.

        Args:
            servo_id: Serial number of articulated steering gear, 1 - 6.
            data_id: Data address.

        Return:
            values 0 - 4096
        """
        return self._mesg(
            ProtocolCode.GET_SERVO_DATA, servo_id, data_id, has_reply=True
        )

    def set_servo_calibration(self, servo_id):
        """The current position of the calibration joint actuator is the angle zero point, 
            and the corresponding potential value is 2048.

        Args:
            servo_id: Serial number of articulated steering gear, 1 - 6.
        """
        return self._mesg(ProtocolCode.SET_SERVO_CALIBRATION, servo_id)
    
    def joint_brake(self, joint_id):
        """Make it stop when the joint is in motion, and the buffer distance is positively related to the existing speed
        
        Args:
            joint_id: 1 - 6 
        """
        return self._mesg(ProtocolCode.JOINT_BRAKE, joint_id)

    def release_servo(self, servo_id):
        """Power off designated servo

        Args:
            servo_id: int
                for mycobot: 1 - 6.\n
                for mypalletizer: 1 - 4
                for mypalletizer 340: 1 - 3
        """
        return self._mesg(ProtocolCode.RELEASE_SERVO, servo_id)

    def focus_servo(self, servo_id):
        """Power on designated servo

        Args:
            servo_id: int
                for mycobot: 1 - 6\n
                for mypalletizer: 1 - 4
                for mypalletizer 340: 1 - 3
        """
        return self._mesg(ProtocolCode.FOCUS_SERVO, servo_id)

    # Atom IO
    def set_color(self, r=0, g=0, b=0):
        """Set the light color on the top of the robot arm.

        Args:
            r (int): 0 ~ 255
            g (int): 0 ~ 255
            b (int): 0 ~ 255

        """
        self.calibration_parameters(rgb=[r, g, b])
        return self._mesg(ProtocolCode.SET_COLOR, r, g, b)

    def set_pin_mode(self, pin_no, pin_mode):
        """Set the state mode of the specified pin in atom.

        Args:
            pin_no   (int): pin number.
            pin_mode (int): 0 - input, 1 - output, 2 - input_pullup
        """
        return self._mesg(ProtocolCode.SET_PIN_MODE, pin_no, pin_mode)

    def set_digital_output(self, pin_no, pin_signal):
        """

        Args:
            pin_no     (int):
            pin_signal (int): 0 / 1
        """
        return self._mesg(ProtocolCode.SET_DIGITAL_OUTPUT, pin_no, pin_signal)

    def get_digital_input(self, pin_no):
        """singal value"""
        return self._mesg(ProtocolCode.GET_DIGITAL_INPUT, pin_no, has_reply=True)

    """
    def set_pwm_mode(self, pin_no, channel):
        self._mesg(Command.SET_PWM_MODE, pin_no, channel)
    """

    def set_pwm_output(self, channel, frequency, pin_val):
        """ PWM control 

        Args:
            channel (int): IO number.
            frequency (int): clock frequency
            pin_val (int): Duty cycle 0 ~ 256; 128 means 50%
        """
        return self._mesg(ProtocolCode.SET_PWM_OUTPUT, channel, [frequency], pin_val)

    def get_gripper_value(self):
        """Get the value of gripper.

        Return: 
            gripper value (int)
        """
        return self._mesg(ProtocolCode.GET_GRIPPER_VALUE, has_reply=True)

    def set_gripper_state(self, flag, speed):
        """Set gripper switch state

        Args:
            flag  (int): 0 - open, 1 - close
            speed (int): 0 ~ 100
        """
        return self._mesg(ProtocolCode.SET_GRIPPER_STATE, flag, speed)

    def set_gripper_value(self, value, speed):
        """Set gripper value

        Args:
            value (int): 0 ~ 100
            speed (int): 0 ~ 100
        """
        self.calibration_parameters(speed=speed)
        return self._mesg(ProtocolCode.SET_GRIPPER_VALUE, value, speed)

    def set_gripper_calibration(self):
        """Set the current position to zero, set current position value is `2048`."""
        return self._mesg(ProtocolCode.SET_GRIPPER_CALIBRATION)

    def is_gripper_moving(self):
        """Judge whether the gripper is moving or not

        Returns:
            0 - not moving
            1 - is moving
            -1- error data
        """
        return self._mesg(ProtocolCode.IS_GRIPPER_MOVING, has_reply=True)

    # Basic
    def set_basic_output(self, pin_no, pin_signal):
        """Set basic output for M5 version.

        Args:
            pin_no: pin port number.
            pin_signal: 0 / 1
        """
        return self._mesg(ProtocolCode.SET_BASIC_OUTPUT, pin_no, pin_signal)

    def get_basic_input(self, pin_no):
        """Get basic input for M5 version.

        Args:
            pin_no: (int) pin port number.
        """
        return self._mesg(ProtocolCode.GET_BASIC_INPUT, pin_no, has_reply=True)

    def set_ssid_pwd(self, account, password):
        """Change connected wifi. (Apply to m5 or seeed)

        Args:
            account: (str) new wifi account.
            password: (str) new wifi password.
        """
        self._mesg(ProtocolCode.SET_SSID_PWD) # 先发指令，再发设置的账号密码
        time.sleep(0.02)
        return self._mesg(ProtocolCode.SET_SSID_PWD, account, password, has_reply=True)

    def get_ssid_pwd(self):
        """Get connected wifi account and password. (Apply to m5 or seeed)

        Return: 
            (account, password)
        """
        return self._mesg(ProtocolCode.GET_SSID_PWD, has_reply=True)

    def set_server_port(self, port):
        """Change the connection port of the server.

        Args:
            port: (int) The new connection port of the server.
        """
        return self._mesg(ProtocolCode.SET_SERVER_PORT, port)

    def get_tof_distance(self):
        """ Get the detected distance (Requires external distance detector).

        Return:
            (int) The unit is mm.
        """
        return self._mesg(ProtocolCode.GET_TOF_DISTANCE, has_reply=True)
    
    def set_tool_reference(self, coords):
        """Set tool coordinate system
        
        Args:
            coords: a list of coords value(List[float])
                for mycobot :[x(mm), y, z, rx(angle), ry, rz]
                for mypalletizer 340: [x, y, z]
        """
        # self.calibration_parameters(coords=coords)
        coord_list = []
        for idx in range(3):
            coord_list.append(self._coord2int(coords[idx]))
        for angle in coords[3:]:
            coord_list.append(self._angle2int(angle))
        return self._mesg(ProtocolCode.SET_TOOL_REFERENCE, coord_list)
    
    def get_tool_reference(self):
        """Get tool coordinate system """
        return self._mesg(ProtocolCode.GET_TOOL_REFERENCE, has_reply=True)
    
    def set_world_reference(self, coords):
        """Set the world coordinate system
        
        Args:
            coords: a list of coords value(List[float])
                for mycobot :[x(mm), y, z, rx(angle), ry, rz]
                for mypalletizer 340: [x, y, z]
        """
        # self.calibration_parameters(coords=coords)
        coord_list = []
        for idx in range(3):
            coord_list.append(self._coord2int(coords[idx]))
        for angle in coords[3:]:
            coord_list.append(self._angle2int(angle))
        return self._mesg(ProtocolCode.SET_WORLD_REFERENCE, coord_list)
    
    def get_world_reference(self):
        """Get the world coordinate system"""
        return self._mesg(ProtocolCode.GET_WORLD_REFERENCE, has_reply=True)
    
    def set_reference_frame(self, rftype):
        """Set the base coordinate system
        
        Args:
            rftype: 0 - base 1 - tool.
        """
        return self._mesg(ProtocolCode.SET_REFERENCE_FRAME, rftype)
    
    def get_reference_frame(self):
        """Get the base coordinate system
        
        Return: 
            0 - base 1 - tool.
        """
        return self._mesg(ProtocolCode.GET_REFERENCE_FRAME, has_reply=True)
    
    def set_movement_type(self, move_type):
        """Set movement type
        
        Args:
            move_type: 1 - movel, 0 - moveJ
        """
        return self._mesg(ProtocolCode.SET_MOVEMENT_TYPE, move_type)

    def get_movement_type(self):
        """Get movement type
        
        Return: 
            1 - movel, 0 - moveJ
        """
        return self._mesg(ProtocolCode.GET_MOVEMENT_TYPE, has_reply=True)
    
    def set_end_type(self, end):
        """Set end coordinate system
        
        Args:
            end: int
                0 - flange, 1 - tool
        """
        return self._mesg(ProtocolCode.SET_END_TYPE, end)
    
    def get_end_type(self):
        """Get end coordinate system
        
        Return: 
            0 - flange, 1 - tool
        """
        return self._mesg(ProtocolCode.GET_END_TYPE, has_reply=True)
        
    
    def get_plan_speed(self):
        """Get planning speed
        
        Args:
            return: 
                [movel planning speed, movej planning speed].
        """
        return self._mesg(ProtocolCode.GET_PLAN_SPEED, has_reply=True)
    
    def get_plan_acceleration(self):
        """Get planning acceleration
        
        Args:
            return: 
                [movel planning acceleration, movej planning acceleration].
        """
        return self._mesg(ProtocolCode.GET_PLAN_ACCELERATION, has_reply=True)
    
    def set_plan_speed(self, speed, is_linear):
        """Set planning speed
        
        Args:
            speed (int): (0 ~ 100).
            is_linear: 0 -> joint 1 -> straight line
        """
        return self._mesg(ProtocolCode.SET_PLAN_SPEED, speed, is_linear)
    
    def set_plan_acceleration(self, acceleration, is_linear):
        """Set planning acceleration
        
        Args:
            acceleration (int): (0 ~ 100).
            is_linear: 0 -> joint 1 -> straight line
        """
        return self._mesg(ProtocolCode.SET_PLAN_ACCELERATION, acceleration, is_linear)
    
    def get_servo_speeds(self):
        """Get joint speed (Only for mycobot 350)
        
        Return: 
            unit step/s
        """
        return self._mesg(ProtocolCode.GET_SERVO_SPEED, has_reply=True)
    
    def get_servo_currents(self):
        """Get joint current (Only for mycobot 350)
        
        Return: 
            0 ~ 3250 mA
        """
        return self._mesg(ProtocolCode.GET_SERVO_CURRENTS, has_reply=True)
    
    def get_servo_voltages(self):
        """Get joint voltages (Only for mycobot 350)
        
        Return: 
            volts < 24 V
        """
        return self._mesg(ProtocolCode.GET_SERVO_VOLTAGES, has_reply=True)

    def get_servo_status(self):
        """Get joint status (Only for mycobot 350)
        
        Return: 
            [voltage, sensor, temperature, current, angle, overload], a value of 0 means no error, a value of 1 indicates an error
        """
        return self._mesg(ProtocolCode.GET_SERVO_STATUS, has_reply=True)

    def get_servo_temps(self):
        """Get joint temperature (Only for mycobot 350)"""
        return self._mesg(ProtocolCode.GET_SERVO_TEMPS, has_reply=True)
    
    def set_joint_max(self, id, angle):
        """Set the joint maximum angle
        
        Args:
            id: int.
                For mycobot: int 1-6.\n
                For mypalletizer: int 1-4.
                For mypalletizer 340: int 1-3.
            angle: 0 ~ 180 
        """
        return self._mesg(ProtocolCode.SET_JOINT_MAX, id, angle)
    
    def set_joint_min(self, id, angle):
        """Set the joint minimum angle
        
        Args:
            id: int.
                For mycobot: int 1-6.\n
                For mypalletizer: int 1-4.\n
                For mypalletizer 340: int 1-3.
            angle: 0 ~ 180 
        """
        return self._mesg(ProtocolCode.SET_JOINT_MIN, id, angle)
    
    def init_eletric_gripper(self): # TODO 22-5-19 need test
        """Electric gripper initialization (it needs to be initialized once after inserting and removing the gripper) (only for 350)"""
        return self._mesg(ProtocolCode.INIT_ELETRIC_GRIPPER)
    
    def set_eletric_gripper(self, status):  # TODO 22-5-19 need test
        """Set Electric Gripper Mode (only for 350)
        
        Args:
            status: 0 - open, 1 - close.
        """
        return self._mesg(ProtocolCode.SET_ELETRIC_GRIPPER, status)
    
    def set_encoders_drag(self, encoders, speeds):  # TODO 22-5-19 need test
        """Send all encoders and speeds
        
        Args:
            encoders: encoders list
            speeds: Obtained by the get_servo_speeds() method 
        """
        return self._mesg(ProtocolCode.SET_ENCODERS_DRAG, encoders, speeds)
    
    def set_fresh_mode(self, mode):   # TODO 22-5-19 need test
        """Set command refresh mode
        
        Args:
            mode: int.
                1 - Always execute the latest command first.
                0 - Execute instructions sequentially in the form of a queue.
        """
        return self._mesg(ProtocolCode.SET_FRESH_MODE, mode)
        
    def get_fresh_mode(self):
        """Query sports mode"""
        return self._mesg(ProtocolCode.GET_FRESH_MODE, has_reply = True)
