import pygame as pg





class Controller():
    def __init__(self,cont_number=0):
        try:
            self.controller = pg.joystick.Joystick(cont_number)
            self.controller.init()
            try:
                cont_id = self.controller.get_instance_id()
            except AttributeError:
                cont_id = self.controller.get_id()
        except IOError:
            print("no controller connected")


    def get_hat(self):
        hat = self.controller.get_hat(0)
        x = hat[0]
        y = hat[1]*-1
        hat_dict = {"H_X":x,"H_Y":y}
        return hat_dict

    def get_buttons(self):
        south = self.controller.get_button(0)
        east = self.controller.get_button(1)
        west = self.controller.get_button(2)
        north = self.controller.get_button(3)
        l_trigger = self.controller.get_button(4)
        r_trigger = self.controller.get_button(5)
        start = self.controller.get_button(6)
        options = self.controller.get_button(7)
        l_joystick_click = self.controller.get_button(8)
        r_joystick_click = self.controller.get_button(9)
        button_dict = {"B_S":south,"B_E":east,"B_W":west,"B_N":north,"B_LT":l_trigger,"B_RT":r_trigger,"B_ST":start,"B_O":options,"B_LJC":l_joystick_click,"B_RJC":r_joystick_click}
        return button_dict

    def get_axis(self):
        left_joystickX = self.controller.get_axis(0)
        left_joystickY = self.controller.get_axis(1)
        right_joystickX = self.controller.get_axis(2)
        right_joystickY = self.controller.get_axis(3)
        left_bumper = self.controller.get_axis(4)
        right_bumper = self.controller.get_axis(5)
        deadzoneBase = -0.1
        deadzoneRoof = 0.1

        if left_joystickY < deadzoneBase or left_joystickY > deadzoneRoof:#Stops drifting
            left_joystickY = left_joystickY
        else:
            left_joystickY = 0

        if left_joystickX < deadzoneBase or left_joystickX > deadzoneRoof:
            left_joystickX = left_joystickX
        else:
            left_joystickX = 0

        if right_joystickY < deadzoneBase or right_joystickY > deadzoneRoof:
            right_joystickY = right_joystickY
        else:
            right_joystickY = 0

        if right_joystickX < deadzoneBase or right_joystickX > deadzoneRoof:
            right_joystickX = right_joystickX
        else:
            right_joystickX = 0

        if left_bumper < deadzoneBase or left_bumper > deadzoneRoof:
            left_bumper = left_bumper
        else:
            left_bumper = 0

        if right_bumper < deadzoneBase or right_bumper > deadzoneRoof:
            right_bumper = right_bumper
        else:
            right_bumper = 0

        # total_axis = [left_bumper,right_bumper,left_joystickY,right_joystickY,left_joystickX,right_joystickX]
        # for i in range(len(total_axis)):
        #     if total_axis[i] < deadzoneBase or total_axis[i] > deadzoneRoof:
        #         total_axis[i] = total_axis[i]
        #     else:
        #         total_axis[i] = 0

        axis_dict = {"A_LX":left_joystickX,"A_LY":left_joystickY,"A_RX":right_joystickX,"A_RY":right_joystickY,"A_LB":left_bumper,"A_RB":right_bumper}
        return axis_dict
