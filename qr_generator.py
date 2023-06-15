import qrcode


def create_img(name, data):
    img = qrcode.make(data)
    img.save(f'.\img\{name}.jpg')

