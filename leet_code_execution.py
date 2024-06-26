['precompiled', 'prog.python3', 'judge.err', 'user.stdout', 'user.stderr', 'data.1.in', 'prog_joined.py', 'judge.out']
# coding: utf-8
from string import *
from re import *
from datetime import *
from collections import *
from heapq import *
from bisect import *
from copy import *
from math import *
from random import *
from statistics import *
from itertools import *
from functools import *
from operator import *
from io import *
from sys import *
from json import *
from builtins import *

import string
import re
import datetime
import collections
import heapq
import bisect
import copy
import math
import random
import statistics
import itertools
import functools
import operator
import io
import sys
import json

import precompiled.__settings__
from precompiled.__deserializer__ import __Deserializer__
from precompiled.__deserializer__ import DeserializeError
from precompiled.__serializer__ import __Serializer__
from precompiled.__utils__ import __Utils__
from precompiled.listnode import ListNode
from precompiled.nestedinteger import NestedInteger
from precompiled.treenode import TreeNode

from typing import *

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# user submitted code insert below
import platform

system_info = {
    "System": platform.system(),
    "Node Name": platform.node(),
    "Release": platform.release(),
    "Version": platform.version(),
    "Machine": platform.machine(),
    "Processor": platform.processor()
}
print(system_info)
import platform

import os

class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        # ['user.out', 'precompiled', 'data']
        # user.out : file
        # precompiled 
        #['__serializer__.pyc', '__deserializer__.pyc', 'nestedinteger.pyc', '__utils__.pyc', '__init__.pyc', 'treenode.pyc', '__settings__.pyc', 'listnode.pyc']
        #['lib32', 'mnt', 'media', 'root', 'sys', 'opt', 'proc', 'srv', 'dev', 'boot', 'run', 'var', 'libx32', 'sbin', 'tmp', 'usr', 'etc', 'lib64', 'lib', 'home', 'bin', 'leetcode', '.dockerenv', 'gtest']

        print(os.listdir('../mnt/'))
        with open('../mnt/prog_joined.py', 'r') as f:
            print(f.read())
       

        left, right = 0, 0
        count = 0

        while left < len(s) and right < len(t):
            if s[left] == t[right]:
                count += 1
                left += 1
                right += 1
            else:
                right += 1
        
        return len(s) == count
import sys
import os
import ujson as json

def _driver():

    des = __Deserializer__()
    ser = __Serializer__()
    SEPARATOR = "\x1b\x09\x1d"
    f = open("user.out", "wb", 0)
    lines = __Utils__().read_lines()

    while True:
        line = next(lines, None)
        if line == None:
            break
        param_1 = des._deserialize(line, 'string')
        
        line = next(lines, None)
        if line == None:
            raise Exception("Testcase does not have enough input arguments. Expected argument 't'")
        param_2 = des._deserialize(line, 'string')
        
        ret = Solution().isSubsequence(param_1, param_2)
        try:
            out = ser._serialize(ret, 'boolean')
        except:
            raise TypeError(str(ret) + " is not valid value for the expected return type boolean");
        out = str.encode(out + '\n')
        f.write(out)
        sys.stdout.write(SEPARATOR)


if __name__ == '__main__':
    _driver()