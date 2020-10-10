import cv2

camWidth=800
camHeight=600

webcam=cv2.VideoCapture("/dev/video0")
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, camWidth)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, camHeight)


prefix="./sudoku/new/"
suffix="_img"

index=126

while True:
    _, frame = webcam.read()
    #need to flip the image
    frame = cv2.flip(frame, -1)

    h, w, _ = frame.shape
    cv2.imshow("webcam",frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('w'):
        fname="{}{:04d}{}.jpg".format(prefix,index,suffix)
        cv2.imwrite(fname,frame)
        print("{} saved!".format(fname))
        index = index + 1
webcam.release()
cv2.destroyWindow("webcam")

