# Automation of work with Aerolociya.PRO files
 Программа для оптимизации работы с пользовательскими файлами программы Аэролоция.PRO
## Описание проекта.
 После начала специальной операции и отключения иностранных сервисов по расчету планов полета моя компания была вынуждена искать замену на внутреннем рынка. 
 
 Такой заменой стала программа Аэролоция.PRO от компании Аэрософт.
 Данной программе для корректной работы необходимы файлы с разработанными маршрутами (постоянно изменяются и дополняются) и аэродинамическими моделями самолетов (периодически дополняются и актуализируются). Над созданием и поддержанием данных файлов трудится несколько отделов. Каждый сотрудник выгружает результат своей работы на сетевой диск компании.
 
 Проблема программы Аэролоция.PRO заключается в том, что она умеет работать только с папками и файлами, расположенным на жестком диске. Поэтому сотрудникам приходилось при внесении изменений вручную проверять список измененных файлов или копировать с заменой все файлы с сетевого диска в нужные папки на жестком диске своего ПК. Это вызывало постоянные ошибки: удаление "нужных" файлов и папок, копирование в неправильную папку, а также занимало много времени.
 
 Данная программа была написана мной для оптимизации работы с файлами и исключения ошибок пользователей.
 
 Для удобства пользователей (не умеют работать с командной строкой) графический интерфейс программы был написан при помощи PySimpleGUI, а затем помещен в EXE файл с помощью PyInstaller.
 ## Основные функции программы.
 1. Завершение процесса программы Аэролоция.PRO (работа с файлами возможна только при закрытой программе).
 2. Запуск программы Аэролоция.PRO.
 3. Удобное указание пути к папкам с файлами на жестком диске ПК.
 4. Все пути к папкам программа храним в генерируемом файле конфигурации auto_aerolociya_settings.ini, который автоматически пересохраняется при выходе из программы (на случай изменения путей). При запуске программа автоматически считывает данные из файла auto_aerolociya_settings.ini, если он есть.
 5. Программа копирует только недостающие и/или модифицированные файлы с сетевого диска.
 6. Очистка папок на жестком диске от всех файлов (пользователи хранят в данных папках персональные, модифицированные файлы, которые не нужно удалять при копировании новых файлов).
 7. Быстрое открытие папков в explorer с определенными файлами, которые могут потребоваться пользователю во время работы с программой.
