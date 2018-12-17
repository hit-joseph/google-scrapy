#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author   : Joyous_Yim
# @time     : 2018/12/11 14:25
# @File     : quotes_spider.py
# @Software : PyCharm
import scrapy
from urllib import parse
import execjs


class Py4Js():
    def __init__(self):
        self.ctx = execjs.compile("""
        function TL(a) {
        var k = "";
        var b = 406644;
        var b1 = 3293161072;

        var jd = ".";
        var $b = "+-a^+6";
        var Zb = "+-3^+b+-f";

        for (var e = [], f = 0, g = 0; g < a.length; g++) {
            var m = a.charCodeAt(g);
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
            e[f++] = m >> 18 | 240,
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
            e[f++] = m >> 6 & 63 | 128),
            e[f++] = m & 63 | 128)
        }
        a = b;
        for (f = 0; f < e.length; f++) a += e[f],
        a = RL(a, $b);
        a = RL(a, Zb);
        a ^= b1 || 0;
        0 > a && (a = (a & 2147483647) + 2147483648);
        a %= 1E6;
        return a.toString() + jd + (a ^ b)
    };

    function RL(a, b) {
        var t = "a";
        var Yb = "+";
        for (var c = 0; c < b.length - 2; c += 3) {
            var d = b.charAt(c + 2),
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
        }
        return a
    }
    """)

    def getTk(self, text):
        return self.ctx.call("TL", text)


url = "https://translate.google.cn/translate_a/single?client=webapp&sl=zh-CN&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&source=bh&otf=1&ssel=3&tsel=0&kc=1&"


def get_tk(content):
    js = Py4Js()
    tk = js.getTk(content)
    return tk


def get_url(word, url=url):
    dict_ = dict(tk=get_tk(word),
                 q=word)
    dict_url = parse.urlencode(dict_)
    return url + dict_url


words = []
with open("phrase.txt", "r", encoding="utf-8")as file_in:
    for line in file_in:
        line = line.strip()
        words.append(line)


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        for word in words:
            print(word)
            url = get_url(word)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response)
        # page = parse.urldecode(response.url.split("=")[-1])
        filename = 'quotes.html'
        with open(filename, 'ab', 0) as f:
            f.write(response.body + b"\n")
        self.log('Saved file %s' % filename)
