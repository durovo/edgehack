import cv2

font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 1
fontColor              = (255,255,255)
lineType               = 2

def displayText(text, x, y, img, font_color=(255, 255, 255)):
    cv2.putText(img, str(text), 
                (int(x), int(y)), 
                font, 
                fontScale,
                font_color,
                lineType)