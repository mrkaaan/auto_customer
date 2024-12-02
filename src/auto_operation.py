from WinGUI import WinGUI
import utils as ul
import os   
import time     
import datetime
import keyboard   
import pyautogui   
import pyperclip   
import pandas as pd
from utils import show_toast
from loguru import logger  

# 循环执行 直到出现标志或者手动终止 需要修改
def running_loop(window_name, cycle_number=-1):
    """
    执行自动化程序：检测窗口状态，按循环次数或按键终止。
    
    :param window_name: 应用窗口的名称
    :param cycle_number: 循环次数，-1 表示无限循环 直到手动终止
    """
    exit_flag = False

    def on_key_event(event):
        # 当按键被按下时触发事件，如果按下 'q' 键，则终止循环
        nonlocal exit_flag
        if event.name == 'q':
            logger.info(f"END | terminated by user, windoe name: {window_name}") # 被用户终止
            exit_flag = True

    keyboard.on_press(on_key_event)  # 设置按键监听

    app = WinGUI(window_name)  # 创建 WinGUI 实例，用于窗口操作
    logger.info(f'START | window name: {window_name}')  # 记录窗口名称
    
    cycle_count = 0 # 初始化循环计数器
    while not exit_flag:
        try:
            if is_loop_over(app, 'icon.png'): # 检测是否结束
                logger.info(f"Cycle {cycle_count} is finished")  # 记录当前循环结束
                if cycle_number > 0 and cycle_count >= cycle_number:  # 检查是否达到设定的循环次数
                    logger.info(f"finished {cycle_count} cycles!")  # 记录完成循环次数
                    return
                

                cycle_count += 1  # 循环计数加一
        except Exception as err:
            logger.info(err)  # 记录异常信息

        
        time.sleep(0.5)   # 每次循环暂停1秒

def running_loop_test(cycle_number=-1):
    """
    :param cycle_number: 循环次数，-1 表示无限循环 直到手动终止
    """
    # 假设这里打开文件

    exit_flag = False

    def set_exit_flag():
        nonlocal exit_flag
        print(f"END | terminated by user")
        exit_flag = True

    # 设置组合键监听
    keyboard.add_hotkey('shift+ctrl+e', set_exit_flag)

    cycle_count = 0  # 初始化循环计数器
    try:
        while not exit_flag:
            print(f"Cycle {cycle_count} is finished")
            if cycle_number > 0 and cycle_count >= cycle_number:  # 检查是否达到设定的循环次数
                logger.info(f"finished {cycle_count} cycles!")  # 记录完成循环次数
                return
                
            cycle_count += 1  # 循环计数加一

            # 省略一系列复杂操作
            # 操作末尾给当前数据打上处理完毕标记

            time.sleep(0.5)  # 每次循环暂停1秒

    except KeyboardInterrupt:
        print("检测到 Ctrl+C，正在退出...")
    except Exception as e:
        print(f"快捷键监听出错：{e}")
    finally:
        # 回写文件
        
        # 移除所有快捷键监听
        keyboard.unhook_all()
        print('退出监听')

# 判断循环是否结束 需要修改
def is_loop_over(app, icon):
    """
    检测指定图标是否出现在窗口中，以判断循环是否结束
    
    :param app: WinGUI 实例，提供窗口和图标检测功能
    :return: 如果测试结束则返回 True，否则返回 False
    """
    valid = app.check_icon(icon)  # 检测标志
    return valid

# 千牛 执行一次备注操作
def run_once_remarks_by_qianniu(window_name):
    app = WinGUI(window_name)  # 创建 WinGUI 实例，用于窗口操作
    # logger.info(f'START | window name: {window_name}')  # 记录窗口名称

    try:
        # app.get_app_screenshot()
        # 点击备注
        find_button_remarks = app.click_icon('Button_Remarks.png',0.5,1.0,0.4,1.0)
        if not find_button_remarks:
            logger.info(f"END | not find Button_Remarks.png, windoe name: {window_name}") # 停止记录
            return
        # 点击红色备注
        app.click_icon('Button_RedFlag.png',0.4,1.0,0.4,1.0)
        # 向下移动到输入框并点击
        app.rel_remove_and_click(0, 150)
        # time.sleep(0.1)
        # 获取输入框当前的内容
        keyboard.press_and_release('ctrl+a')  
        keyboard.press_and_release('ctrl+c')  # 模拟按下并释放
        current_text = pyperclip.paste()      # 获取剪贴板中的文本
        time.sleep(0.1)
        entry_text = ''
        # 判断输入框是否有内容
        print('------')
        print(current_text)
        if current_text.strip():  # 如果字符串不为空
            entry_text = f'{current_text}\n已登记补发' if '已登记' in current_text else '已登记补发'
        else:
            entry_text = '已登记补发'
        print(entry_text)
        # 判断有无按下附加信息按钮
        # app.check_icon('button_additional_information.png'):
        # time.sleep(0.1)
        # 输入
        keyboard.write(entry_text)
        # 点击确认
        app.click_icon('Button_Confirm_Remarks.png',0.8,1.0,0.8,1.0)
        # 点击取消
        # app.click_icon('Button_Cancel_Remarks.png',0.8,1.0,0.8,1.0)

        # logger.info(f"END | terminated by program, windoe name: {window_name}") # 停止记录
        run_once_unmark_by_qianniu(window_name)
    except Exception as err:
        logger.info(err)  # 记录异常信息

# 千牛 执行一次取消标记操作
def run_once_unmark_by_qianniu(window_name, mode=1):
    '''
        mode: 1 使用快捷键取消标记 2 使用鼠标点击取消标记
    '''
    app = WinGUI(window_name)  # 创建 WinGUI 实例，用于窗口操作
    # logger.info(f'START | window name: {window_name}')  # 记录窗口名称

    try:
        # app.get_app_screenshot()
        # 取消标记
        if mode == 1:
            keyboard.press_and_release('ctrl+i')
            # 按下三次 ctrl+w 取消标记
            keyboard.press_and_release('ctrl+w')
            keyboard.press_and_release('ctrl+w')
            keyboard.press_and_release('ctrl+w')
        elif mode == 2:
            local_x, local_y, is_find = app.locate_icon('button_selected_session_annotation.png',0,0.4,0,1.0)
            if is_find:
                app.move_and_click(local_x, local_y, 'right')
                time.sleep(0.1)
                app.click_icon('button_cancel_annotations.png',0,0.4,0.2,1.0)
            else:
                # 找 button_selected_session_annotation.png
                local_other_x, local_other_y, is_find_other = app.locate_icon('button_selected_session_annotation_other.png',0,0.4,0,1.0)
                if is_find_other:
                    app.move_and_click(local_other_x, local_other_y, 'right')
                    time.sleep(0.1)
                    app.click_icon('button_cancel_annotations.png',0,0.4,0.2,1.0)
                else:
                    logger.info(f"END | not find button_selected_session_annotation.png, windoe name: {window_name}") # 停止记录

        # logger.info(f"END | terminated by program, windoe name: {window_name}") # 停止记录
    except Exception as err:
        logger.info(err)  # 记录异常信息

# 测试
def run_test(window_name):
    app = WinGUI(window_name)  # 创建 WinGUI 实例，用于窗口操作
    try:
        print()
    except Exception as err:
        logger.info(err)  # 记录异常信息

# 通知补发单号
# mode1 使用输入框通知 mode2 使用补发窗口通知
def notification_reissue(window_name, table_name, notic_shop_name, notic_mode=2, show_logistics=False, logistics_mode=1, use_today=None, test_mode=0, is_write=True, table_path='', form_folder='./form'):
    '''
        :param window_name: 应用窗口的名称
        :param table_name: 表单名称
        :param notic_shop_name: 店铺名称
        :param notic_mode: 通知模式 1：输入框通知 2：补发窗口按钮通知
        :param show_logistics: 是否显示物流公司 输入框通知模式下生效
        :param logistics_mode: 物流模式 1自动识别物流公司 2手动输入物流公司
        :param use_today: 是否使用今天日期作为路径 默认今天 指定则传入如 2024-11-27 注需要存在文件及路径
        :param test_mode: 测试模式 0：不测试 若测试则输入测试数量
        :param is_write: 是否写入数据 默认写入
        :param table_path: 表单路径 暂时用不到 预留位置 当前逻辑比较畸形避免处可以用于出错后续优化
        :param form_folder: 表单文件夹路径
    '''
    # 打印参数信息 每条信息换行
    print(f"窗口名称：{window_name}\n表单名称：{table_name}\n店铺名称：{notic_shop_name}\n通知模式：{notic_mode}\n显示物流公司：{show_logistics}\n物流模式：{logistics_mode}\n是否使用今天日期作为路径：{use_today}\n测试模式：{test_mode}\n是否写入数据：{is_write}\n表单路径：{table_path}\n表单文件夹路径：{form_folder}")

    app = WinGUI(window_name)  # 创建 WinGUI 实例，用于窗口操作

    # 避免店铺名称冲突
    if notic_shop_name == '团洁':
        notic_shop_name = '团洁旗舰'

    # 设置店铺名称图片名称 包含选中与未选中状态
    # '潮洁居家日用旗舰店-天猫', '余猫旗舰店-天猫', '团洁3504猫宁-天猫', '团洁旗舰店-天猫', '潮洁873猫宁-天猫'
    if notic_shop_name == '团洁旗舰':
        shop_name_icon = 'tuanjie_table_icon_selected.png'
        shop_name_icon_not_selected = 'tuanjie_table_icon_not_selected.png'
    elif notic_shop_name == '潮洁居家':
        shop_name_icon = 'chaojie_table_icon_selected.png'
        shop_name_icon_not_selected = 'chaojie_table_icon_not_selected.png'
    elif notic_shop_name == '余猫旗舰':
        shop_name_icon = 'yumao_table_icon_selected.png'
        shop_name_icon_not_selected = 'yumao_table_icon_not_selected.png'
    elif notic_shop_name == '猫宁3504':
        notic_shop_name = '3504猫宁'
        shop_name_icon = 'maoning_table_icon_selected.png'
        shop_name_icon_not_selected = 'maoning_table_icon_not_selected.png'
    elif notic_shop_name == '猫宁873':
        notic_shop_name = '873猫宁'
        shop_name_icon = 'maoning_table_icon_selected.png'
        shop_name_icon_not_selected = 'maoning_table_icon_not_selected.png'
    elif notic_shop_name == '音美旗舰':
        shop_name_icon = 'yinmei_table_icon_selected.png'
        shop_name_icon_not_selected = 'yinmei_table_icon_not_selected.png'
    elif notic_shop_name == 'lelodi':
        shop_name_icon = 'lelodi_table_icon_selected.png'
        shop_name_icon_not_selected = 'lelodi_table_icon_not_selected.png'
    elif notic_shop_name == 'yemo':
        shop_name_icon = 'yemo_table_icon_selected.png'
        shop_name_icon_not_selected = 'yemo_table_icon_not_selected.png'
    else:
        print(f"未知店铺名称：{notic_shop_name}")
        return
    
    # 定义一个退出标志
    exit_flag = False
    
    # 定义按键监听事件
    def set_exit_flag():
        nonlocal exit_flag
        print(f"END | terminated by user")
        exit_flag = True
    
    keyboard.add_hotkey('shift+ctrl+q', set_exit_flag)


    try:
        # 组合表单路径
        # 如果使用今天日期 则进行组合
        if not use_today:
            form_folder += f"/{datetime.datetime.now().strftime('%Y-%m-%d')}"
        else:
            form_folder += f"/{use_today}"
        table_file = os.path.join(form_folder, table_name)


        # 根据不同文件格式读取表格
        file_format = table_name.split('.')
        if 'xls' in file_format[1]:
            # 表格不存在提示
            if os.path.exists(table_file):
                print(f"表单文件：{table_file} 不存在")
                show_toast('提醒', f'表单文件：{table_file} 不存在')
                return
            # 读取 Excel 文件
            df = pd.read_excel(table_file, sheet_name=None, dtype={'原始单号': str, '物流单号': str})
        elif 'csv' in file_format[1]:
            print('未处理 csv 文件')
            return
        else:
            print('未知格式')
            return
        
        # 获取所有sheet的名称
        sheet_names = df.keys()

        current_sheet_name = ''
        # 选定店铺名 循环判断notic_shop_name是否在sheet_names中
        for sheet_name in sheet_names:
            if notic_shop_name in sheet_name:
                print(f"选定表单：{sheet_name}")
                current_sheet_name = sheet_name
                break
        if not current_sheet_name:
            print(f"未找到 '{notic_shop_name}' 的表单，程序终止")
            return
        
        # 读取当前表单
        df_current_sheet = df[current_sheet_name]
        column_names = df_current_sheet.columns.tolist()  # 获取列名列表
        # print(column_names) # 打印列名列表

        # 检查是否存在"是否通知"列，如果不存在则添加
        if '是否通知' not in column_names:
            df_current_sheet['是否通知'] = 0
            # 将更改写回 Excel 文件
            with pd.ExcelWriter(table_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df_current_sheet.to_excel(writer, index=False, sheet_name=current_sheet_name)
            print(f"列 '是否通知' 已添加到表格指定sheet '{current_sheet_name}' 中")
        else:
            print(f"列 '是否通知' 已存在于表格指定sheet '{current_sheet_name}' 中")
        

        # 点击店铺名称 分为两种情况 已经被选中和未被选中的状态
        is_find_shop_icon = app.click_icon(shop_name_icon, 0, 0.9, 0, 0.3)
        if not is_find_shop_icon:
            is_find_shop_icon = app.click_icon(shop_name_icon_not_selected, 0, 0.9, 0, 0.3)
        if not is_find_shop_icon:
            print(f"未找到店铺名称：{notic_shop_name}")
            return
        time.sleep(0.2)

        if test_mode:
            # 限制 DataFrame 到指定行数 用于测试 排除 '是否通知' 列中值为 0 的行
            # df_subset = df_current_sheet.head(2)
            # df_subset = df_current_sheet.iloc[:2]
            # df_subset = df_current_sheet.iloc
            print(f"当前sheet: {current_sheet_name}，测试模式，只处理前 {test_mode} 行")
            df_subset = df_current_sheet.loc[df_current_sheet['是否通知'] != 1, :].iloc[:test_mode]
        else:
            print(f"当前sheet: {current_sheet_name}，处理所有行")
            df_subset = df_current_sheet
        print(df_subset)
        # 逐行处理DataFrame
        for index, row in df_subset.iterrows():
            if exit_flag:
                break  # 如果接收到退出信号，则终止循环
            
            # 检查是否已经通知
            if row['是否通知'] == 1:
                print('当前用户已通知')
                continue  # 如果已经通知，则跳过当前行

            # 获取原始单号和物流单号
            original_number = row['原始单号']
            logistics_number = row['物流单号']
            print(f"原始单号：{original_number} 物流单号：{logistics_number}")
            # 原始单号为空 提示并跳过
            if not original_number:
                print(f"原始单号为空 跳过")
                show_toast('提醒', f'原始单号为空 跳过')
                continue
            # 物流单号为空 提示并跳过
            if not logistics_number:
                print(f"物流单号为空 跳过")
                show_toast('提醒', f'物流单号为空 跳过')
                continue

            # original_number=123456789789

            # app.get_app_screenshot()
            # app.move_and_click(750, 500)
            # time.sleep(0.5)
            # 模拟按下 alt+W 快捷键打开目标软件
            # keyboard.press_and_release('alt+c')
            # 等待软件响应
            # 模拟按下 ctrl+F 打开搜索功能
            # keyboard.press_and_release('ctrl+i')
            # time.sleep(0.5)
            # keyboard.press_and_release('ctrl+f')
            # time.sleep(0.5)

            # 点击搜索框
            app.click_icon('button_search_cus.png',0,0.3,0,0.3)
            time.sleep(0.1)

            # 清除搜索框
            keyboard.press_and_release('ctrl+a')  
            keyboard.press_and_release('backspace')

            # 将 original_number 的内容输入到搜索框中
            # pyautogui.typewrite(original_number)
            # 将中文字符串复制到剪贴板
            pyperclip.copy(original_number)
            keyboard.press_and_release('ctrl+v') 
            # 等待搜索结果响应
            time.sleep(0.2)

            # 判断是否未找到
            _, __, not_find_cus = app.locate_icon('not_find_customer.png',0, 0.4, 0, 0.6)
            if not_find_cus:
                print(f"未搜索到结果，跳过 {original_number}")
                continue  # 未搜索到直接continue下一个
            else:
              print('搜索到指定用户，即将发送通知...')
            
            # 模拟按下回车键进入指定用户的聊天窗口
            keyboard.press_and_release('enter')
            time.sleep(0.3)

            
            # 通知模式 1：输入框通知 2：补发窗口通知
            if notic_mode == 1:
                # 按下 ctrl+J 定位到输入框中
                keyboard.press_and_release('ctrl+i')
                time.sleep(0.2)

                # 调用 app.locate_icon 传入图片名称，找到是否有某个图片存在
                # x, y, is_find = app.locate_icon('input_box_icon.png')
                # 判断 is_find 是否为 True
                # if not is_find:
                #     logger.err("无法定位到输入框，程序终止")
                #     break  # 无法定位到直接终止程序
                # 如果为 True，则相对向下移动 200 个像素后点击
                # app.remove_and_click(x, y + 200)

                # 清除输入框
                keyboard.press_and_release('ctrl+a')  
                keyboard.press_and_release('backspace')

                time.sleep(0.2)
                # 获取快递公司
                if show_logistics:
                    logistics = ul.get_express_company(logistics_number)
                else:
                    logistics = ''
                message = f"亲 {logistics} {logistics_number} 这是您的补发单号 请注意查收"

                # 将中文字符串复制到剪贴板
                pyperclip.copy(message)
                # 使用 pyautogui.typewrite 粘贴剪贴板内容
                keyboard.press_and_release('ctrl+v')  
                # pyautogui.typewrite(message, paste=True)
                time.sleep(0.2)

                # 模拟按下回车发送消息
                keyboard.press_and_release('enter')
            elif notic_mode == 2:
                # 聚焦到智能客服 避免误触
                keyboard.press_and_release('ctrl+o')
                # 点击最近三月订单和安装服务 避免误触
                recent_orders_text_x, recent_orders_text_y, is_find_recent_orders_text = app.locate_icon('recent_orders_text.png', 0.6, 1, 0.2, 1)
                app.click_icon('recent_orders_text.png', 0.6, 1, 0.2, 1)
                if not is_find_recent_orders_text:
                    app.click_icon('installation_services.png', 0.6, 1, 0.2, 1)
                # time.sleep(0.1)

                # 尝试点击两次搜索订单按钮
                is_find_search_button = False 
                for i in range(2):
                    search_button_x, search_button_y, is_find_search_button = app.locate_icon('search_order_button.png', 0.6, 1, 0.2, 1)
                    if not is_find_search_button:
                        # 未找到搜索订单按钮 尝试点击以选中的按钮
                        selected_search_button_x, selected_search_button_y, is_find_selected_search_button = app.locate_icon('selected_search_order_button.png', 0.6, 1, 0.2, 1)
                        if not is_find_selected_search_button:
                            print(f'未找到搜索订单按钮，尝试滑动后再次查找...')
                            pyautogui.scroll(-100)
                        else:
                            print(f'当前搜索按钮已被点击直接执行下一步...')
                            is_find_search_button = True
                            break
                    else:
                        app.move_and_click(search_button_x, search_button_y)
                        break
                if not is_find_search_button:
                    print(f'未找到搜索订单按钮，跳过{logistics_number}')
                    continue
                # time.sleep(0.1)

                # 尝试点击两次搜索框
                is_find_search_text = False
                for i in range(2):
                    search_text_x, search_text_y, is_find_search_text = app.locate_icon('search_order_text.png', 0.6, 1, 0.2, 1)
                    if is_find_search_text:
                        print(f'找到搜索框，点击搜索框...')
                        break
                    print(f'未找到搜索框，尝试滑动后再次查找...')
                    pyautogui.scroll(-150)

                if not is_find_search_text:
                    print(f'未找到搜索框，跳过{logistics_number}')
                    continue
                else:
                    app.move_and_click(search_text_x+100, search_text_y)
                time.sleep(0.3)

                # 保证输入框没有内容
                keyboard.press_and_release('ctrl+a') 
                keyboard.press_and_release('backspace') 
                # 输入订单号
                pyperclip.copy(original_number)
                keyboard.press_and_release('ctrl+v') 
                # time.sleep(0.1)
                # 模拟按下回车搜索
                keyboard.press_and_release('enter')
                # 使用 pyautogui 向下滚动鼠标滚轮
                pyautogui.scroll(-300)
                time.sleep(0.3)

                #  尝试点击两次补发按钮
                is_find_reissue_button = False
                for _ in range(2):
                    reissue_button_x, reissue_button_y, is_find_reissue_button = app.locate_icon('reissue_button.png', 0.6, 1, 0.2, 1)
                    if is_find_reissue_button:
                        print(f'找到补发按钮，点击补发按钮...')
                        break
                    print(f'未找补发按钮，尝试滑动后再次查找...')
                    pyautogui.scroll(-150)

                if not is_find_reissue_button:
                    print(f'未找到补发按钮，跳过{original_number}')
                    continue
                app.move_and_click(reissue_button_x, reissue_button_y, 'left')
                time.sleep(0.3)

                # 点击输入框
                add_logistics_number_x, add_logistics_number_y, is_find_add_logistics_number = app.locate_icon('add_logistics_number.png', 0.6, 1, 0.5, 1)
                if not is_find_add_logistics_number:
                    print(f'未找到添加物流单号提示文字，跳过{original_number}')
                    continue
                app.move_and_click(add_logistics_number_x, add_logistics_number_y)

                # 将中文字符串复制到剪贴板
                pyperclip.copy(logistics_number)
                keyboard.press_and_release('ctrl+v') 
                keyboard.press_and_release('tab')
                time.sleep(0.5)

                # 手动输入物流公司
                if logistics_mode == 2:
                    print(f'手动输入快递公司模式..')
                    logistics = ul.get_express_company(logistics_number)
                    # 如果不为空 末尾加快递二字
                    if logistics:
                        logistics = f"{logistics}快递"
                        pyperclip.copy(logistics)
                        keyboard.press_and_release('ctrl+v')
                        keyboard.press_and_release('enter')

                    else:
                        logistics_mode = 1  # 自动识别物流公司
                # 自动识别物流
                if logistics_mode == 1:
                    print(f'自动输入快递模式...')
                    # 按下回车
                    keyboard.press_and_release('enter')
                time.sleep(0.1)


                # 点击确认补发按钮
                confirm_button_x, confirm_button_y, is_find_confirm_button = app.locate_icon('confirm_button.png', 0.6, 1, 0.2, 1)
                if not is_find_confirm_button:
                    print(f'未找到确认补发按钮，跳过{original_number}')
                    continue
                else:
                    # 点击确认按钮
                    app.move_and_click(confirm_button_x, confirm_button_y)

                # change  判断是否弹出失败提示

            else:
                print(f"未知通知模式：{notic_mode}")
                return
                
            # 将当前行的"是否通知"标记为1
            print(f'已通知 {notic_shop_name} {original_number}')
            df_current_sheet.at[index, '是否通知'] = 1
                
            # 循环结束暂停
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("检测到 Ctrl+C，正在退出...")
    except Exception as e:
        print(f"通知程序异常：{e}")
        # 如果读取过程中出现异常，可能是文件被其他程序占用（例如已打开）
        if 'Permission error' in str(e) or '已被其他程序打开' in str(e):
            print("文件可能已被其他程序打开，请确保文件未被打开后再试。")
    finally:
        # 使用pyperclip库清空剪切板
        pyperclip.copy('')
        print('通知程序已退出')
        show_toast('提示', '程序已退出')
        # 将更改写回 Excel 文件
        with pd.ExcelWriter(table_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            # 只写回当前处理的sheet
            df_current_sheet.to_excel(writer, sheet_name=current_sheet_name, index=False)

        keyboard.unhook_all()  # 移除所有按键监听
    return df