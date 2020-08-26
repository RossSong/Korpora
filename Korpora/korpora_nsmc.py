import os
from typing import List

from .korpora import KorporaData, KorporaSubdata
from .utils import check_path, load_text


class NSMCSubdata(KorporaSubdata):
    labels: List[str]

    def __init__(self, texts, labels):
        if len(texts) != len(labels):
            raise ValueError('`texts` and `labels` must be same length')
        super().__init__(texts)
        self.labels = labels


class NSMCData(KorporaData):
    def __init__(self, root_dir):
        train_path = os.path.join(root_dir, 'ratings_train.txt')
        test_path = os.path.join(root_dir, 'ratings_test.txt')
        check_path(train_path, 'NSMCData')
        check_path(test_path, 'NSMCData')

        train_texts, train_labels = self.cleaning(load_text(train_path, num_heads=1))
        test_texts, test_labels = self.cleaning(load_text(test_path, num_heads=1))
        self.train = NSMCSubdata(train_texts, train_labels)
        self.test = NSMCSubdata(test_texts, test_labels)

    def cleaning(self, raw_lines: List[str]):
        separated_lines = [line.split('\t') for line in raw_lines]
        for i_sent, separated_line in enumerate(separated_lines):
            if len(separated_line) != 3:
                raise ValueError(f'Found some errors in line {i_sent}: {separated_line}')
        _, texts, labels = zip(*separated_lines)
        labels = [int(label) for label in labels]
        return texts, labels

    def get_all_texts(self):
        return self.train.texts + self.test.texts

    def get_all_labels(self):
        return self.train.labels + self.test.labels