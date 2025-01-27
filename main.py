import time
import pytesseract
from PIL import Image, ImageOps
import mss
import numpy as np
from re import search
import threading

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

r_top = 880
r_left = 10
r_width = 520
r_height = 165
region = {"top": 880, "left": 10, "width": 520, "height": 165}

archive = [
    ('START', 0)
]
meter_type = 0

running = False

def save_logs():
    with open('logs.txt', 'w') as f:
        f.write(''.join(archive))

def show_logs():
    print('\n'.join(["[ " + s + " ] : " + str(n) + "" for (s, n) in archive[1:]]))

def show_skill_logs():
    tmp = {}
    for (s, n) in archive[1:]:
        if s in tmp:
            tmp[s] += n
        else:
            tmp[s] = n

    print('\n'.join(["[ " + s + " ] : " + str(n) + "" for (s, n) in {key: tmp[key] for key in sorted(tmp.keys())}.items()]))

def compare_logs(arr):
    global running
    if not running:
        return
    
    global archive

    l = len(arr)

    if l < 1:
        return

    stop_index = l
    archive_index = -1
    for i in range(l - 1, -1, -1):
        if arr[i] == archive[archive_index]:
            archive_index -= 1
        else:
            stop_index = i
            archive_index = -1
    
    res = arr[stop_index:]
    archive += res

        # print("AVG: ", np.mean(arr[stop_index:]), " SUM: ", np.sum(arr[stop_index:]))
        
    sum = 0
    for (s, x) in res:
        sum += x
    print("DMG: ", sum)

def process_text(content):
    global running
    if not running:
        return
    splited = content.replace("\n", " ").replace("[Combat]", " [Combat] ").replace("[Reward]", " [Reward] ").replace("[Item]", " [Item] ")
    words = splited.split(" ")

    logs = []
    is_mine = False
    is_combat = False
    dmg_type = None

    skill_start_index = 0
    skill_end_index = 0

    for (index, w) in enumerate(words):

        if w == '[Combat]':
            is_combat = True
            continue
        if w == 'Your':
            is_mine = True
            skill_start_index = index + 1
            continue
        if meter_type == 1 and search('heal', w):
            dmg_type = 'heal'
            skill_end_index = index
            continue
        if meter_type == 0 and search('damage', w):
            dmg_type = 'damage'
            skill_end_index = index
            continue
        if w.isnumeric() and is_combat and is_mine and ((meter_type == 0 and dmg_type == 'damage') or (meter_type == 1 and dmg_type == 'heal')):
            is_combat = False
            is_mine = False
            skill = ' '.join(words[skill_start_index:skill_end_index])
            if skill == '' or skill == ' ' or skill == None: continue
            logs.append((skill, (int(w))))
            skill_start_index = None
            dmg_type = None
            continue
    

    compare_logs(logs)

def capture_dps(time_interval):
    global running
    global region

    with mss.mss() as sct:
        while running:
            screenshot = sct.grab(region)
            
            image = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
            inverted_image = ImageOps.invert(image.convert("RGB"))

            scaled_image = inverted_image.resize((image.width * 2, image.height * 2))

            custom_config = r'--oem 3 --psm 6'

            text = pytesseract.image_to_string(scaled_image, config=custom_config)
            
            if text.strip():
                process_text(text.strip())

            

            time.sleep((time_interval / 1000))

def get_screenshot(region, show_text = False):
    with mss.mss() as sct:
        screenshot = sct.grab(region)
        image = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)

        if not show_text:
            image.show()

        if show_text:
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(image, config=custom_config)
            print(text.strip())

def start(interval = 1000):
    global running
    if not running:
        running = True

        params = {'time_interval': interval}
        thread = threading.Thread(target=capture_dps, kwargs=params)
        thread.daemon = True
        thread.start()

        print("Starting to capture DPS")
    else:
        print("Already running.")

def stop():
    global running

    running = False

    print("Stopped the DPS meter.")


def simple_repl():
    print("REPL is running...")
    
    while True:
        try:

            # Read input from the user
            command = input(">>> ").strip().lower()
            
            # If the user types 'exit', break the loop
            if command == "exit":
                print("Exiting REPL. Goodbye!")
                break
            elif command == 'stop':
                stop()
            
            elif command == "start":

                print("1: Damage, 2: Healing")

                meter_type = input(">>> ")

                if meter_type == "1":
                    meter_type = 0
                elif meter_type == "2":
                    meter_type = 1

                print("Input capturing interval in ms - min: 300 ms, default 1000 ms, press Enter for default")
                capturing_interval = input(">>> ")

                if capturing_interval == "":
                    start()
                    continue

                if capturing_interval.isnumeric():
                    if int(capturing_interval) >= 300:
                        start(int(capturing_interval))
                        continue
                    else:
                        print('Invalid number')
                else:
                    print('Invalid number')
            
            elif command == "test":
                print("Capturing screenshot")
                get_screenshot(region)
            
            elif command == "text":
                print("Running OCR through screenshot")
                get_screenshot(region, True)
            
            elif command == "save logs":
                print("Saving logs to file")
                save_logs()
            
            elif command == "show":
                print("1: Group by skills  2: All logs")
                input1 = input(">>> ").strip().lower()
                
                if input1 == "1":
                    show_skill_logs()
                elif input1 == "2":
                    show_logs()

            elif command == "settings":
                print("Top: ", region["top"], " Left: ", region["left"], " Width: ", region["width"], " Height: ", region["height"])
            
            elif command == "set":
                print("t: top, l: left, w: width, h: height")
                input1 = input(">>> ").strip().lower()
                print("Amount")
                input2 = input(">>> ")

                if input1 == "t":
                    region["top"] = int(input2)
                elif input1 == "l":
                    region["left"] = int(input2)
                elif input1 == "w":
                    region["width"] = int(input2)
                elif input1 == "h":
                    region["height"] = int(input2)

                print("Changed settigns")
        
        except Exception as e:
            # Handle any exceptions that occur
            print(f"Error: {e}")

simple_repl()
