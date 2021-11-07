import cv2

def empty():
    pass

def getContours(img, imgContour, areaMin, y=0):
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # É aqui onde trabalhamos com os contornos!
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #areaMin = areaMin #cv2.getTrackbarPos("AreaMin", "Parametros")
        areaMax = 1000000 #cv2.getTrackbarPos("AreaMax", "Parametros")

        if areaMax > area > areaMin:
            #cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 3)

            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)

            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x, y), (x+w, y+h), (200,200,0), 4)

            cv2.putText(imgContour, "y: "+str(y), (50,50), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255,0,0), 1)
            """ 
            cv2.putText(imgContour, "Pontos: " + str(len(approx)), (x + w + 20, y + 20), 
                        cv2.FONT_HERSHEY_COMPLEX, .7, (255, 0, 0), 2)
            """
            cv2.putText(imgContour, "Area: " + str(int(area)), (10,170), #(x + w + 20, y + 45),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 0, 0), 1)
    
    return y