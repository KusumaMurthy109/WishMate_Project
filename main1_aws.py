import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from rekognition import Rekognition

# Load the kv file
Builder.load_file('image_app.kv')

class ImageAppLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ImageAppLayout, self).__init__(**kwargs)
        self.r = Rekognition()

    def option_selected(self, option):
        if option == 'c':
            self.capture_image()
        elif option == 'u':
            self.upload_image()

    def capture_image(self):
        # Your capture logic here
        r = self.r
        r.camera()
        file_path = "/Users/kusumamurthy/Desktop/HackKU/2024/Actual/images"
        s3 = "s3://hack-ku-2024/"

        instruction = f"aws s3 cp {file_path} {s3} --recursive"
        subprocess.run(instruction, shell=True)

        camera_wishlist_path = "/Users/kusumamurthy/Desktop/HackKU/2024/Actual/camera_wishlist.txt"
        with open(camera_wishlist_path, "w") as camera_wishlist:
            photo = 'image1.png'
            bucket = 'hack-ku-2024'
            result = self.r.image_lable_recognizer(photo, bucket)
            camera_wishlist.write(','.join(result))

    def upload_image(self):
        # Your upload logic here
        file_path = "/Users/kusumamurthy/Desktop/HackKU/2024/Actual/images"
        s3 = "s3://hack-ku-2024/"

        instruction = f"aws s3 cp {file_path} {s3} --recursive"
        subprocess.run(instruction, shell=True)

        camera_wishlist_path = "/Users/kusumamurthy/Desktop/HackKU/2024/Actual/camera_wishlist.txt"
        with open(camera_wishlist_path, "w") as camera_wishlist:
            photo = 'jeacket.png'
            bucket = 'hack-ku-2024'
            result = self.r.image_lable_recognizer(photo, bucket)
            camera_wishlist.write(','.join(result))

class ImageApp(App):
    def build(self):
        return ImageAppLayout()

if __name__ == "__main__":
    ImageApp().run()
