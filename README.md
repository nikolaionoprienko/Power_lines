Здравствуйте!
Это директория с программой по численному моделированию электростатического поля.

Если вы хотите установить программу на свой компьютер, достаточно скачать папку "Программа для ПК". 
Далее нужно запустить файл "electric field.exe". Важно чтобы оба файла electric field.exe и cmunrm были в одной папке. 

Если хотите посмотреть код, то вот предназначение файлов:

program.py -- основной код для моделирования электрического поля и вывод его как графика с помощью библиотеки matplotlib. 
Ввод данных здесь производится через консоль.  

func.py -- содержит две функции, которые собственно и моделируют поле, если вы запустите program.py.

pygame_interface.py -- код для моделирования поля с пользовательским интерфейсом, где ввод данных осуществляется с помощью мышки.

func_for_pg.py -- переписанные для библиотеки pygame функции с моделированием электрического поля.