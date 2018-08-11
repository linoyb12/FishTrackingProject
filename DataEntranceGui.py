from Tkinter import *
import numpy as np
import scene_planner
import fish_3D_coordinates
import os.path

side_cam_tank_points_path = fish_3D_coordinates.side_cam_tank_points_path
up_cam_tank_points_path = fish_3D_coordinates.up_cam_tank_points_path
tank_config_path = fish_3D_coordinates.tank_config_path

class TrackGUI:
    def __init__(self, window):
        self.window = window
        row = 0

        side_cam_text = 'Side camera index:'
        up_cam_text = 'Up camera index:'

        row += 1
        Label(window, text=side_cam_text).grid(row=row, column=0, sticky=W)
        self.side_cam_index = Entry(window, width=5)
        self.side_cam_index.grid(row=row, column=1, padx=2, sticky=W)
        self.side_cam_button = Button(window, text='Select point', command = self.set_side_point)
        self.side_cam_button.grid(row=row, column=2, padx=2, sticky=W)

        row += 1
        Label(window, text=up_cam_text).grid(row=row, column=0, sticky=W)
        self.up_cam_index = Entry(window, width=5)
        self.up_cam_index.grid(row=row, column=1, padx=2, sticky=W)
        self.up_cam_button = Button(window, text='Select point', command = self.set_up_point)
        self.up_cam_button.grid(row=row, column=2, padx=2, sticky=W)

        side_cam_text = 'Side camera point    x:'
        up_cam_text =   'Up camera point      x:'

        row+=1
        Label(window, text=side_cam_text).grid(row=row, column=0, sticky=W)
        self.side_cam_x = Entry(window, width = 13)
        self.side_cam_x.grid(row=row, column=2, padx=2, sticky=W)
        Label(window, text='y:').grid(row=row, column=3, sticky=W)
        self.side_cam_y = Entry(window, width = 13)
        self.side_cam_y.grid(row=row, column=4, padx=2, sticky=W)

        row+=1
        Label(window, text=up_cam_text).grid(row=row, column=0, sticky=W)
        self.up_cam_x = Entry(window, width = 13)
        self.up_cam_x.grid(row=row, column=2, padx=2, sticky=W)
        Label(window, text='y:').grid(row=row, column=3, sticky=W)
        self.up_cam_y = Entry(window, width = 13)
        self.up_cam_y.grid(row=row, column=4, padx=2, sticky=W)

        row += 1
        self.track_obj_button = Button(window, text='calculate coordinates', command = self.get_3D_coordinates)
        self.track_obj_button.grid(row=row, column=0, padx=3, pady=3)

        Label(window, text='x:').grid(row=row, column=1, sticky=W)
        self.result_x = Entry(window, width = 13)
        self.result_x.grid(row=row, column=2, padx=3, pady=3, sticky=W)

        Label(window, text='y:').grid(row=row, column=3, sticky=W)
        self.result_y = Entry(window, width = 13)
        self.result_y.grid(row=row, column=4, padx=3, pady=3, sticky=W)

        Label(window, text='z:').grid(row=row, column=5, sticky=W)
        self.result_z = Entry(window, width = 13)
        self.result_z.grid(row=row, column=6, padx=3, pady=3, sticky=W)

        window.mainloop()

    def get_3D_coordinates(self):
        side_x = self.side_cam_x.get()
        side_y = self.side_cam_y.get()
        up_x = self.up_cam_x.get()
        up_y = self.up_cam_y.get()
        sideCoordinates = np.array([side_x, side_y], dtype=np.float32)
        upCoordinates = np.array([up_x, up_y], dtype=np.float32)
        point = fish_3D_coordinates.calculate3DCoordinates(sideCoordinates, upCoordinates)
        self.result_x.insert(0, point[0])
        self.result_y.insert(0, point[1])
        self.result_z.insert(0, point[2])

    def set_side_point(self):
        cam_id = int(self.side_cam_index.get())
        arr = scene_planner.SP_Main(cam_id)
        point = arr[0]
        self.side_cam_x.insert(0, point[0])
        self.side_cam_y.insert(0, point[1])

    def set_up_point(self):
        cam_id = int(self.up_cam_index.get())
        arr = scene_planner.SP_Main(cam_id)
        point = arr[0]
        self.up_cam_x.insert(0, point[0])
        self.up_cam_y.insert(0, point[1])

class DataGUI:
    def __init__(self, window):
        self.window = window

        title = 'Press on the points corresponding to the following world points (in that order)'
        world_points = '[0, 0, 0], [tank_length, 0, 0], [0, tank_width, 0], [tank_length, tank_width, 0]'

        row = 0
        Label(window, text=title).grid(row=row, column=0, columnspan = 3, sticky=W)

        row+=1
        Label(window, text=world_points).grid(row=row, column=0, columnspan = 3, sticky=W)

        side_cam_text = 'Side camera index:'
        up_cam_text = 'Up camera index:'

        row+=1
        Label(window, text=side_cam_text).grid(row=row, column=0, sticky=W)
        self.side_cam_index = Entry(window, width = 5)
        self.side_cam_index.grid(row=row, column=1, padx=2, sticky=W)
        self.side_cam_button = Button(window, text='Select points', command = self.select_side_cam_points)
        self.side_cam_button.grid(row=row, column=2, padx=2, sticky=W)

        row+=1
        Label(window, text=up_cam_text).grid(row=row, column=0, sticky=W)
        self.up_cam_index = Entry(window, width = 5)
        self.up_cam_index.grid(row=row, column=1, padx=2, sticky=W)
        self.up_cam_button = Button(window, text='Select points', command = self.select_up_cam_points)
        self.up_cam_button.grid(row=row, column=2, padx=2, sticky=W)

        row += 1
        Label(window, text="tank length:").grid(row=row, column=0, sticky=W)
        self.tank_length = Entry(window, width=10)
        self.tank_length.grid(row=row, column=1, padx=2, sticky=W)

        self.save_config = Button(window, text='Update tank config', command = self.save_tank_config)
        self.save_config.grid(row=row, column=2, rowspan = 3, padx=2, sticky=W)

        row += 1
        Label(window, text="tank width:").grid(row=row, column=0, sticky=W)
        self.tank_width = Entry(window, width=10)
        self.tank_width.grid(row=row, column=1, padx=2, sticky=W)

        row += 1
        Label(window, text="tank height:").grid(row=row, column=0, sticky=W)
        self.tank_height = Entry(window, width=10)
        self.tank_height.grid(row=row, column=1, padx=2, sticky=W)

        row+=1
        self.track_obj_button = Button(window, text='Track fish', command=self.track_fish_window, width = 30)
        self.track_obj_button.grid(row=row, column=0, columnspan = 3, pady = 3)
        window.mainloop()

    def track_fish_window(self):
        self.window.destroy()
        track_window = Tk()
        TrackGUI(track_window)

    def select_side_cam_points(self):
        cam_id = int(self.side_cam_index.get())
        arr = scene_planner.SP_Main(cam_id)
        np_arr = np.array(arr, dtype=np.float32)
        save_arr_in_path(side_cam_tank_points_path, np_arr)

    def select_up_cam_points(self):
        cam_id = int(self.up_cam_index.get())
        arr = scene_planner.SP_Main(cam_id)
        np_arr = np.array(arr, dtype=np.float32)
        save_arr_in_path(up_cam_tank_points_path, np_arr)

    def save_tank_config(self):
        tank_length = int(self.tank_length.get())
        tank_width = int(self.tank_width.get())
        tank_height = int(self.tank_height.get())
        arr = np.array([tank_length, tank_width, tank_height])
        save_arr_in_path(tank_config_path, arr)


def save_arr_in_path(path, arr):
    if os.path.exists(path):
        os.remove(path)
    np.save(path, arr)


window = Tk()
DataGUI(window)