# import pyautogui
# print(pyautogui.size())

import json
import os
import time
import win32gui
import win32con
import keyboard


# 存储句柄
def save_handle(name, handle):
    handles = load_handles()
    handles[name] = handle
    with open('handles.json', 'w') as f:
        json.dump(handles, f)

# 加载句柄
def load_handle(name):
    handles = load_handles()
    return handles.get(name)

# 打开句柄文件
def load_handles():
    if os.path.exists('handles.json'):
        with open('handles.json', 'r') as f:
            return json.load(f)
    else:
        return {}

# 打开指定软件
def open_sof(name, handle=None, manual=0):
    if manual:
        # 手动模式启用，直接使用传入的句柄
        if not handle:
            print("手动模式下未提供句柄！")
            return None
        if not win32gui.IsWindow(handle):
            print(f"提供的句柄 {handle} 无效！")
            return None
        print(f"手动模式启用，使用指定句柄 {handle}。")
        save_handle(name, handle)  # 保存句柄到文件
    else:
        # 自动模式：从文件或窗口名称中查找句柄
        handle = load_handle(name)  # 尝试从文件读取句柄
        if not handle:
            print(f'文件中未找到句柄，尝试通过窗口名称 {name} 查找...')
            handle = win32gui.FindWindow(0, name)
            if handle == 0:
                print(f'未找到窗口 {name}')
                return None
            save_handle(name, handle)  # 保存句柄到文件
        else:
            print(f'文件中找到句柄 {name}：{handle}')

    win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)  # 发送消息以确保窗口恢复显示
    time.sleep(0.2) # 延迟1秒，等待窗口恢复

    win32gui.ShowWindow(handle, True)          # 使用win32gui库使窗口可见
    win32gui.SetForegroundWindow(handle)       # 使用win32gui库将窗口置于前台(焦点)
    win32gui.SendMessage(handle, win32con.SC_MAXIMIZE, 0) # 最大化窗口
    time.sleep(0.2)                              # 使用time库延迟1秒
    
    pos = win32gui.GetWindowRect(handle) # 窗口位置
    print(f'窗口位置 {pos}') # 打印窗口位置

def auto_key(hotkeys):
    # 去除空格并移除重复的快捷键
    seen_keys = set()
    filtered_hotkeys = []
    for hotkey in hotkeys:
        # 去掉快捷键中多余的空格
        clean_key = hotkey['key'].replace(" ", "")
        
        if clean_key in seen_keys:
            print(f"发现重复快捷键 {clean_key}，保留第一个绑定，移除后续重复绑定。")
            continue  # 跳过重复的快捷键
        
        seen_keys.add(clean_key)
        filtered_hotkeys.append({
            "key": clean_key,
            "func": hotkey['func'],
            "args": hotkey.get('args', [])
        })
    # 绑定快捷键
    for hotkey in filtered_hotkeys:
        keyboard.add_hotkey(hotkey['key'], lambda *args, f=hotkey['func'], a=hotkey['args']: f(*a))
    
    # for hotkey in hotkeys:
    #     keyboard.add_hotkey(hotkey['key'], lambda *args, f=hotkey['func'], a=hotkey.get('args', []): f(*a))

    # keyboard.add_hotkey('alt+r', lambda: open_sof('ToDesk'))
    
    try:
        # 保持脚本运行，直到按下退出快捷键
        keyboard.wait('shift+ctrl+e')  # 按下 Esc 退出监听
    finally:
        # 无论是否按下 shift+ctrl+e 都移除所有快捷键监听
        keyboard.unhook_all()
        # 清空句柄文件
        if os.path.exists('handles.json'):
            os.remove('handles.json')
        print('退出监听')

if __name__ == '__main__':
    # 定义快捷键、对应的函数和参数
    hotkey_actions = [
        {'key': 'alt+r', 'func': open_sof, 'args': ['ToDesk']},
        {'key': 'alt+t', 'func': open_sof, 'args': ['WeChat',2296752,1]},
        {'key': 'alt+y', 'func': open_sof, 'args': ['哔哩哔哩',137622,1]}
    ]
    # auto_key(hotkey_actions)
    open_sof('ToDesk')