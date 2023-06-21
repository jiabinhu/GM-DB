打包异常问题：
问题-1：![image](https://github.com/jiabinhu/GM-DB/assets/51167328/bb7232e7-3d87-4b6c-bbab-176ba3930f3a)
描述-1：无法将“pyinstaller”项识别为 cmdlet、函数.....
解决-1：

# GM-DB
一个简单的JSON读取工具
使用方法：把GM-DB.ico、JSON1.json、JSONdata.xlsx、Name.txt、Tools.py放置在同一个文件夹下面
使用pycharm的打包命令：pyinstaller -i GM-DB.ico -F Tools.py -n GM-DB.exe
常用参数 含义F
-i 或 -icon 生成icon
-F 创建一个绑定的可执行文件
-w 使用窗口，无控制台
-C 使用控制台，无窗口
-D 创建一个包含可执行文件的单文件夹包(默认情况下)
-n 文件名
hello
