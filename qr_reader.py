import cv2

def get_data_from_qr():
    vid = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    qr_data = f'Nothing to show'
    while True:
        ret, frame = vid.read()
        data, bbox, straight_qrcode = detector.detectAndDecode(frame)
        if len(data) > 0:
            qr_data = data
            break
        cv2.imshow('Please show a qr code to the cam.', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    vid.release()
    cv2.destroyAllWindows()
    return qr_data