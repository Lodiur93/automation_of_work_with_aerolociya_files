#!/usr/bin/env python
# coding: utf-8

# In[2]:


# импорт необходимых библиотек
import PySimpleGUI as sg
import os
import shutil
import time
import subprocess
import configparser
import wmi

# функция для получения пути к файлу во временной папке (иконка)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# задаем переменные
my_text = 'Программа разработана для автоматизации рутинных задач, связанных с копированием файлов для ПО Аэролоция.PRO. Данная программа создана исключительно для использования на рабочих местах сотрудников АО "Авиакомпания Россия".'
proc_name = 'APRO.EXE'
# задаем стандартные пути
aerolociya_path = r"C:\\Aerosoft\APRO.EXE"
default_routes_path_from = r"\\stc.local\Otdel\Navigation_service\2_Библиотека документов\АЭРОЛОЦИЯ\Маршруты"
default_routes_path_to = r"C:\Aerosoft\ROUTES"
default_planes_path_from = r"\\stc.local\Otdel\Navigation_service\2_Библиотека документов\АЭРОЛОЦИЯ\Парк ВС"
default_planes_path_to = r"C:\Aerosoft\PLANES"
default_userplanes_path_from = r"\\stc.local\Otdel\Navigation_service\2_Библиотека документов\АЭРОЛОЦИЯ\Парк ВС"
default_userplanes_path_to = r"C:\Aerosoft\\USERPLANES"
user_manual_path = r"C:\Aerosoft\DOC"
ndb_path = r"\\stc.local\Otdel\Navigation_service\2_Библиотека документов\АЭРОЛОЦИЯ\ndb"
calculation_instructions_path = r"\\stc.local\Otdel\Navigation_service\ОПД\Методические указания и вспомогательные файлы"
forbidden_paths = ['C:\Aerosoft', 'C:\Aerosoft\\', 'C:/Aerosoft', 'C:/Aerosoft/', 'C:/Aerosoft//']
settings_path = r"C:\Aerosoft\auto_aerolociya_settings.ini"

# прочитаем файл конфигурации
config = configparser.ConfigParser()
if os.path.exists(settings_path):
    config.read(settings_path)
    # Читаем значения из конфиг. файла
    proc_name = config.get("name", "proc_name")
    aerolociya_path = config.get("path", "aerolociya_path")
    default_routes_path_from = config.get("path", "default_routes_path_from")
    default_routes_path_to = config.get("path", "default_routes_path_to")
    default_planes_path_from = config.get("path", "default_planes_path_from")
    default_planes_path_to = config.get("path", "default_planes_path_to")
    default_userplanes_path_from = config.get("path", "default_userplanes_path_from")
    default_userplanes_path_to = config.get("path", "default_userplanes_path_to")
    user_manual_path = config.get("path", "user_manual_path")
    ndb_path = config.get("path", "ndb_path")
    calculation_instructions_path = config.get("path", "calculation_instructions_path")

# устанавливаем тему оформления
sg.theme('Default')
# создаем слой для окна
layout = [[sg.Menu([['Основное', 'Закрыть программу'],
                    ['Помощь', ['О программе', 'Контакты разработчика']]])],
          [sg.Frame('Работа с программой', [
          [sg.Button('Закрыть программу Аэролоция PRO', enable_events=True, size=(36, 1), key='close_aerolociya', font='Helvetica 16'), sg.Button('Запустить программу Аэролоция PRO', size=(38, 1),enable_events=True, key='open_aerolociya', font='Helvetica 16')],
          [sg.Text('Перед работой с файлами необходимо закрыть программу (сохраните работу в программе перед её закрытием). ', size=(400, 1), font='Helvetica 10 bold')],    
          ])],
          [sg.Frame('Работа с файлами', [
          [sg.Text('Путь к папке с маршрутами (на диске С)', font='Helvetica 12')],
          [sg.Input(default_routes_path_to, key='input_routes', size=(62)), sg.FolderBrowse('Найти', size=(9, 1), change_submits=True, target='input_routes', font='Helvetica 12'), sg.Button('Скопировать компанейские маршруты', enable_events=True, key='copy_routes', size=(40, 1), font='Helvetica 12')],
          [sg.Text('Путь к папке с моделями ВС (на диске С)', font='Helvetica 12')],
          [sg.Input(default_userplanes_path_to, key='input_userplanes', size=(62)), sg.FolderBrowse('Найти', size=(9, 1), target='input_userplanes', font='Helvetica 12'), sg.Button('Скопировать модели ВС', enable_events=True, key='copy_userplanes', size=(40, 1), font='Helvetica 12')],
          [sg.Text('Путь к папке со стандартными моделями ВС (на диске С)', font='Helvetica 12')],
          [sg.Input(default_planes_path_to, key='input_planes', size=(62)), sg.FolderBrowse('Найти', size=(9, 1), target='input_planes', font='Helvetica 12'), sg.Button('Скопировать стандартные модели ВС', enable_events=True, key='copy_planes', size=(40, 1), font='Helvetica 12')],
          [sg.Button('Очистить папку ROUTES', enable_events=True, key='clean_routes', size=(28, 1), font='Helvetica 12'), sg.Button('Очистить папку USERPLANES', enable_events=True, key='clean_userplanes', size=(35, 1), font='Helvetica 12'), sg.Button('Очистить папку PLANES', enable_events=True, key='clean_planes', size=(32, 1), font='Helvetica 12')],
          [sg.Text('Корректный путь к папкам на локальном диске (Navigation_service) уже указан в программе. Если указан корректный путь к папке (на диске С), то его не нужно менять.', font='Helvetica 8')],
          ])],
          [sg.Frame('Доступ к основным документам и файлам', [
          [sg.Button('Методические указания и вспомогательные файлы', enable_events=True, size=(44, 1), key='calculation_instructions', font='Helvetica 12'), sg.Button('Обновление НБД', size=(19, 1),enable_events=True, key='ndb', font='Helvetica 12'), sg.Button('Руководство пользователя', size=(42, 1),enable_events=True, key='user_manual', font='Helvetica 12')]
          ])]]
             
# создаем окно программы
window = sg.Window('Автоматизация работы с файлами ПО Аэролоция PRO v. 1.0', layout, size=(920,460), finalize=True, icon=resource_path(r'C:\Users\Никита\Desktop\copy_script\airplane.ico'))

while True:
    event, values = window.read()
    print(event, values)
    # процесс закрытия программы
    if event == sg.WIN_CLOSED or event == 'Закрыть программу':
        # создадим файл конфигурации (если его нет)
        if not os.path.exists(settings_path):
            # создадим файл с конфигурациями
            config.add_section("name")
            config.set("name", "proc_name", proc_name)
            config.add_section("path")
            config.set("path", "aerolociya_path", aerolociya_path)
            config.set("path", "default_routes_path_from", default_routes_path_from)
            config.set("path", "default_routes_path_to", default_routes_path_to)
            config.set("path", "default_planes_path_from", default_planes_path_from)
            config.set("path", "default_planes_path_to", default_planes_path_to)
            config.set("path", "default_userplanes_path_from", default_userplanes_path_from)
            config.set("path", "default_userplanes_path_to", default_userplanes_path_to)
            config.set("path", "user_manual_path", user_manual_path)
            config.set("path", "ndb_path", ndb_path)
            config.set("path", "calculation_instructions_path", calculation_instructions_path)
            # откроем файл и сохраненим параметры
            with open(settings_path, "w") as configfile:
                config.write(configfile)
        else:
            # перезапишем файл конфигурации (если он есть)
            config.set("name", "proc_name", proc_name)
            config.set("path", "aerolociya_path", aerolociya_path)
            config.set("path", "default_routes_path_from", default_routes_path_from)
            config.set("path", "default_routes_path_to", default_routes_path_to)
            config.set("path", "default_planes_path_from", default_planes_path_from)
            config.set("path", "default_planes_path_to", default_planes_path_to)
            config.set("path", "default_userplanes_path_from", default_userplanes_path_from)
            config.set("path", "default_userplanes_path_to", default_userplanes_path_to)
            config.set("path", "user_manual_path", user_manual_path)
            config.set("path", "ndb_path", ndb_path)
            config.set("path", "calculation_instructions_path", calculation_instructions_path)
            # откроем файл и сохраненим параметры
            with open(settings_path, "w") as configfile:
                config.write(configfile)
            time.sleep(1)
            break        
        
    # завершение процесса Аэролоция.PRO
    elif event == 'close_aerolociya':
        flag = 0
        p = wmi.WMI()
        # перебор процессов
        for process in p.Win32_Process():
            # завершаем процесс, если название соответствует
            if process.name == proc_name:
                process.Terminate()
                sg.popup("Программа Аэролоция PRO закрыта. Можно копировать файлы.")
                flag = 1
        if flag == 0:
            sg.popup("Программа Аэролоция PRO не была запущена.")
        
    # запуск процесса Аэролоция.PRO
    elif event == 'open_aerolociya':
        flag = 0
        p = wmi.WMI()
        # перебор процессов (проверка что программа еще не запущена)
        for process in p.Win32_Process():
            if process.name == proc_name:
                flag = 1
        if flag == 1:
            sg.popup("Программа Аэролоция PRO уже работает.")       
        else:
            # запускаем файл
            subprocess.Popen(aerolociya_path)
            time.sleep(6)
            sg.popup("Программа Аэролоция PRO успешно запущена.")
    
    # вывод информации о программе   
    elif event == 'О программе':
        sg.popup_scrolled(my_text) 
    
    # вывод контактов разработчика
    elif event == 'Контакты разработчика':
        sg.popup('Контакты                                                 Назаров Никита Александрович                                эл. почта n.nazarov@rossiya-airlines.com                                         телефон 89267572600')
    
    # копирование компанейских маршрутов
    elif event == 'copy_routes':
        try:
            # проверка на запретный путь
            if (values['Найти'] in forbidden_paths) or (values['input_routes'] in forbidden_paths):
                sg.popup('Выбран некорректный путь. Использование данного пути приведет в удалению файлов программы Аэролоция PRO!!!              Нужно выбрать другой путь.')
            else:
                # сохранение нового пути
                default_routes_path_to = values['input_routes']
                # создание папки по указанному пути, если её нет
                if not os.path.isdir(default_routes_path_to):
                    sg.popup('Указанная папка с маршрутами на диске С не найдена. Папка будет создана.')
                    os.mkdir(default_routes_path_to)
                else:
                    new_files = []
                    duplicate_files =[]
                    # создадим списка новых файлов и списка дубликатов
                    for i in os.listdir(default_routes_path_from):
                        if i not in os.listdir(default_routes_path_to):
                            new_files.append(i)
                        else:
                            duplicate_files.append(i)
                    # добавим измененые файлы к списку новых файлов 
                    for i in duplicate_files:
                        # если время последней модификации файла в папке источника больше,то необходимо добавить в список новых файлов
                        if os.path.getmtime(default_routes_path_from + "\\" + i) > os.path.getmtime(default_routes_path_to + "\\" + i):
                            new_files.append(i)
                    count=0
                    # копирование новых файлов (из источника)
                    for file_name in new_files:
                        # создаем полные пути к файлам
                        source = default_routes_path_from + '\\' + file_name
                        destination = default_routes_path_to + '\\' + file_name
                        count+=1
                        # вывод прогресса копирования
                        sg.one_line_progress_meter('Прогресс копирования маршрутов', count, len(new_files), orientation = "h", bar_color = ('Dark blue', 'Grey'), keep_on_top=True, size = (35, 20), no_button=True)
                        shutil.copy(source, destination)
                sg.popup(f'Успешно скопировано {len(new_files)} файла(-ов) с компанейскими маршрутами.')
        except FileNotFoundError:
            sg.popup('Не найдена папка на сетевом диске (источник копирования) или некорректно указан путь к папке с маршрутами на диске С (папка назначения).')
                      
    # копирование моделей вс
    elif event == 'copy_userplanes':
        try:
            # проверка на запретный путь
            if (values['Найти0'] in forbidden_paths) or (values['input_userplanes'] in forbidden_paths):
                sg.popup('Выбран некорректный путь. Использование данного пути приведет в удалению файлов программы Аэролоция PRO!!!              Нужно выбрать другой путь.')
            else:
                # сохранение нового пути
                default_userplanes_path_to = values['input_userplanes']
                # создание папки по указанному пути, если её нет
                if not os.path.isdir(default_userplanes_path_to):
                    sg.popup('Указанная папка с моделями ВС на диске С не найдена. Папка будет создана.')
                    os.mkdir(default_userplanes_path_to)
                else:
                    new_files = []
                    duplicate_files =[]
                    # создадим списка новых файлов и списка дубликатов
                    for i in os.listdir(default_userplanes_path_from):
                        if i not in os.listdir(default_userplanes_path_to):
                            new_files.append(i)
                        else:
                            duplicate_files.append(i)
                    # добавим измененые файлы к списку новых файлов 
                    for i in duplicate_files:
                        # если время последней модификации файла в папке источника больше,то необходимо добавить в список новых файлов
                        if os.path.getmtime(default_userplanes_path_from + "\\" + i) > os.path.getmtime(default_userplanes_path_to + "\\" + i):
                            new_files.append(i)
                    count=0
                    # копирование новых файлов (из источника)
                    for file_name in new_files:
                        # создаем полные пути к файлам
                        source = default_userplanes_path_from + '\\' + file_name
                        destination = default_userplanes_path_to + '\\' + file_name
                        count+=1
                        # вывод прогресса копирования
                        sg.one_line_progress_meter('Прогресс копирования моделей ВС', count, len(new_files), orientation = "h", bar_color = ('Dark blue', 'Grey'), keep_on_top=True, size = (35, 20), no_button=True)
                        shutil.copy(source, destination)
                sg.popup(f'Успешно скопировано {len(new_files)} файла(-ов) с моделями ВС.') 
        except FileNotFoundError:
            sg.popup('Не найдена папка на сетевом диске (источник копирования) или некорректно указан путь к папке с моделями ВС на диске С (папка назначения).')
    
    # копирование стандартных моделей вс
    elif event == 'copy_planes':
        try:
            # проверка на запретный путь
            if (values['Найти1'] in forbidden_paths) or (values['input_planes'] in forbidden_paths):
                sg.popup('Выбран некорректный путь. Использование данного пути приведет в удалению файлов программы Аэролоция PRO!!!              Нужно выбрать другой путь.')
            else:
                # сохранение нового пути
                default_planes_path_to = values['input_planes']
                # создание папки по указанному пути, если её нет
                if not os.path.isdir(default_planes_path_to):
                    sg.popup('Указанная папка со стандартными моделями ВС на диске С не найдена. Папка будет создана.')
                    os.mkdir(default_planes_path_to)
                else:
                    new_files = []
                    duplicate_files =[]
                    # создадим списка новых файлов и списка дубликатов
                    for i in os.listdir(default_planes_path_from):
                        if i not in os.listdir(default_planes_path_to):
                            new_files.append(i)
                        else:
                            duplicate_files.append(i)
                    # добавим измененые файлы к списку новых файлов 
                    for i in duplicate_files:
                        # если время последней модификации файла в папке источника больше,то необходимо добавить в список новых файлов
                        if os.path.getmtime(default_planes_path_from + "\\" + i) > os.path.getmtime(default_planes_path_to + "\\" + i):
                            new_files.append(i)
                    count=0
                    # копирование новых файлов (из источника)
                    for file_name in new_files:
                        # создаем полные пути к файлам
                        source = default_planes_path_from + '\\' + file_name
                        destination = default_planes_path_to + '\\' + file_name
                        count+=1
                        # вывод прогресса копирования
                        sg.one_line_progress_meter('Прогресс копирования стандартных моделей ВС', count, len(new_files), orientation = "h", bar_color = ('Dark blue', 'Grey'), keep_on_top=True, size = (35, 20), no_button=True)
                        shutil.copy(source, destination)
                sg.popup(f'Успешно скопировано {len(new_files)} файла(-ов) со стандартными моделями ВС.')
        except FileNotFoundError:
            sg.popup('Не найдена папка на сетевом диске (источник копирования) или некорректно указан путь к папке со стандартными моделями ВС на диске С (папка назначения).')
    
    # открытие папки с методичкой
    elif event == 'calculation_instructions':
        if os.path.isdir(calculation_instructions_path):
            os.system(r"explorer.exe " + calculation_instructions_path)
        else:
            sg.popup('Не удается найти папку, проверьте путь или обратитесь к разработчику.')
            
    # открытие папки с НБД
    elif event == 'ndb':
        if os.path.isdir(ndb_path):
            os.system(r"explorer.exe " + ndb_path)
        else:
            sg.popup('Не удается найти папку, проверьте путь или обратитесь к разработчику.')
            
    # открытие папки с руководством пользователя
    elif event == 'user_manual':
        if os.path.isdir(user_manual_path):
            os.system(r"explorer.exe " + user_manual_path)
        else:
            sg.popup('Не удается найти папку, проверьте путь или обратитесь к разработчику.')
            
    # очистка папки ROUTES
    elif event == 'clean_routes':
        # если папки нет, то создать
        if not os.path.isdir(default_routes_path_to):
            sg.popup('Папка с маршрутами по указанному пути на диске С не найдена. Папка будет создана.')
            os.mkdir(default_routes_path_to)
        else:
            # если папка есть, но занята каким-то процессом, то вывести сообщение
            try:
                shutil.rmtree(default_routes_path_to, ignore_errors=True)
                os.mkdir(default_routes_path_to)
                sg.popup('Папка с маршрутами успешно очищена.')
            except:
                sg.popup('Видимо, папка с маршрутами сейчас открыта (занята процессом). Закройте папку (завершите процесс) и повторите попытку снова')
    
    # очистка папки USERPLANES
    elif event == 'clean_userplanes':
        # если папки нет, то создать
        if not os.path.isdir(default_userplanes_path_to):
            sg.popup('Папка с моделями ВС по указанному пути на диске С не найдена. Папка будет создана.')
            os.mkdir(default_userplanes_path_to)
        else:
            # если папка есть, но занята каким-то процессом, то вывести сообщение
            try:
                shutil.rmtree(default_userplanes_path_to, ignore_errors=True)
                os.mkdir(default_userplanes_path_to)
                sg.popup('Папка с моделями ВС успешно очищена.')
            except:
                sg.popup('Видимо, папка с моделями ВС сейчас открыта (занята процессом). Закройте папку (завершите процесс) и повторите попытку снова')
    
    # очистка папки PLANES
    elif event == 'clean_planes':
        # если папки нет, то создать
        if not os.path.isdir(default_planes_path_to):
            sg.popup('Папка со стандартными моделями ВС по указанному пути на диске С не найдена. Папка будет создана.')
            os.mkdir(default_planes_path_to)
        else:
            # если папка есть, но занята каким-то процессом, то вывести сообщение
            try:
                shutil.rmtree(default_planes_path_to, ignore_errors=True)
                os.mkdir(default_planes_path_to)
                sg.popup('Папка со стандартными моделями ВС успешно очищена.')
            except:
                sg.popup('Видимо, папка со стандартными моделями ВС сейчас открыта (занята процессом). Закройте папку (завершите процесс) и повторите попытку снова')
    
window.close()


# In[ ]:




