import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import os
from PIL import Image

sg.theme('LightGrey')

class InternalError(Exception):
    pass

# Define the window's contents
layout = [ 
    [sg.Text("Select the images to resize and crop:", font=('', 25))],
    [sg.FilesBrowse(file_types=(("Image Files", "*.png;*.jpeg;*.jpg;*.webp"),), key="-INPUT_FILES-", font=('', 20), enable_events=True)],
    [sg.Listbox(values=[], size=(100, 10), key="-FILE_LISTBOX-")],

    # Image basenamess
    [sg.Text("Give basename for files:", font=('', 30))],
    [sg.InputText(font=('', 30), key="-BASENAME-")],

    # Checkboxes
    [sg.Checkbox("Stretch images? (default: centered)", font=('', 22), key="-IS_STRETCHED-"),
    sg.Checkbox("Use 1:1 aspect ratio?", font=('', 22), enable_events=True, key="-ONEBYONE-")],
    [sg.Checkbox("Use original image format? (default: jpeg)", font=('', 22), key="-USEINPUTFORMAT-")],

    # New resolutions for the images
    [sg.Text("New width:", font=('', 25)), sg.Spin(values=[i for i in range(1, 10000)], initial_value=500, key="-WIDTH-", font=('', 24))],
    [sg.Text("New height:", font=('', 25)), sg.Spin(values=[i for i in range(1, 10000)], initial_value=500, key="-HEIGHT-", font=('', 24))],

    # Color picker for the background
    [sg.Text("Background color in RGB.", font=('', 28))],
    [sg.Text("Used only in centered-mode.", font=('', 18), text_color="grey")],
    [sg.Text("RGB = 255, 255, 255 means white and 0, 0, 0 black.", font=('', 18), text_color="grey")],
    [sg.Text("Red", font=('', 25), text_color="red"), sg.Slider(range=(0, 255), default_value=255, orientation="h", size=(20, 20), pad=((200, 5)), key="-RED-")],
    [sg.Text("Green", font=('', 25), text_color="green"), sg.Slider(range=(0, 255), default_value=255, orientation="h", size=(20, 20), pad=((180, 5)), key="-GREEN-")],
    [sg.Text("Blue", font=('', 25), text_color="blue"), sg.Slider(range=(0, 255), default_value=255, orientation="h", size=(20, 20), pad=((200, 5)), key="-BLUE-")],

    # Destination folder
    [sg.Text("Select the destination folder:", font=('', 25)), sg.FolderBrowse(key="-OUTPUTFOLDER-", font=('', 20), target="-DESTINATION_PATH-")],
    [sg.Text("No path selected", font=('', 20), text_color="grey", key=("-DESTINATION_PATH-"))],

    # Action buttons
    [sg.Button("Run", font=('', 20)), sg.Button("Quit", font=('', 20))],
]

# Create the window
window = sg.Window("Renamecrop", layout, size=(1000, 800), resizable=True)

def resizeImagesCentered(input_files, basename, output_path, target_width, target_height, target_format, background_color):
    counter = 1
    # Iterate over a list of files
    for file in input_files:
        # Open the file
        with Image.open(file) as img:
            width = img.width
            height = img.height
            aspect_ratio = width / height
            new_aspect_ratio = target_width / target_height

            if aspect_ratio > new_aspect_ratio:
                # Image is wider, adjust height to fit
                new_width = target_width
                new_height = int(target_width / aspect_ratio)
            else:
                # Image is taller, adjust width to fit
                new_width = int(target_height * aspect_ratio)
                new_height = target_height
            # Create a new blank image with the desired size and fill it with the desired background color
            resized_image = Image.new("RGB", (target_width, target_height), background_color)

            # Paste the resized image onto the blank image, centered
            paste_x = (target_width - new_width) // 2
            paste_y = (target_height - new_height) // 2
            resized_image.paste(img.resize((new_width, new_height)), (paste_x, paste_y))

            img_format="jpeg"
            # Check the target format
            if target_format == True and img.format != None:
                img_format = img.format.lower()
                
            # Save the image with the counter as a suffix
            new_filename = f"{basename}_{counter}.{img_format}"
            resized_image.save(os.path.join(output_path, new_filename))

        counter += 1
    return counter

def resizeImagesStretched(input_files, basename, output_path, target_width, target_height, target_format):
    counter = 1
    # Iterate over a list of files
    for file in input_files:
        # Open the file
        with Image.open(file) as img:
            # Resize the image
            resized_image = img.resize((target_width, target_height))

            img_format="jpeg"
            # Check the target format
            if target_format == True and img.format != None:
                img_format = img.format.lower()

            # Save the image with the counter as a suffix
            new_filename = f"{basename}_{counter}.{img_format}"
            resized_image.save(os.path.join(output_path, new_filename))
        counter += 1

while True:

    event, values = window.read()

    if event == 'Quit' or event == sg.WIN_CLOSED:
        break

    elif event == 'Run':
        # Used to keep track of the selected files

        try:
            # Used to track the selection of files
            file_list = []
            base_name = values["-BASENAME-"]
            if base_name == "":
                raise InternalError("No basename given.")

            output_folder = values["-OUTPUTFOLDER-"]
            if output_folder == "":
                raise InternalError("No output folder selected.")

            background_color = (int(values["-RED-"]), int(values["-GREEN-"]), int(values["-BLUE-"]))
            is_stretched = values["-IS_STRETCHED-"]
            
            # Get the target image format
            target_format = values["-USEINPUTFORMAT-"]

            # Get the new size
            new_width = int(values["-WIDTH-"])
            if values["-ONEBYONE-"]:
                # One by one is true
                new_height = new_width
            else:
                # One by one is false, get the new height
                new_height = int(values["-HEIGHT-"])

            # Append the files from the -INPUT_FILES- field
            file_list = values["-INPUT_FILES-"].split(";")

            # Filter only image files
            selected_images = [file for file in file_list if file.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))]

            # Check if any images were selected
            if len(selected_images) <= 0:
                raise InternalError("No images selected.")

            # Execute the resizeImages on all of the images
            if is_stretched == True:
                resizeImagesStretched(selected_images, base_name, output_folder, new_width, new_height, target_format)
            else:
                resizeImagesCentered(selected_images, base_name, output_folder, new_width, new_height, target_format, background_color)
            
            # Success
            sg.popup("Files were resized and renamed")

        except InternalError as e:
            # Let the user continue using the program. Don't break the main loop.
            sg.popup_error(e, font=('', 32), title="Non-fatal Error", keep_on_top=True)
    
    # Appends the files into the general selected_files variable
    # And updates the file listbox
    elif event == "-INPUT_FILES-":
        file_list = values["-INPUT_FILES-"].split(";")
        window["-FILE_LISTBOX-"].update(file_list)

    elif event == "-ONEBYONE-":
        window["-HEIGHT-"].update(disabled=values["-ONEBYONE-"])

window.close()
