# -*- coding: utf-8 -*-
#效果：可以对一个Excel表格数据进行关键词提取，关键句子提取（包含关键词的句子），会生成两列新的数据
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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

def main():
    num = 0
    result_file = open('result.csv', 'wb')
    with open(task["sourceFile"], 'r') as f:
        for row in csv.DictReader(f):
            if num == 0:
                keys = row.keys() + ["关键词", "关键词句子"]
                # print keys
                writer = csv.DictWriter(result_file, fieldnames=keys)
                writer.writeheader()
            num += 1
            k_content = row[task["columnName"]].decode("utf-8")
            flag = 0
            for keyword in task["keywords"].split("#"):
                index = k_content.find(keyword.decode("utf-8"))
                word = ""
                # import ipdb; ipdb.set_trace()
                if index != -1:
                    end = -1
                    start = -1
                    flagnum = 0


                    for i in range(index, -1, -1):
                        ch = k_content[i]
                        if delimiters.has_key(ch.encode("utf-8")):
                            print ch
                            flagnum += 1
                            if flagnum == 3:
                                start = i
                                break
                    flagnum = 0
                    for i, ch in enumerate(k_content[index:]):
                        if delimiters.has_key(ch.encode("utf-8")):
                            flagnum += 1
                            if flagnum == 3:
                                print ch
                                end = i
                                break
                    if end == -1:
                        end = len(k_content) - index
                        # import ipdb; ipdb.set_trace()
                    word = k_content[start+1:index+end]

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
