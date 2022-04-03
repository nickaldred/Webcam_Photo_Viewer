from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
import time

from file_sharer import FileSharer
import webbrowser


Builder.load_file('frontend.kv')

class CameraScreen(Screen):
    """ Starts camera and changes Button text"""

    def start(self):
        self.ids.camera.opacity = 1
        self.ids.camera.play = True
        self.ids.cam_button.text = 'Stop Camera'
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        """Stops camera and changes button text"""
        self.ids.camera.opacity = 0
        self.ids.camera.play = False
        self.ids.cam_button.text = 'Start Camera'
        self.ids.camera.texture = None

    def capture(self):
        """ Creates a filename with the current time 
        and captures and saves a photo under that filename"""

        current_time = time.strftime('%Y%m%d-%H%M%S')
        self.filepath = "files/" + current_time + ".png"
        self.ids.camera.export_to_png(self.filepath)
        self.manager.current = 'image_screen'
        self.manager.current_screen.ids.img.source = self.filepath


class ImageScreen(Screen):
    link_message = "Create a Link First"
    def create_link(self):
        """ Access the photo filepath, uploads it to the web and 
        inserts the link the label widget"""
        file_path = App.get_running_app().root.ids.camera_screen.filepath
        filesharer = FileSharer(filepath = file_path)
        self.url = filesharer.share()
        self.ids.link.text = self.url
        print (self.url)

    def copy_link(self):
        """ Copys the link for the photo into the clipboard if it exists"""
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text = self.link_message

    def open_link(self):
        """Opens the link in a web browser"""
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = self.link_message


class RootWidget(ScreenManager):
    pass

class MainApp(App):
        
        def build(self):
            return RootWidget()

MainApp().run()





