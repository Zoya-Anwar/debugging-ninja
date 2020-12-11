# Runs on 1920 x 1080 screen resolution
# tested on the linux mint virtual machine
# checked using pep8 online checker http://pep8online.com/

# default gameplay settings:
# esc to escape program
# space bar to jump
# backspace to pause menu (where you can save game if you wish)
# control b to enter and exit the boss page
# semi colon to cheat once (+100 points, permenant no mr battery men spawn and
# slower speed)

from tkinter import *
from random import randint as rand
import math
import time
import datetime
import os
import pickle

SPEED = 15
w = 1920
h = 1080

score = None
jump_count = 0
pause = True
load_file_dir = None
xspeed = -5
name = ""

window = Tk()
window.option_add('*Font', 'Courier 20')
canvas = Canvas(window)
canvas.place(x=0, y=0, width=w, height=h)

background_image = PhotoImage(file="./images/background.png")
# https://fcit.usf.edu/matrix/project/circuit-board-background-slide-black/
character_image = PhotoImage(file="./images/character.png")
# https://www.newgrounds.com/art/view/slerpy/simple-pixel-character-teoh
bug_image = PhotoImage(file="./images/bug.png")
# https://www.newgrounds.com/art/view/slerpy/simple-pixel-character-teoh
diode_image = PhotoImage(file="./images/diode1.png")
# https://viikonvalo.fi/Open_Clip_Art_Library/
bat_image = PhotoImage(file="./images/mrbattery.png")
# https://commons.wikimedia.org/wiki/File:Battery-303889.svg

background = canvas.create_image(w/2, h/2, image=background_image)

objects = {'wire': None,
           'border': None,
           'ninja': canvas.create_image(300, 300, image=character_image),
           'bug': canvas.create_image(960, 540, image=bug_image),
           'diode': canvas.create_image(0, 0, image=diode_image),
           'battery': canvas.create_image(0, 0, image=bat_image)}


def initialConfigure():
    # configures all things that need to at the first start of program
    configureWindow()
    configureScore()
    configureObjects()
    configureCurrent()
    initialName()


def configureWindow():
    # makes window full screen and gives users an escape path during game play
    window.attributes('-fullscreen', True)
    window.update_idletasks()
    window.bind("<Escape>", lambda e: e.widget.quit())


def configureScore():
    # creates a score label for the game
    global score
    score = Label(canvas,
                  font="Courier 20",
                  width=10,
                  background="#01796F")
    score.pack(anchor="e")


def configureObjects():
    # sets initial values to objects used in the game

    global objects

    c = (0, 0, 0, 0)
    objects['wire'] = {'top': canvas.create_rectangle(c,
                                                      fill='green',
                                                      outline='green'),
                       'bottom': canvas.create_rectangle(c,
                                                         fill='green',
                                                         outline='green'),
                       'sw': canvas.create_rectangle(c,
                                                     fill='gold',
                                                     outline='gold')}
    top = (0, 0, w, 100,)
    bottom = (0, 980, w, h)
    objects['border'] = [canvas.create_rectangle(top, fill='Green',
                                                 outline='Green'),
                         canvas.create_rectangle(bottom, fill='Green',
                                                 outline='Green')]


def configureCurrent():
    # initialises the current to decorate the wire border
    up_c = [None]*18
    down_c = [None]*18

    for i in range(18):
        up = (50 + 108*i, 1005, 100 + 108*i, 1055)
        down = (50 + 108*i, 25, 100 + 108*i, 75)
        up_c[i] = canvas.create_oval(up, outline='#39ff14', fill='#39ff14')
        down_c[i] = canvas.create_oval(down, outline='#39ff14', fill='#39ff14')
    # sends a list of current balls to be animated
    animateCurrent(up_c + down_c)


def createFrame(display_text):
    # given text to display at the top, returns a styled Label Frame
    new_frame = LabelFrame(window,
                           fg="white",
                           text=display_text,
                           background="black")
    new_frame.place(x=0, y=0, width=w, height=h)

    return new_frame


def initialName():
    # Prompts user to enter their name within the text field.
    # They can leave it blank if they wish.
    name_frame = createFrame("Name")

    l = Label(name_frame,
              fg="White",
              bg="black",
              text="Please enter your name")
    l.pack(padx=5, pady=5)

    e = Entry(name_frame, bd=5)
    e.pack(padx=5, pady=5)

    button = Button(name_frame,
                    background="black",
                    fg="White",
                    text='Submit',
                    command=lambda: [getNameInput(e), startMenu()])
    button.pack(padx=5, pady=5)


def getNameInput(e):
    # gets input from Name field and stores it in the leaderboard
    global name
    name = e.get()
    e.pack_forget()


def startMenu():
    # creates a start menu by sending a dictionary of choices to menuPage
    start_menu_choices = {"Start": startGame,
                          "Exit": quit,
                          "View the leaderboard": leaderboard,
                          "Tutorial": tutorial,
                          "Options": configurationPage,
                          "Load a game": showSaves}

    menuPage(start_menu_choices, "Welcome to Debugging Ninja", "Green")


def menuPage(menu_choices, message, c):
    # gets a frame from createFrame called menu
    # creates buttons for each menu item and binds with corresponding commands

    menu = createFrame("Menu")

    output = Label(menu,
                   fg=c,
                   height=5,
                   text=message,
                   background="black",
                   font="Courier 40")
    output.pack()

    b = [None]*len(menu_choices)

    for i, key in enumerate(menu_choices):
        b[i] = Button(menu,
                      background="black",
                      fg=c,
                      text=key,
                      width=50,
                      height=2,
                      command=menu_choices[key])
        b[i].pack()


def tutorial():
    # gets a frame from createFrame called tut
    # Initial tutorial page, introduces the game

    tut = createFrame("Tutorial")

    Fact = ("Ninja needs your help debugging.\n\n"
            "There seems to be a lot of bugs in his computer. "
            "Can you help him?")

    T = Message(tut,
                background="black",
                width=w,
                fg="White",
                text=Fact,
                bd=40)

    confirm = Button(tut,
                     background="black",
                     fg="White",
                     text="Of course",
                     width=50,
                     height=2,
                     command=(lambda: [gameTutorial(T, tut),
                                       confirm.destroy()]))

    T.pack()
    confirm.pack(pady=30)


def gameTutorial(T, tut):
    # Comprehensive tutorial for the game

    fact = ("Great!\n\n"
            "Press space to jump up and down.\n\n"
            "You need to avoid the wires or you will be electrocuted. "
            "Press enter to melt holes in wires without holes.\n\n"
            "Collect the bugs when you see them. Some bugs are worth it, "
            "some will lead you to your death, make your decision well.\n\n"
            "Don't go shooting your laser without thinking. \n\n"
            "If you shoot a potential bug to catch because I'm a pacifist you "
            "loose bug points.\n\n"
            "If you accidently touch the lights "
            "you will burn the bugs you have"
            ", so be careful or you will loose points!\n\n"
            "Sometimes mr battery man might make an appearance: same"
            " deal as the wires but if you kill him because he's hoarding\n\n"
            "loads of bugs you get to keep them!\n\n"
            "Don't get scared when the speed "
            "starts increasing the more "
            "bugs you catch or more mr battery men spawn!")

    confirm = Button(tut,
                     background="black",
                     fg="White",
                     text="I read it all and want to go back to start",
                     width=50,
                     height=2,
                     command=startMenu)

    T.configure(text=fact, fg="Orange")
    confirm.pack(pady=30)


def startGame():
    # calls functions needed to start the game at each full reset

    scoreUpdate(0)
    Misc.lift(canvas)  # raises the gameplay canvas above the others
    resetValues()
    startMotion()


def resetValues():
    # resets values that should reset at start of the game
    # calls on functions to generate new random positions for objects

    global objects

    canvas.coords(objects['ninja'], 300, 300)
    generateBug()
    generateWire()
    generateDiode()
    initialiseBattery()


def startMotion():
    # starts the motion of the objects when starting/unpausing game
    # binds keys for user to move with and changes global pause

    window.after(SPEED, down)
    window.after(SPEED, animateBug)
    window.after(SPEED, animateWire)
    window.after(SPEED, animateDiode)
    window.after(SPEED, borderCollision)
    bindKeys()
    changePause()


def bindKeys():
    # binds keys users can use in the game, by iterating through a
    # global settings dictionary

    global settings

    for key, val in settings.items():
        window.bind(val, key)


def changePause():
    # global pause stops and starts all motion and collision detection

    global pause
    pause = not pause


def cheater(event=None):
    # when you cheat the xspeed permenantly becomes -3
    # you get an increase in score of 100
    # even if you increase your score further the speed will not increase
    # no mr battery men will spawn
    global xspeed
    scoreUpdate(100)
    xspeed = -4
    window.unbind("<semicolon>")


def scoreUpdate(a=None, b=0):
    # updates the score and increases difficulty depending on score
    # if user is at cheater speed, difficulty does not increase
    global xspeed

    if a == 0:
        new_score = 0
    else:
        new_score = int(score.cget("text"))
        if a is None:   # this will only happen on loading a save file
            new_score = b   # sets score to value save file saved
        else:
            new_score = new_score + a

    # if the xspeed is not the cheater speed
    if xspeed != -4:
        if new_score > 9:
            xspeed = -5 - 2 * (new_score // 10)
            # every time they score/loose points xspeed is -2 * score
            # the xspeed is set slower if they loose points, faster if gain
            if (new_score % 30 == 0):
                # if score is above threshold and a multiple of 30
                placeBattery()
        else:
            # if the score is less than 10 then xspeed is reset to -5
            xspeed = -5
    score.configure(text=(str(new_score)))


def collisionDetecter(object1, object2):
    # general purpose collision detector between two objects
    a = canvas.bbox(object1)
    b = canvas.bbox(object2)
    if a[0] in range(b[0], b[2]) or a[2] in range(b[0], b[2]):
        if a[1] in range(b[1], b[3]) or a[3] in range(b[1], b[3]):
            return True
    else:
        return False


def jump(event=None):
    # if player is inside canvas moves player up when button pressed
    global jump_count

    coords = canvas.coords(objects['ninja'])
    coords[1] -= 20

    if coords[1] <= 20:
        coords[1] = 20

    if not pause:
        if jump_count < 7:  # prevents player from shooting up
            canvas.coords(objects['ninja'], coords[0], coords[1])
            jump_count = jump_count + 1
            window.after(SPEED, jump)
        else:
            jump_count = 0


def down():
    # always moves player down
    coords = canvas.coords(objects['ninja'])
    coords[1] += 8  # less than jump movement so jump is registered

    if not pause:
        canvas.coords(objects['ninja'], coords[0], coords[1])
        window.after(SPEED, down)


def laser(event=None):
    # if player presses button a laser is released
    c = canvas.bbox(objects['ninja'])
    middle = (c[1] + c[3])/2  # placed in the middle of the player
    current_laser = canvas.create_oval(300, middle-5, 310, middle+5,
                                       outline='blue', fill='blue')
    animateLaser(current_laser)


def animateLaser(current_laser):
    # moves laser away from ninja
    # checks laser colliding with various objects
    # if colliding, there are different consequences

    endAnimate = False

    if not pause:

        laser_x_move = - xspeed * 5
        canvas.move(current_laser, laser_x_move, 0)
        if collisionDetecter(current_laser, objects['wire']['sw']):
            canvas.move(objects['wire']['sw'], -1000, -1000)
            endAnimate = True
        elif collisionDetecter(current_laser, objects['wire']['top']):
            endAnimate = True
        elif collisionDetecter(current_laser, objects['wire']['bottom']):
            endAnimate = True
        elif collisionDetecter(current_laser, objects['bug']):
            scoreUpdate(-10)
            generateBug()
        elif canvas.itemcget(objects['battery'], 'state') != 'hidden':
            if collisionDetecter(current_laser, objects['battery']):
                initialiseBattery()
                scoreUpdate(10)
        elif canvas.coords(current_laser)[2] > w:
            endAnimate = True

    # when laser collides it is deleted, else animation continues
    if not endAnimate:
        window.after(SPEED, lambda: animateLaser(current_laser))
    else:
        canvas.delete(current_laser)


def borderCollision():
    # if ninja collides with border game ends
    for a in objects['border']:
        if collisionDetecter(objects['ninja'], a):
            endMenu()
    if not pause:
        window.after(SPEED, borderCollision)


def animateCurrent(total_current):
    # animates the current which decorates the wire border, decorative
    if not pause:
        for c in total_current:
            coords = canvas.coords(c)
            coords[0] -= xspeed
            coords[2] -= xspeed
            if coords[2] > w:   # if out of bounds of canvas, resets value
                coords[0] = 50
                coords[2] = 100
            canvas.coords(c, coords[0], coords[1], coords[2], coords[3])

    window.after(SPEED, lambda: animateCurrent(total_current))


def generateDiode():
    # generates random coordinates for diode and moves diode
    height = rand(800, 950)
    offset = rand(400, 1400)
    wire_coords = canvas.coords(objects['wire']['top'])
    canvas.coords(objects['diode'], offset + wire_coords[2], height)
    collisionDiode()


def animateDiode():
    # moves diode towards ninja
    canvas.move(objects['diode'], xspeed, 0)
    if not pause:
        window.after(SPEED, animateDiode)


def collisionDiode(disable_diode=False):
    # if current diode colliding with ninja, penalty applied and disabled

    if not disable_diode:
        if collisionDetecter(objects['diode'], objects['ninja']):
            scoreUpdate(-10)
            disable_diode = True  # Prevents multiple penalties for 1 diode
            window.after(4000, collisionDiode)  # Resets disable_diode after 4s
        elif canvas.coords(objects['diode'])[0] < 0:  # If diode outside canvas
            generateDiode()
        else:
            window.after(SPEED, lambda: collisionDiode(disable_diode))


def generateBug():
    # generates random coordinates for bug and moves the bug
    bug_h = rand(20, h-100)
    canvas.coords(objects['bug'], w+500, bug_h)


def animateBug():
    # moves bug towards ninja and up and down in random directions (like a bug)
    # slightly faster than other objects in game
    # if wire colliding with bug it is moved
    # if bug colliding with ninja, score updated and bug disappears

    y_move = rand(-int(w*0.004), int(w*0.004))
    coords = canvas.coords(objects['bug'])
    canvas.move(objects['bug'], 1.1*xspeed, y_move)

    if collisionDetecter(objects['bug'], objects['ninja']):
        scoreUpdate(10)
        window.after(SPEED, generateBug)

    for key in objects['wire']:
        if collisionDetecter(objects['bug'], objects['wire'][key]):
            window.after(SPEED, generateBug)

    if coords[0] < 0 or coords[1] > 980 or coords[1] < 100:
        window.after(SPEED, generateBug)

    if not pause:
        window.after(SPEED, animateBug)


def generateWire():
    # generates random coordinates for wire top and bottom and moves
    # randomnly selects if wire switch will be in place or not

    while True:
        rand1 = rand(240, 840)
        rand2 = rand(240, 840)
        choose_switch = rand(0, 1)
        if (rand1 - rand2) < 600 and (rand1 - rand2) > 400:
            canvas.coords(objects['wire']['bottom'], 1680, h, 1920, rand1)
            canvas.coords(objects['wire']['top'], 1680, 0, 1920, rand2)
            if choose_switch == 1:
                canvas.coords(objects['wire']['sw'], 1680, rand2, 1920, rand1)
            else:
                canvas.coords(objects['wire']['sw'], 0, 0, 0, 0)
            break


def animateWire():
    # moves all sections of the wire towards ninja
    # if wire is out of bounds of canvas, sends it to be generated again
    # if ninja collides with wire, game ends
    coords = canvas.coords(objects['wire']['top'])

    for key in objects['wire']:
        canvas.move(objects['wire'][key], xspeed, 0)
        if collisionDetecter(objects['ninja'], objects['wire'][key]):
            endMenu()

    if (coords[2]) <= 0:
        generateWire()
    if not pause:
        window.after(SPEED, animateWire)


def initialiseBattery():
    # resets battery to initial values, ready for when difficulty increases
    canvas.coords(objects['battery'], 0, 0)
    canvas.itemconfig(objects['battery'], state=HIDDEN)
    print("Initialising battery")


def placeBattery():
    # places battery when not placement colliding with moving wire
    if canvas.itemcget(objects['battery'], 'state') != 'HIDDEN':
        wire = canvas.coords(objects['wire']['top'])
        if wire[0] > 1600:
            canvas.itemconfig(objects['battery'], state=NORMAL)
            canvas.coords(objects['battery'], wire[0]+600, 540)
            animateBattery()
            collisonBattery()
            callBatteryLaser()
        else:
            window.after(SPEED, placeBattery)


def animateBattery(y=xspeed):
    # moves the battery up and down and towards ninja
    # if battery is out of canvas bounds, it reverts back to a hidden battery
    if not pause and canvas.itemcget(objects['battery'], 'state') != 'hidden':
        bat_coords = canvas.bbox(objects['battery'])

        if bat_coords[3] < 200 or bat_coords[1] > 880:
            y = -y

        canvas.move(objects['battery'], xspeed, y)

        if bat_coords[0] < 0:
            initialiseBattery()

        window.after(SPEED, lambda: animateBattery(y))


def collisonBattery():
    # checks if ninja is colliding with battery, if it is then end of game
    if canvas.itemcget(objects['battery'], 'state') != 'hidden':
        if collisionDetecter(objects['battery'], objects['ninja']):
            initialiseBattery()
            endMenu()
        window.after(SPEED, collisonBattery)


def callBatteryLaser():
    # generates automatic lasers for the battery, every second
    batteryLaser()
    window.after(1000, callBatteryLaser)


def batteryLaser():
    # creates each laser ball
    if not pause and canvas.itemcget(objects['battery'], 'state') != 'hidden':
        c = canvas.bbox(objects['battery'])
        middle = (c[1] + c[3])/2
        current_laser = canvas.create_oval(c[0], middle-5, c[0]+5, middle+5,
                                           outline='red', fill='red')
        animateBatteryLaser(current_laser)


def animateBatteryLaser(current_laser):
    # moves each laser towards the ninja
    # if the ninja collides with the laser, score reduced
    # if laser out of bounds of canvas or battery hidden, it is deleted

    endAnimate = False

    if canvas.itemcget(objects['battery'], 'state') != 'hidden':
        if not pause:
            laser_speed = xspeed * 2
            canvas.move(current_laser, laser_speed, 0)
            if collisionDetecter(current_laser, objects['ninja']):
                canvas.delete(current_laser)
                print("Death by battery laser")
                scoreUpdate(-10)
                endAnimate = True
            elif canvas.coords(current_laser)[2] > w:
                canvas.delete(current_laser)
                print("Laser out of bounds")
                endAnimate = True

            if not endAnimate:
                window.after(SPEED, lambda: animateBatteryLaser(current_laser))

    else:
        canvas.delete(current_laser)


def unBindKeys():
    # unbinds keys user can use during the game by iterating through dictionary
    # for when user has paused/stopped game in various ways

    for value in settings.values():
        window.unbind(value)


def pauseMenu(event=None):
    # pauses game when button pressed, calls for menu page to create pause menu

    if not pause:  # otherwise you can pause in failure menu
        changePause()
        unBindKeys()
        pause_menu_choices = {"Play": unpause,
                              "Exit": quit,
                              "Return to start": startMenu,
                              "Tutorial": tutorial,
                              "Save game": saveGame}
        menuPage(pause_menu_choices, "You have paused the game", "Orange")
    else:
        startMenu()


def unpause():
    # unpauses the game, lifts gameplay canvas and calls for a timer

    Misc.lift(canvas)
    display_timer = Label(canvas,
                          text="Ready?",
                          font="Courier 70",
                          width=10,
                          background="Yellow")
    display_timer.pack()
    window.after(1000, lambda: timer(display_timer))


def timer(display_timer, sec=5):
    # counts down 5 seconds before starting game play again

    output = str(sec)
    print(sec)
    display_timer.configure(text=output)
    if sec > 0:
        # after every second call on function again
        window.after(1000, lambda: timer(display_timer, sec))
        sec = sec - 1
    else:  # until 0 seconds left
        display_timer.pack_forget()
        startMotion()


def endMenu():
    # displays failure message for 3 seconds and returns back to start menu
    unBindKeys()
    changePause()
    updateLeaderboard()

    if load_file_dir is not None:   # deletes save file if user used load file
        print(load_file_dir)
        os.remove(load_file_dir)

    ninja_coords = canvas.coords(objects['ninja'])

    explosion_image = PhotoImage(file="./images/explosion.png")
    # https://commons.wikimedia.org/wiki/File:Explosion-417894_icon.svg
    explosion = canvas.create_image(ninja_coords, image=explosion_image)
    canvas.image = explosion_image     # to prevent garbage collector :(

    message = Label(canvas,
                    text="You failed. Better luck next time!",
                    font="Courier 60",
                    background="Red")
    message.pack()

    window.after(3000, lambda: [canvas.delete(explosion),
                                message.pack_forget(),
                                startMenu()])


def saveGame():
    # saves current paused game into a pickle file with timestamp as file name

    ct = datetime.datetime.now()
    timestamp = (str(ct.timestamp())).split('.', 1)[0]
    file_name = "./saves/" + timestamp + ".dat"

    with open(file_name, 'wb') as f:
        pickle.dump([objects,
                     settings,
                     score['text'],
                     name,
                     jump_count], f, protocol=2)


def showSaves():
    # searches for any save files and displays them as buttons with a date

    load = createFrame("Load a save :)")
    search_path = "./saves/"

    b = []

    for i, fname in enumerate(os.listdir(path=search_path)):
        output = int(fname[:-4])
        output = datetime.datetime.fromtimestamp(output)
        b.append(Button(load,
                        background="black",
                        fg="white",
                        text=output,
                        width=50,
                        height=2,
                        command=lambda: [loadSave(fname),
                                         scoreUpdate(), unpause()]))
        b[i].pack()

    exit = Button(load,
                  background="black",
                  fg="white",
                  text="Return to Main Menu",
                  width=50,
                  height=2,
                  command=startMenu)
    exit.pack()


def loadSave(file_name):
    # loads a chosen save file and saves the appropriate global values

    global objects, settings, score, name, jump_count, load_file_dir

    load_file_dir = "./saves/" + file_name
    with open(load_file_dir, 'rb') as f:
        objects, settings, score['text'], name, jump_count = pickle.load(f)


def updateLeaderboard():
    # updates leaderboard when user dies

    current = int(score.cget("text"))
    file = open('leaderboard.txt', 'a')
    file.write(name + ":" + str(current) + "\n")
    file.close()


def leaderboard():
    # displays the top ten scores and names from a list of scores

    colours = ["Red", "Blue", "Green", "Yellow", "Purple", "Gold", "Orange",
               "Pink", "Brown", "White"]

    board = createFrame("Leaderboard!")
    board.option_add('*Font', 'Courier 24')  # font size is slightly bigger

    file_contents = []

    f = open('leaderboard.txt', 'r')

    for line in f.readlines():
        key, score = line.split(":")
        score = int(score.strip('\n'))
        # saves the name and score to a 2d list
        file_contents.append([key, score])
    f.close()

    # sorts the 2d list by score
    file_contents = sorted(file_contents, key=lambda l: l[1], reverse=True)

    r = 10

    # if there are less than 10 scores set r to the number of entries
    if r > len(file_contents):
        r = len(file_contents)

    for i in range(r):
        t = file_contents[i][0]
        v = file_contents[i][1]
        # if the name wasn't provided call them anonymous
        if t == "":
            t = "Anonymous"

        output = str(i+1) + ") " + t + " : " + str(v) + "\n"
        text = Label(board, text=output, fg=colours[i], bg="black")
        text.pack()

    board.option_add('*Font', 'Courier 20')  # reset back to normal font size

    b = Button(board, background="black", fg="White", text="Go back to Menu",
               height=3, width=20, command=startMenu)

    b.pack(padx=5, pady=5)


def configurationPage():
    # defines the different settings the user can change

    jump_options = {"Space bar": "<space>",
                    "UP key": "<Up>",
                    "W key": "<w>"}

    pause_options = {"Backspace": "<BackSpace>",
                     "P Key": "<p>"}

    laser_options = {"Return": "<Return>",
                     "Right": "<Right>",
                     "D key": "<d>"}

    configButton(jump_options, jump, "Jump")
    configButton(pause_options, pauseMenu, "Pause")
    configButton(laser_options,  laser, "Laser")


def configButton(setting, action, output):
    # creates a new page with a list of radio button options for a setting

    var = StringVar()
    var.set(settings[action])

    config = createFrame("Settings")

    output = Label(config,
                   fg="White",
                   height=5,
                   text=output,
                   background="black")
    output.pack()

    for key, value in setting.items():
        Radiobutton(config,
                    text=key,
                    pady=10,
                    width=20,
                    variable=var,
                    fg="green",
                    background="black",
                    value=value,
                    indicator=0).pack()

    b = Button(config,
               background="black",
               fg="White",
               text="Go to next setting",
               padx=10,
               width=24,
               command=lambda: [changeSetting(action, var.get()),
                                config.place_forget()]).pack()


def changeSetting(action, new_key):
    # unbinds any keys already set and changes the settings dictionary
    # will update when game starts

    window.unbind(settings[action])
    settings[action] = new_key


def bossKey(event=None):
    # the boss page, shows some educational information about debugging

    print("boss")
    changePause()

    boss = Frame(window,
                 background="white")
    boss.place(x=0, y=0, width=w, height=h)

    working_image = PhotoImage(file="./images/boss.png")
    # https://www.flickr.com/photos/topgold/2842497804/
    working = Label(boss, image=working_image,
                    borderwidth=0, highlightthickness=0)
    working.pack()
    working.image = working_image   # to prevent garbage collector :(

    text_image = PhotoImage(file="./images/boss_text.png")
    # https://en.wikipedia.org/wiki/Debugging
    text = Label(boss, image=text_image, outline=None,
                 borderwidth=0, highlightthickness=0)
    text.pack()
    text.image = text_image     # to prevent garbage collector :(

    window.unbind("<Control-b>")
    window.bind("<Control-b>", undoBoss)


def undoBoss(event=None):
    # sends user to the pause menu to unpause game after boss

    window.unbind("<Control-b>")
    window.bind("<Control-b>", bossKey)
    changePause()
    pauseMenu()

settings = {jump: "<space>",
            pauseMenu: "<BackSpace>",
            laser: "<Return>",
            cheater: "<semicolon>",
            bossKey: "<Control-b>"}

initialConfigure()
window.mainloop()
