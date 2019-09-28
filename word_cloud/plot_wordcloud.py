# -*- coding:utf-8 -*-

import os
import PIL
import jieba
import argparse
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud, STOPWORDS


def text_segment(text):
    word_generator = jieba.cut(text, cut_all=False)
    word_list = [word for word in word_generator]
    seg_word_list = ' '.join(word_list)

    return seg_word_list


def word_frequency_count(text, output_dir):
    word_generator = jieba.cut(text, cut_all=False)
    word_list = [word for word in word_generator]
    word_count_dict = Counter(word_list)

    with open(output_dir, 'w') as fw:
        for word, count in word_count_dict.items():
            fw.write("%s,%d\n" % (word, count))


def plot_cloud(seg_word_list, mask_dir, font_dir, output_dir):
    mask = np.array(PIL.Image.open(mask_dir))
    stopwords = set(STOPWORDS)

    wc = WordCloud(background_color="white",
                   max_words=1000,
                   mask=mask,
                   stopwords=stopwords,
                   font_path=font_dir)

    wc.generate(seg_word_list)
    wc.to_file(output_dir)

    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()


parser = argparse.ArgumentParser(description='Plot a wordcloud and save to PNG image')
parser.add_argument("--text_dir", help="Pass a text directory")
parser.add_argument("--mask_dir", help="Pass a mask directory")
parser.add_argument("--image_dir", help="Pass a directory to save the output wordcloud image")
parser.add_argument("--font_dir", help="Pass a font directory to make this language compatible")
parser.add_argument("--userdict_dir", help="Pass a user-defined dictionary directory if needed")
parser.add_argument("--frequency_dir", help="Pass a directory to save the text file counting word frequency")
args = parser.parse_args()

if __name__ == "__main__":
    if args.userdict_dir:
        jieba.load_userdict(args.userdict_dir)
    else:
        try:
            jieba.load_userdict(os.path.join(os.path.dirname(__file__), 'userdict.txt'))
        except:
            pass

    if args.text_dir:
        text_dir = args.text_dir
    else:
        text_dir = os.path.join(os.path.dirname(__file__), 'text.txt')

    if args.mask_dir:
        mask_dir = args.mask_dir
    else:
        mask_dir = os.path.join(os.path.dirname(__file__), 'mask.png')

    if args.image_dir:
        image_dir = args.image_dir
    else:
        image_dir = os.path.join(os.path.dirname(__file__), 'wordcloud.png')

    if args.font_dir:
        font_dir = args.font_dir
    else:
        font_dir = os.path.join(os.path.dirname(__file__), 'msyh.ttf')

    if args.frequency_dir:
        frequency_dir = args.frequency_dir
    else:
        frequency_dir = os.path.join(os.path.dirname(__file__), 'frequency.txt')

    if os.path.exists(text_dir):
        with open(text_dir) as f:
            text = f.read()

        seg_word_list = text_segment(text)

        word_frequency_count(text, frequency_dir)

        plot_cloud(seg_word_list, mask_dir, font_dir, image_dir)

    else:
        raise Exception("Text has not been Passed")
