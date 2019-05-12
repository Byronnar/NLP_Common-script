# -*- coding: utf-8 -*-
#效果：可以对一个Excel表格数据进行关键词提取，关键句子提取（包含关键词的句子），会生成两列新的数据
import sys
import csv
import importlib
importlib.reload(sys) #导入各模块

task = {
    "keywords": " #",                       # 填写关键词名称
    "sourceFile": u".csv",                  # 填写表格名称
    "columnName": "k_content"               #从哪一列截取
}

delimiters = {                              #分隔符号
    "~": 0,
    ".": 0,
    ",": 0,
    "，": 0,
    "!": 0,
    "?": 0,
    "。": 0,
    "！": 0,
    "？": 0,
    "；": 0,
    "|": 0,
}
#以上述符号进行切割。

def main():
    num = 0
    result_file = open('result.csv', 'w', encoding="utf-8") #py3必须进行编码，否则是str，无法成为对象
    with open(task["sourceFile"], encoding="utf-8") as f:
        for row in csv.DictReader(f): #DictReader 以字典形式读取，DictReader会将第一行的内容（类标题）作为key值，第二行开始才是数据内容。
            if num == 0:
                keys = list(row.keys()) + ["关键词", "关键词句子"]
                # print keys
                writer = csv.DictWriter(result_file, fieldnames=keys)
                writer.writeheader()
            num += 1
            k_content = row[task["columnName"]]
            flag = 0

            for keyword in task["keywords"].split("#"): #按符号切割
                index = k_content.find(keyword)
                word = ""
                # import ipdb; ipdb.set_trace()
                if index != -1: #-1代表出错
                    end = -1
                    start = -1
                    flagnum = 0


                    for i in range(index, -1, -1):
                        ch = k_content[i]
                        if ch.encode("utf-8") in delimiters:
                            print(ch)
                            flagnum += 1
                            if flagnum == 3:
                                start = i
                                break
                    flagnum = 0
                    for i, ch in enumerate(k_content[index:]):
                        if ch.encode("utf-8") in delimiters:
                            flagnum += 1
                            if flagnum == 3:
                                print(ch)
                                end = i
                                break
                    if end == -1:
                        end = len(k_content) - index
                        # import ipdb; ipdb.set_trace()
                    word = k_content[start+1:index+end]  #提取包含关键字的某句话。

                    # import ipdb; ipdb.set_trace()
                    row["关键词"] = keyword
                    row["关键词句子"] = word
                    flag = 1
                    writer.writerow(row)
            if flag == 0:
                row["关键词"] = ""
                row["关键词句子"] = ""
                writer.writerow(row)
                
    result_file.close()

if __name__ == "__main__":
    main()
