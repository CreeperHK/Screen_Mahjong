import logging
import tkinter as tk
from tkinter import Frame, Label, Tk, ttk
from ultralytics import YOLO
import cv2
import numpy as np
import mss
import time
import gc
import tkinter as tk
from tkhtmlview import HTMLLabel

from name_corr import int_corr_str
from mah import calc_shanten_14
from cs_mah import call

logging.getLogger('ultralytics').setLevel(logging.WARNING)
model = YOLO('outputs/weights/best.pt')

sct = mss.mss()
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

output_width = 640
output_height = 480

running = True

def stop_running(event):
    global running
    running = False

def str_to_maj(s):
    lists = {
        'm': [],
        's': [],
        'p': [],
        'z': []
    }
    
    for i in range(0, len(s), 2):
        char = s[i + 1]
        number = s[i]
        
        if char in lists:
            lists[char].append(number)
        
    return_str = ''
    
    if lists['m'] != []:
        m_str = ''.join(lists['m'])
        return_str += m_str + 'm'
    if lists['p'] != []:
        p_str = ''.join(lists['p'])
        return_str += p_str + 'p'
    if lists['s'] != []:
        s_str = ''.join(lists['s'])
        return_str += s_str + 's'
    if lists['z'] != []:
        z_str = ''.join(lists['z'])
        return_str += z_str + 'z'

    return return_str

def correct_names(name_need_correct, name_mapping):
    return [name_mapping.get(item, item) for item in name_need_correct]

def whole_screen():
    try:
        img = sct.grab(monitor)
        img_np = np.array(img)
        img_np = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)

        img_np = cv2.resize(img_np, (960, 540))
        height, width, _ = img_np.shape
    except (mss.ScreenShotError, UnboundLocalError):
        return False, None
    
    roi_percentages = (0.0, 0.0, 1.0, 1.0)
    y1 = int(height * roi_percentages[0])
    x1 = int(width * roi_percentages[1])
    y2 = int(height * roi_percentages[2])
    x2 = int(width * roi_percentages[3])

    results = model(img_np)
    whole_screen_return = []

    for result in results:
        img_with_boxes = result.plot()
        filtered_detections = [
            (box, conf, cls) for box, conf, cls in zip(result.boxes.xyxy, result.boxes.conf, result.boxes.cls)
            if (box[0] >= x1 and box[1] >= y1 and box[2] <= x2 and box[3] <= y2 and conf >= 0.5)
        ]

        for box, conf, cls in filtered_detections:
            x1_box, y1_box, x2_box, y2_box = map(int, box)
            class_name = result.names[int(cls)]
            cv2.rectangle(img_with_boxes, (x1_box, y1_box), (x2_box, y2_box), (0, 255, 0), 2)
            cv2.putText(img_with_boxes, f'{class_name}', (x1_box, y1_box - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            whole_screen_return.append(f'{class_name}')

        cv2.rectangle(img_with_boxes, (x1, y1), (x2, y2), (255, 0, 0), 2)

    img_with_boxes_resized = cv2.resize(img_with_boxes, (output_width, output_height))
    cv2.imshow('Mahjong Detection', img_with_boxes_resized)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        return None, None

    del img_np, img_with_boxes
    gc.collect()

    return True, whole_screen_return

def hand_tile_read():
    try:
        img = sct.grab(monitor)
        img_np = np.array(img)
        img_np = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)

        img_np = cv2.resize(img_np, (960, 540))
        height, width, _ = img_np.shape
    except (mss.ScreenShotError, UnboundLocalError):
        return False, None
    
    roi_percentages = (0.8, 0.13, 1.0, 0.99)
    y1 = int(height * roi_percentages[0])
    x1 = int(width * roi_percentages[1])
    y2 = int(height * roi_percentages[2])
    x2 = int(width * roi_percentages[3])
    
    results = model(img_np)
    hand_tile_return = []
    hand_off = []

    for result in results:
        img_with_boxes = result.plot()
        filtered_detections = [
            (box, conf, cls) for box, conf, cls in zip(result.boxes.xyxy, result.boxes.conf, result.boxes.cls)
            if (box[0] >= x1 and box[1] >= y1 and box[2] <= x2 and box[3] <= y2 and conf >= 0.5)
        ]

        for box, conf, cls in filtered_detections:
            x1_box, y1_box, x2_box, y2_box = map(int, box)
            class_name = result.names[int(cls)]
            cv2.rectangle(img_with_boxes, (x1_box, y1_box), (x2_box, y2_box), (0, 255, 0), 2)
            cv2.putText(img_with_boxes, f'{class_name}', (x1_box, y1_box - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            hand_tile_return.append(f'{class_name}')

            width_box = x2_box - x1_box
            height_box = y2_box - y1_box
            if height_box >= 1.25 * width_box:
                orientation = "hand"
            else:
                orientation = "off"
            
            hand_off.append(f'{class_name} ({orientation})')
        
        furo_set = set()
        for item in hand_off:
            if 'off' in item:
                value = item.split(' ')[0]
                furo_set.add(int(value))
            
        furo_list = list(furo_set)

        cv2.rectangle(img_with_boxes, (x1, y1), (x2, y2), (255, 0, 0), 2)

    img_with_boxes_resized = cv2.resize(img_with_boxes, (output_width, output_height))
    cv2.imshow('Mahjong Detection', img_with_boxes_resized)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        return None, None

    del img_np, img_with_boxes
    gc.collect()

    return True, hand_tile_return, furo_list

def hand_off_read():
    try:
        img = sct.grab(monitor)
        img_np = np.array(img)
        img_np = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)

        img_np = cv2.resize(img_np, (960, 540))
        height, width, _ = img_np.shape
    except (mss.ScreenShotError, UnboundLocalError):
        return False, None
    
    roi_percentages = (0.5, 0.39, 0.9, 0.59)
    y1 = int(height * roi_percentages[0])
    x1 = int(width * roi_percentages[1])
    y2 = int(height * roi_percentages[2])
    x2 = int(width * roi_percentages[3])

    results = model(img_np)
    hand_off_return = []

    for result in results:
        img_with_boxes = result.plot()
        filtered_detections = [
            (box, conf, cls) for box, conf, cls in zip(result.boxes.xyxy, result.boxes.conf, result.boxes.cls)
            if (box[0] >= x1 and box[1] >= y1 and box[2] <= x2 and box[3] <= y2 and conf >= 0.5)
        ]

        for box, conf, cls in filtered_detections:
            x1_box, y1_box, x2_box, y2_box = map(int, box)
            class_name = result.names[int(cls)]
            cv2.rectangle(img_with_boxes, (x1_box, y1_box), (x2_box, y2_box), (0, 255, 0), 2)
            cv2.putText(img_with_boxes, f'{class_name}', (x1_box, y1_box - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            hand_off_return.append(f'{class_name}')

        cv2.rectangle(img_with_boxes, (x1, y1), (x2, y2), (255, 0, 0), 2)

    img_with_boxes_resized = cv2.resize(img_with_boxes, (output_width, output_height))
    cv2.imshow('Mahjong Detection', img_with_boxes_resized)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        return None, None

    del img_np, img_with_boxes
    gc.collect()

    return True, hand_off_return

def determine_strategy(game_process, distance_ron_value):
    if game_process == "Beginning":
        strategy = 'Offense1'
        summary = 'In the early game,\n you can Offense boldly'
    elif game_process == 'Middle' and distance_ron_value == 'Tingpai':
        strategy = 'Offense2'
        summary = 'Strong Offense recommended'
    elif game_process == 'Final' and distance_ron_value == 'Tingpai':
        strategy = 'Balance1'
        summary = 'Game is about to end,\n Maintaining Hand Tiles Value'
    elif game_process == 'Middle' and (2 <= distance_ron_value <= 3):
        strategy = 'Balance2'
        summary = 'Close to Tingpai,\n keep the hand tiles value and pay attention to safety'
    elif game_process == 'Middle' and distance_ron_value < 3:
        strategy = 'Defense1'
        summary = 'The hand tiles is far from Tingpai,\n so safety is the priority'
    elif game_process == 'Final' and distance_ron_value == 2:
        strategy = 'Defense2'
        summary = 'The hand tiles is far from Tingpai,\n so safety is the priority'
    else:
        strategy = 'Defense3'
        summary = 'Data not enough to analyze,\n Please Defense'
    
    return strategy, summary

def process_hand_tiles(acc, hand_c, whole_a):
    html_content = ""
    for idx in range(1, len(acc)):
        discard_option = acc[idx][0]
        possible_tiles = acc[idx][1]
        count = 4 * len(possible_tiles) - sum(1 for item in whole_a if item in possible_tiles)
        count = max(count, 0)
        
        null_ron = correct_names(null_ron_list, int_corr_str)
        ron_false = any(n in null_ron for n in possible_tiles)
        
        if discard_option in hand_c:
            continue
            
        html_content += f"<p>打:<img src='image/{discard_option}.png'></p>"
        html_content += "<ul>"
        show_possible_tiles = ''.join(f"<img src='image/{i}.png'>" for i in possible_tiles)
        html_content += f"<li>侍牌: {show_possible_tiles}</li>"
        html_content += f"<li>總數: {count}</li>"
        if ron_false:
            html_content += "<li style='color: red'>※可能振聽</li>"
        html_content += "</ul>"
    
    return html_content

def capture_real():
    global running
    output_frame = tk.Toplevel()
    output_frame.iconbitmap('favicon.ico')
    output_frame.geometry("1200x1000")

    # Create main frame for HTML content
    main_frame = Frame(output_frame)
    main_frame.pack(side='left', expand=True, fill='both')

    html_label = HTMLLabel(main_frame, html='')
    html_label.pack(expand=True, fill='both')

    # Create sidebar frame once
    sidebar_frame = Frame(output_frame, width=300, bg='lightgrey')
    sidebar_frame.pack(side='right', fill='y')

    output_frame.bind('<q>', stop_running)

    while running:
        hand_a, hand_b, hand_c = hand_tile_read()
        if len(hand_b) != 14 and hand_a is not None:
            continue
        
        hand_tile_str = ''.join(correct_names(sorted(hand_b), int_corr_str))
        html_content = "<p>※按Q鍵關閉程式。</p>"
        html_content += f"<h2>手牌：{str_to_maj(hand_tile_str)}</h2>"
        
        _, whole_a = whole_screen()
        whole_a = correct_names(whole_a, int_corr_str)
        hand_c = correct_names([str(x) for x in hand_c], int_corr_str)
        hand_tile = ''.join(correct_names(hand_b, int_corr_str))
        
        result1 = call(hand_tile)
        result2 = calc_shanten_14(hand_tile)
        
        try:
            result1_distance = int(result1[0][0])
        except ValueError:
            result1_distance = 0

        try:
            result2_distance = int(result2[0][0])
        except ValueError:
            result2_distance = 0
        
        if result1_distance == result2_distance:
            acc = result2
            model_now = 'calc_shanten_14'
        elif result1_distance < result2_distance:
            acc = result1
            model_now = 'cs_mah'
        elif result1_distance > result2_distance:
            acc = result2
            model_now = 'calc_shanten_14'

        try:
            distance_ron_value = int(acc[0][0]) + 1
        except ValueError:
            distance_ron_value = 'Tingpai'

        html_content += f"<p>Current Model: {model_now}</p>"
        html_content += f"<p>Distance to call a RON: {distance_ron_value}</p>"

        global null_ron_list
        _, null_ron_list = hand_off_read()
        game_process = "Beginning" if len(null_ron_list) <= 6 else "Middle" if len(null_ron_list) <= 12 else "Final"
        
        # Determine strategy and summary
        strategy, summary = determine_strategy(game_process, distance_ron_value)

        # Update sidebar content
        sidebar_content = f"""== Risk Assessment Overview ==
Current game process: {game_process}
Distance to call a RON: {distance_ron_value}
Suggest Strategy: {strategy}

Summary: {summary}
"""
        # Clear existing sidebar content
        for widget in sidebar_frame.winfo_children():
            widget.destroy()
        
        placeholder_label = tk.Label(sidebar_frame, text=sidebar_content, bg='lightgrey')
        placeholder_label.pack(pady=10)

        # Process hand tiles for display
        html_content += process_hand_tiles(acc, hand_c, whole_a)
        html_label.set_html(html_content)

        output_frame.update()
        time.sleep(0.5)

    output_frame.destroy()

if __name__ == "__main__":
    capture_real()