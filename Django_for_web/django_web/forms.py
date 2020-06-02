#!/usr/bin/evn python
# _*_ coding:utf-8 _*_
from django import forms


class BookForm(forms.Form):
    TYPE =[
        ['所有', '所有'],
        ['小说', '小说'],
        ['外国文学', '外国文学'],
        ['编程', '编程'],
        ['互联网', '互联网'],
        ['中国文学', '中国文学'],
        ['随笔', '随笔'],
        ['日本文学', '日本文学'],
        ['散文', '散文'],
        ['村上春树', '村上春树'],
        ['诗歌', '诗歌'],
        ['童话', '童话'],
        ['名著', '名著'],
        ['儿童文学', '儿童文学'],
        ['古典文学', '古典文学'],
        ['余华', '余华'],
        ['鲁迅', '鲁迅'],
        ['诗词', '诗词'],
        ['张爱玲', '张爱玲'],
        ['钱钟书', '钱钟书'],
        ['茨威格', '茨威格'],
    ]
    BookName = forms.CharField(label='名称', max_length=30)
    # BookDec = forms.ChoiceField(lable='类型',choices=TYPE)
    BookDec  = forms.ChoiceField(label='类型', choices=TYPE)