# Obstruction Map Tools

Example software for using photographic obstruction maps to control window shading.
The code in this repository accompanies the paper in Journal of Building Engineering: https://doi.org/10.1016/j.jobe.2020.101170

  * **convert-fish2orthonorm.py** - code from appendix 1 of the paper
  * **obstruction-map-query.py** - code from appendix 2
  * **images** directory - contains example photos from the paper for testing the code. Note: the images in this directory are for a facade with inclination angle of ~ 92 degrees (2 degrees off vertical), so the horizon is below the middle of the image.
    * **inputL.jpg** - a photo taken from the right side of a window to capture obstructions to the left, camera rotation = 0.14 degrees for this photo
    * **inputR.jpg** - a photo taken from the left side of a window to capture obstructions to the right, camera rotation = 0.99 degrees for this photo
    * **LA_obsmap.png** - an obstruction map example to test query function
  * **lens_distortion** directory - contains tools for measuring lens distortion
    * **camera_stepper_mount.stl** - a cad file for 3D printing an adapter to mount the camera module to a stepper motor.

## Measuring angular distortion

I'll include some of the scripts used for measuring angular distortion soon. For now I've included a file for 3D printing an adapter for mounting the camera module to a stepper motor.
![CAD model of adapter to mount camera module to stepper motor](lens_distortion/camera_stepper_mount.png)

Hardware used to rotate camera for distortion calibration:
  * NEMA 17 Stepper motor (https://www.amazon.com/dp/B00PNEQ9T4/)
  * Motor shield for raspberry pi (https://shop.sb-components.co.uk/products/motorshield-for-raspberry-pi)
  
