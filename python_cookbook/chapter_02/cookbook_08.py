

# 2.8 Writing a regular expression for multiline patterns
import re

comment = re.compile(r'/\*(.*?)\*/')
text1 = '/* this is a comment */'
text2 = '''
        /* this is
        a multiline
        comment*/
'''
print(comment.findall(text1))
print(comment.findall(text2))

comment = re.compile(r'/\*((?:.|\n)*?)\*/')
print(comment.findall(text1))
print(comment.findall(text2))

comment = re.compile(r'/\*(.*?)\*/', re.DOTALL)  # re.MULTILINE ignores dots
print(comment.findall(text1))
print(comment.findall(text2))
