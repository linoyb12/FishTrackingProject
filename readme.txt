Fish 3D tracking:

Calibration:
1) Only ones for each camera - calibrate each camera separately.
	- take pictures for each camera using the method takePictures in calibration.py with the camera number (usually 1/2)
	- calibrate the camera using the method calibrateCamera in calibration.py with the folder path you want to save the calibration 	matrices in and the camera number. 
2) Do when changing the position of the cameras - Match each world point to corresponding pixels for each camera.
	- measure the tank sizes and update the values on fish_3D_cordinates.py (the height entered is the water height, not the tank's)
	- for each world point in the array world_coordinates, change the values of the pixel points in the same index of arrays 		cam_up_coordinates, cam_side_coordinates (fish_3D_cordinates.py) to the updated pixel point matching the world coordinate at each 	  index. (The world coordinates are the points of intersection of the tank with the water surface)
	To find the pixel points use scene_planner.py and select the relevant points (preferably in the order of the points in the array).
	When finished clicking on the points press c.
	The coordinate system is described in the fish tracking conclusion file.
	
Finding object 3D coordinates:
1) Find the pixel coordinates of the object for each camera.
	- use scene_planner.py and press the object on the same point for both cameras.
	- change the coordinates found in the arrays sideCoordinates, upCoordinates on fish_3D_cordinates.py. (make sure entering float 	values) 
2) Find 3D coordinates:
	- run the method calculate3DCoordinates on fish_3D_cordinates.py with the points from the previous step.
	The return value of the function is the 3D point of the object.
