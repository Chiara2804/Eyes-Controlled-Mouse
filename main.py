import cv2
import mediapipe as mp
import pyautogui

def show_webcam():
    scale = 10

    camera = cv2.VideoCapture(0)

    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = pyautogui.size()

    while True:
        _, frame = camera.read()
        frame = cv2.flip(frame, 1)

        height, width, channels = frame.shape
        #cropping
        centerX,centerY=int(height/2),int(width/2)
        radiusX,radiusY= int(scale*height/100),int(scale*width/100)
        minX,maxX=centerX-radiusX,centerX+radiusX
        minY,maxY=centerY-radiusY,centerY+radiusY
        cropped = frame[minX:maxX, minY:maxY]
        resized_cropped = cv2.resize(cropped, (width, height))

        rgb_frame = cv2.cvtColor(resized_cropped, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        # print(landmark_points)
        frame_h, frame_w, _ = resized_cropped.shape
        if landmark_points:
            landmarks = landmark_points[0].landmark
            for id, landmark in enumerate(landmarks[473:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(resized_cropped, (x, y), 3, (0, 255, 0))
                if id == 1:
                    screen_x = screen_w / frame_w * x
                    screen_y = screen_h / frame_h * y
                    try:
                        pyautogui.moveTo(screen_x, screen_y) 
                    except pyautogui.FailSafeException:
                        print('Running code before exiting.')
                        break
                    pyautogui.moveTo(screen_x, screen_y)
            # LEFT CLICK
            left = [landmarks[145], landmarks[159]]
            for landmark in left:
                xl = int(landmark.x * frame_w)
                yl = int(landmark.y * frame_h)
                cv2.circle(resized_cropped, (xl, yl), 3, (0, 255, 255))
            if (left[0].y - left[1].y) < 0.04:
                # print('click')
                pyautogui.click()
                pyautogui.sleep(0.05)
            # RIGHT CLICK
            right = [landmarks[374], landmarks[386]]
            for landmark in right:
                xr = int(landmark.x * frame_w)
                yr = int(landmark.y * frame_h)
                cv2.circle(resized_cropped, (xr, yr), 3, (255, 0, 0))
            if (right[0].y - right[1].y) < 0.02:
                print(right[0].y - right[1].y)
                # print('click')
                pyautogui.click(button='right')
                pyautogui.sleep(0.05)

        cv2.imshow('Eyes Controlled Mouse', resized_cropped)
        key = cv2.waitKey(10)
        # if Esc key is press then break out of the loop 
        if key == 27: 
            break
    
    camera.release()
    cv2.destroyAllWindows()

def main():
    show_webcam()

if __name__ == '__main__':
    main()