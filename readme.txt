fish 3D tracking:

(update only once when switching setting)
- calibrate each camera separately using a chessboard. (calibration is done using the file calibration.py)
- match each world point to corresponding pixels for each camera. (using the file scene_planner.py select the 4 points of intersection with the water surface and the tank corners and then pressing c to exit and display 
	selected coordinates), the data collected will replace the array values cam_up_coordinates, cam_side_coordinates in file fish_3D_cordinates.py
- adjust the tank measurements to match the tank sizes (the height entered is the water height, not the tank's)


- find the pixel coordinates of the object at each camera. (can be done again using scene_planner.py)
- update the coordinates in fish_3D_coordinates.py to the once found.
- get the point 3D coordinates by running the program.
