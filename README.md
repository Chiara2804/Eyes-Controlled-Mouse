<img src="README_imgs/github-header-image.png" width="100%"/>
<div>
  <img src="https://img.shields.io/badge/Made%20with-Jupyter-orange?style=for-the-badge&logo=Jupyter"/>
</div>
An AI which helps you to control your mouse using your eyes.

### Requirements
<ul> 
  <li>Python 3
  <li>OpenCV
  <li>Mediapipe
  <li>PyAutoGUI
</ul>

## Code
Zooming and cropping the frame.
``` python
scale = 10
centerX,centerY=int(height/2),int(width/2)
radiusX,radiusY= int(scale*height/60),int(scale*width/60)
minX,maxX=centerX-radiusX,centerX+radiusX
minY,maxY=centerY-radiusY,centerY+radiusY
cropped = frame[minX:maxX, minY:maxY]
resized_cropped = cv2.resize(cropped, (width, height))
```
<br>
Finding out landamrks of the eyes.

``` python
rgb_frame = cv2.cvtColor(resized_cropped, cv2.COLOR_BGR2RGB)
output = face_mesh.process(rgb_frame)
landmark_points = output.multi_face_landmarks
```
<br>
Moving the mouse the same space the eyes move.

``` python
screen_x = screen_w / frame_w * x
screen_y = screen_h / frame_h * y
try:
  pyautogui.moveTo(screen_x, screen_y) 
except pyautogui.FailSafeException:
  print('Running code before exiting.')
  break
pyautogui.moveTo(screen_x, screen_y)
```
<br>
Left click: if the y coordinates of upper and lower eyelid are close enough.

``` python
for landmark in left:
  x = int(landmark.x * frame_w)
  y = int(landmark.y * frame_h)
  cv2.circle(resized_cropped, (x, y), 3, (0, 255, 255))
if (left[0].y - left[1].y) < 0.04:
  pyautogui.click()
  pyautogui.sleep(1)
```
