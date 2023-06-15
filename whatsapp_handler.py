import pywhatkit

def send_img(path, number):
    pywhatkit.sendwhats_image(
        receiver=number,
        img_path=path
    )
    