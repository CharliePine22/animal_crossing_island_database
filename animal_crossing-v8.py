import matplotlib.pyplot as plt
matplotlib.use('Agg')
import tkinter
import webbrowser
import tkinter as tk
import os
from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
from functools import partial
from win32api import GetSystemMetrics
import bs4
import glob
import psycopg2 as pg2
import pandas as pds
import sys
import pygame

global grab_name

sys.setrecursionlimit(5000)
display_width = GetSystemMetrics(0)
display_height = GetSystemMetrics(1)

######################################### INITIALIZING GLOBAL VARIABLES #########################################

#   Initializing tkinter
root = Tk()
root.title('Animal Crossing Database')
geometry = "%dx%d" % (display_width, display_height)
root.geometry(geometry)
root.configure(background='cyan')
root.pack_propagate(0)
pygame.mixer.init()


def play():
    """Grab and play music file"""

    pygame.mixer.music.load(
        r"C:\Users\irush\Desktop\python projects\animal_crossing_database\Animal Crossing New Horizons OST - Main Theme 1 Hour Extended.mp3")
    pygame.mixer.music.play(loops=1)


def stop():
    """Function to stop the music"""
    pygame.mixer.music.stop()


#   Create empty lists to store names, personalities, species, and images of villagers
all_villager_names = []
all_villager_images = []
all_villager_species = []
all_villager_personalities = []
all_villager_catchphrases = []
types_of_hobbies = ['Nature', 'Fitness', 'Play', 'Education', 'Fashion', 'Music', 'Nature']
all_villager_hobbies = []


#   Path of AC Webpage
with open(r"C:\Users\irush\Desktop\python projects\animal_crossing_database\ac_villager_list.html", 'r', encoding='UTF-8') as f:
    page = f.read()

#   Loop through image files
for filename in glob.iglob(
        "\ac_villager_images" + '**/*.png',
        recursive=True):
    #   Resize all the images in the folder to be the same size
    img = Image.open(filename)
    resize = img.resize((306, 488), Image.ANTIALIAS)
    all_villager_images.append(resize)

######################################### DATA AND LOGIC #########################################

#   Beautiful soup selectors to locate and select specific selectors
soup = bs4.BeautifulSoup(page, 'lxml')
name = soup.select('table tbody b')
species = soup.findAll('a')
personalities = soup.findAll('a')
catchphrases = soup.findAll('i')
hobbies = soup.findAll('td')

#   Loop through all the anchor tags to find everything that has text in it
names_of_species = []
for test in species:
    if test.get('title') is not None:
        names_of_species.append(test.get('title'))

#   Had to append multiple times due to irregular names
species1 = names_of_species[64:600:3]
species2 = names_of_species[602:-212:3]
species3 = names_of_species[1080:1238:3]
all_villager_species.extend(species1)
all_villager_species.extend(species2)
all_villager_species.extend(species3)

#   Loop through names and add to names list
for i in name[1:]:
    all_villager_names.append(i.text)

#   Loop through all personalities to add to species list
for i in personalities[200::]:
    if i.text.startswith('♀') or i.text.startswith('♂'):
        all_villager_personalities.append(i.text[2:])

#   Loop through all villager catchphrases and append to list
for i in catchphrases[3:]:
    all_villager_catchphrases.append(i.text)

#   Dictionary holding name as key and species as value
complete_ac_list = dict(zip(all_villager_names, all_villager_species))

grab_name = ''
data_to_insert = []


def create_new_window():
    """Function to create new window upon calling"""

    top = Toplevel()
    top.geometry('1910x1080')
    top.configure(background='cyan')
    back_button = Button(top, text='Back', command=top.destroy, height=2, width=12)
    back_button.place(x=1000, y=950)
    return top


def verify_add_villager():
    """Function to create a new window when adding or removing to decrease user error"""

    top = create_new_window()
    top.title('Verification')
    top.geometry('300x150')
    alert = Label(top, text='Are you sure?', font=('Arial', 20), bg='cyan', fg='white')
    alert.place(x=55, y=25)
    yes = Button(top, text='Yes', width=10, command=lambda: [add_villager(), top.destroy()])
    yes.place(x=55, y=100)
    no = Button(top, text='No', width=10, command=top.destroy)
    no.place(x=165, y=100)


def web_info(villager_name):
    webbrowser.open("www.animalcrossing.fandom.com/wiki/" + str(villager_name), new=2)


def display_villager_info(villager_name):
    """Function to display the villager's information"""

    #   Try to open file and display data, if there are any errors, display them.
    try:
        villager = villager_name.title()  # Data value from the input

        #   Open file path and display image
        villager_img_filename = os.path.join(os.path.dirname(__file__), "ac_villager_images/{}.png".format(str(villager)))
        villager_img_path = Image.open(villager_img_filename)
        villager_img = ImageTk.PhotoImage(villager_img_path)

    except FileNotFoundError:
        print('FILE NOT FOUND')

    else:
        #   Configure new window
        top = create_new_window()
        top.attributes("-fullscreen", True)

        #   Display villager name
        villager_name = Label(master=top, text=villager.title(), bg='cyan', fg='white', font=('Arial', 50))
        villager_name.place(x=900, y=80)

        #   Label for Species
        species_label = Label(top, text='Species:', bg='cyan', fg='white', font=('Arial', 40))
        species_label.place(x=550, y=200)

        #   Grab species type
        species_type = Label(top, text=complete_ac_list[villager.title()], font=('Arial', 40), fg='white',
                             bg='cyan')
        species_type.place(x=780, y=203)

        #   Label for Personalities
        personality_label = Label(top, text='Personality: ', bg='cyan', fg='white', font=('Arial', 40))
        personality_label.place(x=550, y=400)

        #   Grab personality type
        personality_type = Label(top,
                                 text=all_villager_personalities[all_villager_names.index(str(villager.title()))],
                                 fg='white', bg='cyan', font=('Arial', 40))
        personality_type.place(x=845, y=403)

        #   Label for Catchphrases
        catchphrase_label = Label(top, text='Catchphrase: ', bg='cyan', fg='white', font=('Arial', 40))
        catchphrase_label.place(x=550, y=603)

        #   Grab villager catchphrase
        catchphrase = Label(top, text=all_villager_catchphrases[all_villager_names.index(str(villager.title()))],
                            bg='cyan', fg='white', font=('Arial', 40))
        catchphrase.place(x=870, y=606)

        #   Place image in new window
        villager_png = tkinter.Label(master=top, image=villager_img)
        villager_png.image = villager_img
        villager_png.place(x=100, y=200)

        #   Add Villager Button
        add_villager_button = Button(top, text='Add Villager', height=2, width=15,
                                     command=verify_add_villager)
        add_villager_button.place(x=775, y=950)

        #   Create a button that opens a tab in your browser to view more nfo.
        more_info = Button(top, text='More Info', command=partial(web_info, villager), height=2, width=12)
        more_info.place(x=190, y=725)

        global grab_name
        grab_name += villager
        data_to_insert.append(grab_name)
        data_to_insert.append(complete_ac_list[villager])
        data_to_insert.append(all_villager_personalities[all_villager_names.index(villager)])
        grab_name = ''

    E.delete(0, END)
    return villager_name


#   Main AC Title Image
filename = os.path.join(os.path.dirname(__file__), "ac_villager_images/ac_home_page.jfif")
img1 = Image.open(filename)
img1 = img1.resize((1000, 500), Image.ANTIALIAS)  # resize img
main_img = ImageTk.PhotoImage(img1)
label1 = tkinter.Label(image=main_img)
label1.image = main_img
label1.place(x=485, y=200)

#   Main AC Text
main_header = tkinter.Text(root, height=1, spacing1=1, width=46, bg='cyan', fg='white', bd=0)
main_header.configure(font=('Courier', 30))
main_header.place(x=430, y=100)
main_header.insert(tkinter.END, "Animal Crossing New Horizons Villager Database")

#   Main AC Entry
name_entry = Label(root, text='Name Of Villager:', font=('Times New Roman', 24), bg='cyan',
                   fg='white')  # Label showing name
name_entry.place(x=600, y=800)
E = Entry(root, width=40)  # Entry widget for entering villagers name
E.place(x=845, y=815)
E.bind("<Return>", (lambda event: display_villager_info(E.get())))

#   Play music button
play_button_file = os.path.join(os.path.dirname(__file__), "play-button.png")
play_button_img = Image.open(play_button_file)
play_button_img = play_button_img.resize((150, 100), Image.ANTIALIAS)
play_img = ImageTk.PhotoImage(play_button_img)
play_button = Button(root, text='Play', image=play_img, height=50, width=55, command=play)
play_button.place(x=10, y=10)

#   Stop music button
stop_button_file = os.path.join(os.path.dirname(__file__), "stop-button.png")
stop_button_img = Image.open(stop_button_file)
stop_button_img = stop_button_img.resize((150, 100), Image.ANTIALIAS)
stop_img = ImageTk.PhotoImage(stop_button_img)
stop_button = Button(root, text='Play', image=stop_img, height=50, width=50, command=stop)
stop_button.place(x=1840, y=10)

#   Submit Button
submit_button = Button(root, text='Submit', width=10, height=1, command=display_villager_info)
submit_button.place(x=1100, y=812)

#   Close the app
quit_app = Button(root, text='Quit', command=root.destroy, height=4, width=30)
quit_app.place(x=display_width * (5 / 7), y=900)

######################################### SQL BACKEND #########################################

secret = 'knight21'
conn = pg2.connect(database='animal_crossing', user='postgres', password=secret)
cur = conn.cursor()
cur.execute("SELECT * FROM villager_info")
data = cur.fetchall()
data_frame = pds.read_sql("select * from \"villager_info\"", conn)
dflist = data_frame.values.tolist()
pds.set_option('display.max_rows', len(data_frame))
conn.close()


def tree_double_click(action):
    """Function to allow user to double click on data in the tree"""

    villager_id = action.widget.focus()
    villager = action.widget.item(villager_id)
    villager_df = pds.DataFrame(villager['values']).transpose()
    villager_df.columns = ["Name", "Species", "Personality", "Hobby", "Birthday"]
    villager_to_pass = list(villager_df.itertuples(index=False, name=None))
    display_villager_info(villager_to_pass[0][0])


def create_filter_window():
    """Function to display filtered data"""

    top = create_new_window()
    top.attributes("-fullscreen", True)

    secret = 'knight21'
    conn = pg2.connect(database='animal_crossing', user='postgres', password=secret)
    cur = conn.cursor()
    cur.execute("SELECT * FROM villager_info")

    #   Label for filter option
    head = Label(top, text='Please select filter option:', bg='cyan', font=('Arial', 28))
    head.place(x=500, y=100)

    def grab_dropdown_value(event):
        """Grab combobox value"""

        if dropdown.get() == 'Hobby':

            cur.execute("SELECT * FROM villager_info ORDER BY hobby")
            #   Displaying table using a tree view
            tree = ttk.Treeview(top, column=("column1", "column2", "column3", "column4", "column5"), show='headings',
                                height=25)
            tree.heading("#1", text="Name")
            tree.heading("#2", text="Species")
            tree.heading("#3", text="Personality")
            tree.heading("#4", text="Hobby")
            tree.heading("#5", text="Birthday")
            tree.place(x=450, y=100)

            #   Configure the style of view
            style = ttk.Style()
            style.configure("Treeview.Heading", font=("Arial", 18, "bold"))
            style.configure("Treeview", font=("Arial", 14), rowheight=30, foreground='cyan')
            tree.tag_configure("oddrow", background="grey75")  # Background color for the odd rows
            tree.tag_configure("evenrow", background="snow")  # Background color for the even rows
            tree_count = 0
            data = cur.fetchall()

            for row in data[1:]:
                #   Loop through each row in the table
                if (tree_count % 2) == 0:
                    tree.insert("", tk.END, values=row,
                                tags=("oddrow",))  # Every odd row do something (change bg color)
                    tree_count += 1
                else:
                    tree.insert("", tk.END, values=row, tags=("evenrow",))
                    tree_count += 1
            conn.close()
            tree.bind("<Double-Button-1>", tree_double_click)

        elif dropdown.get() == 'Personality':

            cur.execute("SELECT * FROM villager_info ORDER BY personality")
            #   Displaying table using a tree view
            tree = ttk.Treeview(top, column=("column1", "column2", "column3", "column4", "column5"), show='headings',
                                height=25)
            tree.heading("#1", text="Name")
            tree.heading("#2", text="Species")
            tree.heading("#3", text="Personality")
            tree.heading("#4", text="Hobby")
            tree.heading("#5", text="Birthday")
            tree.place(x=450, y=100)

            #   Configure the style of view
            style = ttk.Style()
            style.configure("Treeview.Heading", font=("Arial", 18, "bold"))
            style.configure("Treeview", font=("Arial", 14), rowheight=30, foreground='cyan')
            tree.tag_configure("oddrow", background="grey75")  # Background color for the odd rows
            tree.tag_configure("evenrow", background="snow")  # Background color for the even rows
            tree_count = 0
            data = cur.fetchall()

            for row in data[1:]:
                #   Loop through each row in the table
                if (tree_count % 2) == 0:
                    tree.insert("", tk.END, values=row,
                                tags=("oddrow",))  # Every odd row do something (change bg color)
                    tree_count += 1
                else:
                    tree.insert("", tk.END, values=row, tags=("evenrow",))
                    tree_count += 1
            conn.close()
            tree.bind("<Double-Button-1>", tree_double_click)

        elif dropdown.get() == 'Species':

            cur.execute("SELECT * FROM villager_info ORDER BY species")
            #   Displaying table using a tree view
            tree = ttk.Treeview(top, column=("column1", "column2", "column3", "column4", "column5"), show='headings',
                                height=25)
            tree.heading("#1", text="Name")
            tree.heading("#2", text="Species")
            tree.heading("#3", text="Personality")
            tree.heading("#4", text="Hobby")
            tree.heading("#5", text="Birthday")
            tree.place(x=450, y=100)

            #   Configure the style of view
            style = ttk.Style()
            style.configure("Treeview.Heading", font=("Arial", 18, "bold"))
            style.configure("Treeview", font=("Arial", 14), rowheight=30, foreground='cyan')
            tree.tag_configure("oddrow", background="grey75")  # Background color for the odd rows
            tree.tag_configure("evenrow", background="snow")  # Background color for the even rows
            tree_count = 0
            data = cur.fetchall()

            for row in data[1:]:
                #   Loop through each row in the table
                if (tree_count % 2) == 0:
                    tree.insert("", tk.END, values=row,
                                tags=("oddrow",))  # Every odd row do something (change bg color)
                    tree_count += 1
                else:
                    tree.insert("", tk.END, values=row, tags=("evenrow",))
                    tree_count += 1
            conn.close()
            tree.bind("<Double-Button-1>", tree_double_click)

    dropdown = ttk.Combobox(top, width=35, height=4, values=['Personality', 'Hobby', 'Species'])
    dropdown.place(x=920, y=120)
    dropdown.bind("<<ComboboxSelected>>", grab_dropdown_value)


def view_all_villagers():
    """Function to open a new window to display all villager info"""

    #   Create new window and label heading
    top = create_new_window()
    display_heading = Label(top, text='All Villagers', font=('Courier', 46), bg='cyan', fg="white")
    display_heading.place(x=700, y=20)
    top.attributes("-fullscreen", True)

    #   Connect to SQL database and grab data
    secret = 'knight21'
    conn = pg2.connect(database='animal_crossing', user='postgres', password=secret)
    cur = conn.cursor()
    cur.execute("SELECT * FROM villager_info")

    #   Displaying table using a tree view
    tree = ttk.Treeview(top, column=("column1", "column2", "column3", "column4", "column5"), show='headings', height=25)
    tree.heading("#1", text="Name")
    tree.heading("#2", text="Species")
    tree.heading("#3", text="Personality")
    tree.heading("#4", text="Hobby")
    tree.heading("#5", text="Birthday")
    tree.place(x=450, y=100)

    #   Configure the style of view
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 18, "bold"))
    style.configure("Treeview", font=("Arial", 14), rowheight=30, foreground='cyan')
    tree.tag_configure("oddrow", background="grey75")  # Background color for the odd rows
    tree.tag_configure("evenrow", background="snow")  # Background color for the even rows
    tree_count = 0
    data = cur.fetchall()

    for row in data[1:]:
        #   Loop through each row in the table
        if (tree_count % 2) == 0:
            tree.insert("", tk.END, values=row, tags=("oddrow",))  # Every odd row do something (change bg color)
            tree_count += 1
        else:
            tree.insert("", tk.END, values=row, tags=("evenrow",))
            tree_count += 1
    conn.close()
    tree.bind("<Double-Button-1>", tree_double_click)

    #   Open up menu with drop-down bar to filter
    filter_info = Button(top, text='Filter', height=2, width=12, command=create_filter_window)
    filter_info.place(x=800, y=950)


#   List all villager Button
view_all = Button(root, text='View All Villagers', height=4, width=30, command=view_all_villagers)
view_all.place(x=display_width * (3 / 7), y=900)


def island_data():
    """Function to return data to determine if villager is on island"""

    villager_data = []
    current_villagers = []

    secret = 'knight21'
    conn = pg2.connect(database='animal_crossing', user='postgres', password=secret)
    cur = conn.cursor()

    #   Select the data from current island and grab hobbies from main database to merge and display
    cur.execute("""SELECT villager_info.name, island_villagers.species, island_villagers.personality, villager_info.hobby, island_villagers.date_joined  
    FROM villager_info 
    LEFT JOIN island_villagers
    ON island_villagers.name = villager_info.name
    WHERE island_villagers.species IS NOT NULL""")

    data = cur.fetchall()

    for row in data:
        villager_data.append(row)

    conn.close()

    #   Loop through villager data to get individual values for use later
    for villager in villager_data:
        for values in villager:
            current_villagers.append(values)

    return current_villagers


def view_island_info():
    """Function to display island villager information"""

    #   Create new window
    display = create_new_window()
    display.attributes("-fullscreen", True)
    #   Heading for the window
    island_heading = Label(display, text="Current Island Villagers", font=('Times New Roman', 46), bg='cyan',
                           fg="white")
    island_heading.place(x=650, y=110)

    #   SQL CONNECTION
    secret = 'knight21'
    conn = pg2.connect(database='animal_crossing', user='postgres', password=secret)
    cur = conn.cursor()

    #   Select the data from current island and grab hobbies from main database to merge and display
    cur.execute("""SELECT villager_info.name, island_villagers.species, island_villagers.personality, villager_info.hobby, island_villagers.date_joined  
    FROM villager_info 
    LEFT JOIN island_villagers
    ON island_villagers.name = villager_info.name
    WHERE island_villagers.species IS NOT NULL LIMIT 10""")

    #   Displaying table using a tree view
    tree = ttk.Treeview(display, column=("column1", "column2", "column3", "column4", "column5"), show='headings',
                        height=10)
    #   Making sure the headings align with data headings
    tree.heading("#1", text="Name")
    tree.heading("#2", text="Species")
    tree.heading("#3", text="Personality")
    tree.heading("#4", text="Hobby")
    tree.heading("#5", text="Date_Of_Arrival")
    tree.place(x=450, y=250)

    #   Configure the style of view
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 18, "bold"), foreground='black')
    style.configure("Treeview", font=("Arial", 15), rowheight=60, foreground='cyan', bordercolor='cyan')
    tree.tag_configure("oddrow", background="grey75")  # Background color for the odd rows
    tree.tag_configure("evenrow", background="snow")  # Background color for the even rows
    tree_count = 0
    data = cur.fetchall()

    for row in data:
        #   Loop through each row in the table
        if (tree_count % 2) == 0:
            tree.insert("", tk.END, values=row, tags=("oddrow",))  # Every odd row do something (change bg color)
            tree_count += 1

        else:
            tree.insert("", tk.END, values=row, tags=("evenrow",))  # Every even row do something
            tree_count += 1

    button1 = Button(display, text='Remove Villager', height=2, command=delete_villager_window)
    button1.place(x=800, y=950)
    tree.bind("<Double-Button-1>", tree_double_click)

    conn.close()


def add_villager():
    """Function that will add villager information to current villager database"""

    #   Creating window to inform user of retrieval success or failure
    alert_window = Toplevel()
    alert_window.title('Alert')
    alert_window.geometry('300x50')

    #   Connect to SQL
    secret = 'knight21'
    conn = pg2.connect(database='animal_crossing', user='postgres', password=secret)

    #   For grabbing data in the all_villagers database
    cur = conn.cursor()
    cur.execute('SELECT * FROM villager_info')
    data = cur.fetchall()

    #   Grab all the data
    postgrest_insert_query = "INSERT INTO island_villagers(name, species, personality, date_joined) VALUES (%s, %s, %s, CURRENT_TIMESTAMP) ON CONFLICT(name) DO UPDATE SET name=island_villagers.name"

    #   Commit to database
    try:
        print(data_to_insert)
        cur.execute(postgrest_insert_query, data_to_insert)

        if data_to_insert[0] in island_data():
            display = Label(alert_window, text=data_to_insert[0] + " is already on your island!")
            display.pack()

        else:
            success = Label(alert_window, text=data_to_insert[0] + " has been successfully added to your island!")
            success.pack()

    except IndexError:
        print('NOPE')

    conn.commit()
    conn.close()
    data_to_insert.pop()
    data_to_insert.pop()
    data_to_insert.pop()


delete_villager_name = ''


def grab_entry(en):
    global delete_villager_name
    name = en.get().title()
    delete_villager_name = name
    en.delete(0, END)
    return name


def delete_villager():
    """Removing villager from island"""

    global delete_villager_name
    curr_villagers = []
    curr_villagers.extend(island_data())
    print(delete_villager_name)

    if delete_villager_name in curr_villagers:

        top = Toplevel()

        secret = 'knight21'
        conn = pg2.connect(database='animal_crossing', user='postgres', password=secret)
        cur = conn.cursor()
        cur.execute("DELETE FROM island_villagers WHERE name = %s", [delete_villager_name])
        conn.commit()
        conn.close()
        success = Label(top, text=delete_villager_name + " has been successfully removed from your island!")
        success.pack()

    else:

        top = Toplevel()

        display = Label(top, text=delete_villager_name + " is not on your island!")
        display.pack()


def delete_villager_window():
    """Display remove villager window"""

    top = Toplevel()
    top.geometry('500x250')

    l = Label(top, text="Please type the villager, you'd like to remove")
    l.pack()

    e = Entry(top, width=30)
    e.pack()
    e.bind("<Return>", (lambda event: [grab_entry(e), delete_villager()]))

    submit = Button(top, text='Submit', width=10, height=2, command=lambda: [grab_entry(e), delete_villager()])
    submit.pack()


#   Label and placement for button to view current islanders
current_island_info = Button(root, text='View Island Info', height=4, width=30, command=view_island_info)
current_island_info.place(x=display_width * (1 / 7), y=900)

play()
root.attributes("-fullscreen", True)
root.mainloop()

