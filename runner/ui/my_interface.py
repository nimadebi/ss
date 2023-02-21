# import serial
# import tkinter as tk
#
# def read_serial(serial_port):
#     try:
#         while True:
#             data = serial_port.readline().decode().strip()
#             print(data)
#     except serial.SerialException:
#         pass
#
# def start_gui(serial_port):
#     root = tk.Tk()
#     root.title("Serial Data Receiver")
#
#     text = tk.Text(root)
#     text.pack()
#
#     def update_text():
#         nonlocal text
#         nonlocal serial_port
#         try:
#             data = serial_port.readline().decode().strip()
#             text.insert(tk.END, data + "\n")
#         except serial.SerialException:
#             pass
#         root.after(10, update_text)
#
#     root.after(10, update_text)
#     root.mainloop()
#
# if __name__ == "__main__":
#     import sys
#
#     port = sys.argv[1]
#
#     try:
#         serial_port = serial.Serial(port, baudrate=115200, timeout=1)
#     except serial.SerialException as e:
#         print(f"Error opening serial port: {e}")
#         sys.exit(1)
#
#     read_serial(serial_port)  # uncomment this line to simply print the data to the console
#     # start_gui(serial_port)  # uncomment this line to start the GUI

"""
Joystick keybinds, using pygame

forward pitch:
backward pitch:
right roll:
left roll:

left yaw:
right yaw:

motor throttle:

safe mode:
panic mode:
manual mode:
calibration mode:
yaw controlled mode:
full controlled mode:

"""
import os
import pygame
import serial


class X3DController(object):
    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def listen(self, serial_port):
        """Listen for events to happen"""

        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            read_serial_once(serial_port)
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value,2)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value

                os.system('clear')
                # pprint.pprint(self.button_data)
                # pprint.pprint(self.axis_data)
                # pprint.pprint(self.hat_data)

                """
                ESC, SPACE BAR	go to safe mode, through panic mode
                0	mode 0 -> Safety mode 
                1	mode 1 -> Panic mode
                numbers	etc. (random access)
                a/z	lift up/down
                left/right arrow	roll up/down
                up/down arrow	pitch down/up (cf. stick)
                q/w	yaw down/up
                u/j	yaw control P up/down
                i/k	roll/pitch control P1 up/down
                o/l	roll/pitch control P2 up/down
                
                
                The data that will be sent to the UART will be in the following format:
                [PROTOCOL HEADER]<mode><pitch><roll><yaw><throttle><yaw control P><roll/pitch control P1><roll/pitch control P2>
                
                So we have to compose this message to be sent.
                
                """

                if self.button_data[0]:
                    print("Safety mode pressed.")

                if self.button_data[1]:
                    print("Panic mode pressed.")
                if self.button_data[2]:
                    print("Button 2 pressed.")
                if self.button_data[3]:
                    print("Button 3 pressed.")
                if self.button_data[4]:
                    print("Button 4 pressed.")
                if self.button_data[5]:
                    print("Button 5 pressed.")
                if self.button_data[6]:
                    print("Button 6 pressed.")
                if self.button_data[7]:
                    print("Button 7 pressed.")
                if self.button_data[8]:
                    print("Button 8 pressed.")
                if self.button_data[9]:
                    print("Button 9 pressed.")
                if self.button_data[10]:
                    print("Button 10 pressed.")
                if self.button_data[11]:
                    print("Button 11 pressed.")
                if 0 in self.axis_data:
                    if self.axis_data[0] > 0:
                        print(f"Right roll pressed: {self.axis_data[0]}")
                    if self.axis_data[0] < 0:
                        print(f"Left roll pressed: {self.axis_data[0]}")
                if 1 in self.axis_data:
                    if self.axis_data[1] > 0:
                        print(f"Backward pitch pressed: {self.axis_data[1]}")
                    if self.axis_data[1] < 0:
                        print(f"Forward pitch pressed: {self.axis_data[1]}")
                if 2 in self.axis_data:
                    if self.axis_data[2] > 0:
                        print(f"Right yaw pressed: {self.axis_data[2]}")
                    if self.axis_data[2] < 0:
                        print(f"Left yaw pressed: {self.axis_data[2]}")
                if 3 in self.axis_data:
                    if self.axis_data[3] < 1:
                        print(f"Motor throttle pressed: {self.axis_data[3]}")


def read_controller(serial_port):
    joystick = X3DController()
    joystick.init()
    joystick.listen(serial_port)


def read_serial_loop(serial_port):
    try:
        while True:
            data = serial_port.readline().decode().strip()
            print(data)
    except serial.SerialException:
        pass


def read_serial_once(serial_port):
    try:
        data = serial_port.readline().decode().strip()
        print(data)
    except serial.SerialException as er:
        print(er)


def run_ui(serial_port):
    read_controller(serial_port)


if __name__ == "__main__":
    import sys

    port = sys.argv[1]

    try:
        serial_port = serial.Serial(port, baudrate=115200, timeout=1)
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        sys.exit(1)

    # read_serial(serial_port)
    # start_gui(serial_port)
    # read_controller()  # read the controller
    run_ui(serial_port)

    """
    Panic in case joystick disconnects! 
    Heartbeat to the drone
    
    """
