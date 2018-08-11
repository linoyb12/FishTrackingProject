Fish 3D tracking:

Calibration:
1) Only ones for each camera - calibrate each camera separately.
	- Take pictures for each camera using the method takePictures in calibration.py with the camera number (usually 1/2)
	- Calibrate the camera using the method calibrateCamera in calibration.py with the folder path you want to save the calibration matrices in and the camera number. 
2) Run the GUI DataEntranceGui.py:
	Do when changing the position of the cameras - Match each world point to corresponding pixels for each camera.
		- Enter camera Id in the text element
		- Press on the button select points
		- Select the 4 points on the screen and press c when finished (their values will be saved in a npy file - side_cam_tank_points.npy, up_cam_tank_points.npy)
		Each point should match the real world point in the title, the coordinate system is described in the fish tracking Project_Info file.
		(The i'th point selected matches the i'th point in the array)
	Do when changing tank
		- Measure the tank sizes and update the values in the GUI (the height entered is the water height, not the tank's)
		- Press the button update tank config to update this values (after entering all 3 values).
	
Finding object 3D coordinates:
1) Find the pixel coordinates of the object for each camera.
	- Press the button Track fish in the main window.
	- Enter index for each camera
	-Press the button select point and select one point on the screen. (To exit enter c)
	-Select the point on the screen and press c when finished (The chosen point coordinates will be then displayed on the screen)
2) Find 3D coordinates:
	- After entering the point for each camera select the button calculate coordinates in order to calculate the object point.
	- The point will be displayed in the window.
