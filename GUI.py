from io import BytesIO
from pathlib import Path
from PIL import Image, ImageEnhance
import numpy as np
import PySimpleGUI as sg
import os



sg.theme('Black')

# Class title
class GUI:

    # the init function
    def __init__(self):
        # initiation variables used in rest of class
        self.column_width = 960
        self.column_height = 720
        self.width = 0
        self.height = 0
        self.diff = 10
        self.white = (255, 255, 255, 0)
        self.font = ('Courier New', 16, 'bold')
        # This is a graph, where the image resides (used in layout[])
        col = [[self.graph()]]
        # This is the left half of the GUI
        file_list_column = [
                            # variable creation within the PySimpleGUI class
                           [sg.Text("Image Folder:"),
                            sg.In(size=(25,1), enable_events=True, key="-FOLDER-"),
                            sg.FolderBrowse()],
                            [
                            self.button('Zoom In'),
                            self.button('Zoom Out'),
                            self.button('Previous')],
                            [self.button('Next'),
                            self.button('Brighten'),
                            self.button('Darken')],
                            [sg.Text("Search Image:"),
                            sg.Input(do_not_clear=True, size=(20, 1), enable_events=True, key='-INPUT-')],
                            [sg.Listbox(values=[], enable_events=True, size=(40, 20), key="-FILE LIST-")],

                            ]
        # This is the entire layout (right side inside)
        layout = [
            [
                # Left side
                sg.Column(file_list_column),
                # Line separating two sides
                sg.VSeperator(),
                # Right side (image display)
                self.column(col, key='Column'),
            ]
        ]
        # More instance variables
        self.window = sg.Window('Image Viewer - PACS Demo', layout, finalize=True,
            use_default_focus=False)
        self.draw   = self.window['Graph']
        self.im     = None
        self.key    = None
        self.scale  = 1
        self.folder = None
        self.fnames = None
        self.file_list = None
        self.filename = None
        self.listNum = None
        self.enhancer = None
        self.factor = None
        self.output = None
        self.results = None
        self.new_values = None

    # Button function used when creating buttons so all are uniform
    def button(self, text):
        return sg.Button(button_text=text, enable_events=True,
            key=text)

    # Column function used when creating columns so all are uniform
    def column(self, layout, key='Column'):
        return sg.Column(layout, background_color='grey', scrollable=True,
                         size=(self.column_width, self.column_height), key='Column')

    # File function used when creating files so all are uniform
    def file(self, save=False):
        return sg.popup_get_file('message', save_as=save, no_window=True,
            font=self.font, file_types=(
            ("ALL Files", "*.*"), ("PNG Files", "*.jpg")),
            default_extension='png')

    # Graph function used when creating graphs so all are uniform
    def graph(self):
        return sg.Graph(
            (self.column_width, self.column_height), (0, self.column_height),
            (self.column_width, 0), pad=(0, 0), background_color='grey',
            enable_events=True, key='Graph')

    # Image function used when creating images so all are uniform
    def image(self):
        return sg.Image(key='Image', enable_events=True)

    # function to draw the image on screen when it is updated
    def draw_image(self):
        try:
            # if theres something there
            if self.key:
                # delete it
                self.draw.delete_figure(self.key)
            # set new key to the new image at location 0, 0
            self.key = self.draw.draw_image(data=self.data, location=(0, 0))
            # draw
            self.draw.Widget.configure(width=self.width*self.scale, height=self.height*self.scale)
            # set max width height of image
            max_width = max(self.width*self.scale, self.column_width)
            max_height = max(self.height*self.scale, self.column_height)
            # canvas
            canvas = g.window['Column'].Widget.canvas
            canvas.configure(scrollregion=(0, 0, max_width, max_height))
        except Exception as e:
            print(e)

    @property
    # Gets information about image
    def data(self):
        try:
            # if scale is same, do nothing
            if self.scale == 1:
                im = self.im
            else:
                im = self.im.resize(
                    (int(self.width*self.scale), int(self.height*self.scale)),
                    resample=Image.NEAREST)
            with BytesIO() as output:
                im.save(output, format="PNG")
                data = output.getvalue()
            return data
        except Exception as e:
            print(e)

    # grey function
    def grey(self):
        try:
            im_grey = np.array(self.im.convert(mode="L"), dtype=np.uint8)
            im = np.array(self.im, dtype=np.uint8)
            return im, im_grey
        except Exception as e:
            print(e)

    # open file function
    def open_file(self):
        try:
            # if its the right file
            if self.filename and Path(self.filename).is_file():
                # open the image in PIL library
                self.im = Image.open(self.filename).convert(mode='RGBA')
                # get properties of it
                self.width, self.height = self.im.size
                # reset scale to 1
                #self.scale = 1
                # draw the image
                self.draw_image()
        except Exception as e:
            print(e)

    # remove function
    def remove(self):
        try:
            x, y = values['Graph']
            x, y = x//self.scale, y//self.scale
            image, image_grey = self.grey()
            pixel = image_grey[y, x]
            lst = [(x, y)]
            checked = set()
            while lst:
                tmp = set()
                for point in lst:
                    x1, y1 = point
                    if point not in checked:
                        checked.add((x1, y1))
                        if pixel-self.diff <= image_grey[y1, x1] <= pixel+self.diff:
                            image[y1, x1] = self.white
                            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                if 0<=x1+dx<self.width and 0<=y1+dy<self.height:
                                    tmp.add((x1+dx, y1+dy))
                lst = tmp
            self.im = Image.fromarray(image)
            self.draw_image()
        except Exception as e:
            print(e)

    # savesfile under filename
    def save_file(self):
        try:
            if self.key:
                filename = self.file(save=True)
                if filename:
                    g.im.save(filename)
        except Exception as e:
            print(e)

    # Zoom in function
    def zoom_in(self):
        try:
            # set scale up
            self.scale = min(self.scale+1, 10)
            # redraw image
            self.draw_image()
        except Exception as e:
            print(e)

    # Zoom out function
    def zoom_out(self):
        try:
            # set scale down 1
            self.scale = max(self.scale-1, 1)
            # draw image
            self.draw_image()
        except Exception as e:
            print(e)

    # called when folder selected, display Files function
    def displayFiles(self, values):
        # get the value of the folder
        self.folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            self.file_list = os.listdir(self.folder)
        # if theres an error (no files in there)
        except:
            # make the list empty
            self.file_list = []

        # take out all non .png/.gif
        self.fnames = [
            f
            for f in self.file_list
            if os.path.isfile(os.path.join(self.folder, f))
               and f.lower().endswith((".png", ".gif"))
        ]
        # update the file list
        self.window["-FILE LIST-"].update(self.fnames)

    # display image function called when image is clicked
    def displayImage(self, values):
        # try this
        try:
            # joins file path of folder and image for later use
            self.filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            # sets the list index for prev/next function
            self.listNum = self.fnames.index(values['-FILE LIST-'][0])
            # opens the image
            self.scale = 1
            self.open_file()
        # if theres an error, don't quit the program, just keep going
        except:
            pass

    # Previous image function
    def previousImage(self):
        # try this
        try:
            # if its the beginning of the list, set listnum to the end + 1
            if self.listNum == 0:
                self.listNum = len(self.fnames)
            # subtract one
            self.listNum -= 1
            # join file paths
            self.filename = os.path.join(
                values["-FOLDER-"], str(self.fnames[self.listNum])
            )
            # open new file
            self.open_file()

        except Exception as e:  # if theres an error, don't quit program, just print the error
            print(e)

    # go to next image
    def nextImage(self):
        # try this
        try:
            # if its the last element, set it to one below first
            if self.listNum == len(self.fnames) - 1:
                self.listNum = -1
            # add one to the listnum
            self.listNum+=1
            # join file paths
            self.filename = os.path.join(values["-FOLDER-"], str(self.fnames[self.listNum]))
            # open the file
            self.open_file()
        # if theres an error, don't quit, just print the error
        except Exception as e:
            print(e)

    def brighten(self):
        try:
            self.enhancer = ImageEnhance.Brightness(self.im)
            self.factor = 1.1
            self.output = self.enhancer.enhance(self.factor)
            self.output.save(self.filename)
            self.open_file()
        except Exception as e:
            print(e)

    def darken(self):
        try:
            self.enhancer = ImageEnhance.Brightness(self.im)
            self.factor = 0.9
            self.output = self.enhancer.enhance(self.factor)
            self.output.save(self.filename)
            self.open_file()
        except Exception as e:
            print(e)

    def search(self, values):
        try:
            self.results = values['-INPUT-']
            self.new_values = [x for x in self.fnames if self.results in x]
            self.window["-FILE LIST-"].update(self.new_values)
        except Exception as e:
            print(e)

# create an instance of the class
g = GUI()
# function list for each button/action
function = {'Open':g.open_file,  'Save':g.save_file, 'Graph':g.remove,
            'Zoom In':g.zoom_in, 'Zoom Out':g.zoom_out, '-FOLDER-':g.displayFiles,
            '-FILE LIST-':g.displayImage, "Previous":g.previousImage, "Next":g.nextImage,
            'Brighten':g.brighten, 'Darken':g.darken}
# main loop for program
while True:
    # get the events and values that happen every time
    event, values = g.window.read()
    # if that event is a close button, then close
    if event in (sg.WINDOW_CLOSED, 'Exit'):
        break
    elif values['-INPUT-'] != '':
        g.search(values)
    else:
        g.displayFiles(values)
    # if a new folder has opened, or file has been clicked, open the function but with parameter values passed in
    if '-FOLDER-' in event or '-FILE LIST-' in event:
        function[event](values)
    # if its any other function just call the function
    elif event in function:
        function[event]()

# when loop ends, close the program
g.window.close()
