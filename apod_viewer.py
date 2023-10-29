# APOD Viewer
import tkinter
from io import BytesIO
from tkinter import filedialog

import requests
import webbrowser
from PIL import Image
from PIL import ImageTk
from tkcalendar import DateEntry

# Define window
root = tkinter.Tk()
root.title('APOD Photo Viewer')

# Define fonts and colors
text_font = ('Times New Roman', 14)
nasa_blue = "#043c90"
nasa_light_blue = "#7aa5d3"
nasa_red = "#ff1923"
nasa_white = "#ffffff"
root.config(bg=nasa_blue)


# Define function
def get_request():
    """Get request data from nasa APOD API"""
    global response

    # set the parameter for the request
    url = ' https://api.nasa.gov/planetary/apod'
    api_key = 'zaLVmmSTquJhBhsHBzno4JJrqWeEXrRcwu7afI5E'
    date = calendar.get_date()
    querystring = {'api_key': api_key, 'date': date}
    # Call the request and turn it into a python usable form
    response = requests.request("GET", url, params=querystring)
    response = response.json()
    # print(response)
    # update output labels
    set_infor()


def set_infor():
    """Update output label base on the api call"""
    # example response
    '''{'copyright': 'Vikas Chander', 
      'date': '2023-03-21',
      'explanation': "Can dust be beautiful? Yes, and it can also be useful.  
      The Taurus molecular cloud has several bright stars, but it is the dark dust that really draws attention.  
      The pervasive dust has waves and ripples and makes picturesque dust bunnies, but perhaps more importantly,
       it marks regions where interstellar gas is dense enough to gravitationally contract to form stars. In the image 
       center is a light cloud lit by neighboring stars that is home not only to a famous nebula, but to a very young 
       and massive famous star.  Both the star, T Tauri, and the nebula, Hind's Variable Nebula, are seen to vary
        dramatically in brightness -- but not necessarily at the same time, adding to the mystery of this intriguing
         region. T Tauri and similar stars are now generally recognized to be Sun-like stars that are less than a few 
         million years old and so still in the early stages of formation. The featured image spans about four degrees
          not far from the Pleiades star cluster, while the featured dust field lies about 400 light-years away.", 
          
      'hdurl': 'https://apod.nasa.gov/apod/image/2303/TaurusDust_Chander_4096.jpg', 
      'media_type': 'image',
      'service_version': 'v1', 
      'title': 'Dark Nebulae and Star Formation in Taurus',
      'url': 'https://apod.nasa.gov/apod/image/2303/TaurusDust_Chander_1080.jpg'}'''

    # update the picture data and explanation
    picture_date.config(text=response['date'])
    picture_explanation.config(text=response['explanation'])

    # we need to use 3 images in other functions; an img, a thumb, and a full_img
    global img
    global thumb
    global full_img
    url = response['url']

    if response['media_type'] == 'image':
        # grab the photo that is stored in the our response

        img_response = requests.get(url, stream=True)
        # get the content of the response and use the BytesIO to open it as an image
        # keep a reference to this img as this is what we can use to save the image(Image not PhotoImage)
        # Create a full screen image for a second window
        img_data = img_response.content
        img = Image.open(BytesIO(img_data))

        full_img = ImageTk.PhotoImage(img)

        # Create the thumbnail for the main screen
        thumb_data = img_response.content
        thumb = Image.open(BytesIO(thumb_data))
        thumb.thumbnail((600, 600))
        thumb = ImageTk.PhotoImage(thumb)

        # set the thumbnail image
        picture_label.config(image=thumb)
    elif response['media_type'] == 'video':
        picture_label.config(text=url, image='')
        webbrowser.open(url)


def full_photo():
    """open the full size phot in a new window"""
    top = tkinter.Toplevel()
    top.title('Full ApOD Photo')

    # load the full image to the top window
    img_label = tkinter.Label(top, image=full_img)
    img_label.pack()


def save_photo():
    """Save the desire photo"""
    save_name = filedialog.asksaveasfilename(initialdir="./", title="save Image",
                                             filetypes=(("JPEG", "*.jpg"), ("All Files", "*.*")))
    img.save(save_name + ".jpg")


# define layouts
# create frames
input_frame = tkinter.Frame(root, bg=nasa_blue)
output_frame = tkinter.Frame(root, bg=nasa_white)
input_frame.pack()
output_frame.pack()
output_frame.pack(padx=50, pady=(0, 25))

# layout for the input_frame
calendar = DateEntry(input_frame, width=10, text=text_font, background=nasa_blue, foreground=nasa_white)
submit_button = tkinter.Button(input_frame, text="Submit", font=text_font, bg=nasa_light_blue, command=get_request)
full_button = tkinter.Button(input_frame, text="Full Photo", font=text_font, bg=nasa_light_blue, command=full_photo)
save_button = tkinter.Button(input_frame, text="Save Photo", font=text_font, bg=nasa_light_blue, command=save_photo)
quit_button = tkinter.Button(input_frame, text="Exit", font=text_font, bg=nasa_red, command=root.destroy)

#
calendar.grid(row=0, column=0, padx=5, pady=10)
submit_button.grid(row=0, column=1, padx=5, pady=10, ipadx=35)
full_button.grid(row=0, column=2, padx=5, pady=10, ipadx=25)
save_button.grid(row=0, column=3, padx=5, pady=10, ipadx=25)
quit_button.grid(row=0, column=4, padx=5, pady=10, ipadx=50)
# layout for the output fame
picture_date = tkinter.Label(output_frame, font=text_font, bg=nasa_white)
picture_explanation = tkinter.Label(output_frame, bg=nasa_white, font=text_font, wraplength=600)

picture_label = tkinter.Label(output_frame)
picture_date.grid(row=1, column=1, padx=10)
picture_explanation.grid(row=0, column=0, padx=10, pady=10, rowspan=2)
picture_label.grid(row=0, column=1, padx=10, pady=10)

# get today's photo to start with, this will valid till 12:00 pm midnight....around 12:00 upwards will enter a wait period
#for the new photo or video code is giving a keyerro....to rectify we comment out line 149 where the get_request()
#is called
get_request()
# run the root window's main loop
root.mainloop()
