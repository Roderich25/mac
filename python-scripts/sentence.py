from collections import abc
import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return f'Sentence({reprlib.repr(self.text)})'

    def __iter__(self):
        return SentenceIterador(self.words)


class SentenceIterador:

    def __init__(self, words):
        self.words = words
        self.index = 0

    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word


s = Sentence("Alpha Bravo Charlie Delta Echo Foxtrot")
print(s.words)
print(s)


for w in s:
    print(w)

# print(list(s))

print(issubclass(SentenceIterador, abc.Iterator))
print(isinstance(s, abc.Iterable))
#
