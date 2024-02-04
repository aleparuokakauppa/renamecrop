import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import os
from PIL import Image

sg.theme('LightGrey')

class InternalError(Exception):
    pass

# Define the window's contents
layout = [ 
    [sg.Text("Select the images to resize and crop", font=('', 30)),
    sg.FilesBrowse(file_types=(("Image Files", "*.png;*.jpeg;*.jpg;*.webp"),), key="-INPUTFILES-", font=('', 20))],
    [sg.Text("None selected", font=('', 25), text_color="grey", key="-COUNT-")],

    # Image basenamess
    [sg.Text("Give basename for files:", font=('', 30)), sg.InputText(font=('', 30), key="-BASENAME-")],

    # Checkboxes
    [sg.Checkbox("Stretch images? (default: centered)", font=('', 25), key="-IS_STRETCHED-"),
    sg.Checkbox("Use 1:1 aspect ratio?", font=('', 25), enable_events=True, key="-ONEBYONE-")],

    # New resolutions for the images
    [sg.Text("New width:", font=('', 25)), sg.Spin(values=[i for i in range(1, 10000)], initial_value=500, key="-WIDTH-", font=('', 24))],
    [sg.Text("New height:", font=('', 25)), sg.Spin(values=[i for i in range(1, 10000)], initial_value=500, key="-HEIGHT-", font=('', 24))],

    # Color picker for the background
    [sg.Text("Background color in RGB. Applicable only in centered-mode.", font=('', 28))],
    [sg.Text("RGB = 255, 255, 255 means white and 0, 0, 0 black.", font=('', 18), text_color="grey")],
    [sg.Text("Red", font=('', 25), text_color="red"), sg.Slider(range=(0, 255), orientation="h", size=(20, 20), pad=((200, 5)), key="-RED-")],
    [sg.Text("Green", font=('', 25), text_color="green"), sg.Slider(range=(0, 255), orientation="h", size=(20, 20), pad=((180, 5)), key="-GREEN-")],
    [sg.Text("Blue", font=('', 25), text_color="blue"), sg.Slider(range=(0, 255), orientation="h", size=(20, 20), pad=((200, 5)), key="-BLUE-")],

    # Destination folder
    [sg.Text("Select the destination folder:", font=('', 25)), sg.FolderBrowse(key="-OUTPUTFOLDER-", font=('', 20), target="-DESTINATION_PATH-")],
    [sg.Text("No path selected", font=('', 20), text_color="grey", key=("-DESTINATION_PATH-"))],

    # Action buttons
    [sg.Button("Run", font=('', 20)), sg.Button("Quit", font=('', 20))],
]

def resizeImagesCentered(input_files, basename, output_path, target_width, target_height, background_color):
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

            # Save the image with the counter as a suffix
            img_format = img.format
            if img_format is not None:
                img_format = img_format.lower()
            new_filename = f"{basename}_{counter}.{img_format}"
            resized_image.save(os.path.join(output_path, new_filename))
        counter += 1
    return counter

def resizeImagesStretched(input_files, basename, output_path, target_width, target_height):
    counter = 1
    # Iterate over a list of files
    for file in input_files:
        # Open the file
        with Image.open(file) as img:
            # Resize the image
            resized_image = img.resize((target_width, target_height))
            # Get the image format
            img_format = img.format
            if img_format is not None:
                img_format = img_format.lower()
            # Save the image with the counter as a suffix
            new_filename = f"{basename}_{counter}.{img_format}"
            resized_image.save(os.path.join(output_path, new_filename))
        counter += 1

# Create the window
window = sg.Window("Renamecrop", layout, size=(1000, 800))

while True:
    event, values = window.read()

    if event == 'Quit':
        break

    elif event == 'Run':
        try:
            selected_files = []
            # Define variables

            base_name = values["-BASENAME-"]
            if base_name == "":
                raise InternalError("No basename given.")

            output_folder = values["-OUTPUTFOLDER-"]
            if output_folder == "":
                raise InternalError("No output folder selected.")

            background_color = (int(values["-RED-"]), int(values["-GREEN-"]), int(values["-BLUE-"]))
            is_stretched = values["-IS_STRETCHED-"]
            # Get the new size
            new_width = int(values["-WIDTH-"])
            if values["-ONEBYONE-"]:
                # One by one is true
                new_height = new_width
            else:
                # One by one is false, get the new height
                new_height = int(values["-HEIGHT-"])

            # Append the files from the inputFolder to the selected_files[] list
            selected_files = values["-INPUTFILES-"].split(";")

            # Filter only image files
            selected_files = [file for file in selected_files if file.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))]

            # Check if any images were selected
            if len(selected_files) <= 0:
                raise InternalError("No images selected.")

            # Execute the resizeImages on all of the images
            if is_stretched == True:
                resizeImagesStretched(selected_files, base_name, output_folder, new_width, new_height)
            else:
                resizeImagesCentered(selected_files, base_name, output_folder, new_width, new_height, background_color)
            
            # Success
            sg.popup("Files were resized and renamed")

        except InternalError as e:
            # Let the user continue using the program. Don't break the main loop.
            sg.popup_error(e, font=('', 32), title="Non-fatal Error", keep_on_top=True)

    elif event == "-ONEBYONE-":
        window["-HEIGHT-"].update(disabled=values["-ONEBYONE-"])

window.close()
