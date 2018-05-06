# Html_parser_for_MING_QING
## Free database
[明實錄、朝鮮王朝實錄、清實錄資料庫](http://hanchi.ihp.sinica.edu.tw/mql/login.html)
## Steps to use this tool
### 1.install python and third-party libs(bs4, xlwt)
if you are not familiar with python, recommend download [Anaconda](https://www.anaconda.com/download/) and install Python 3.6 version. The third-party libs will be included.
### 2.Save the website page as *html* file.
Right click the website and choose **Save as...**
Save to one emopty folder and **DO NOT** change the name.
Copy the python files –Html_parser.py and Find_all_match.py  to this folder
### 3.Run python file
> After installed Anaconda, you can launch Spyder, and use it to open python files.

There are two .py files, First run Find_all_match.py, it will print all found words that we will use later.The list printed is the different types of same word.
for example:

`['顏衛', '朵', '朵顏衛', '朶顏衛', '朵顏', '衛', '朶顏衞', '衞', '朵顏衞']`

we need to search '朵顏衛', '朶顏衛','朶顏衞' or '朵顏衞' .
So we need to open  *Html_parser.py*, find the **matches** varible in *line 12* and type the words in it.

`matches = [['朵顏衞', '朶顏衞','朵顏衛','朶顏衛']]`

Run this .py file.
All done, enjoy! 
## Notice
When there is more than one list of words. for example, search ‘陝西’run Find_all_match.py and got :

`['番', '僧', '番僧', '陜', '西', '陜西', '陝西']`

The matches varible in Html_parser.py will looks like this: 

`matches = [['陜西', '陝西'],['番僧']]`
