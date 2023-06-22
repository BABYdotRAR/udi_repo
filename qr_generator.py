import qrcode
import env_variables as env


def create_img(name, data):
    path = env.PROJECT_PATH + "\\img"
    img = qrcode.make(data)
    img.save(path + f'\{name}.jpg')

