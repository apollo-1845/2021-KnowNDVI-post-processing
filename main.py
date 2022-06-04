#!/usr/bin/env python3
from stages.stage1 import run as stage1
from stages.stage2 import run as stage2

data_points = stage1()
stage2(data_points)
