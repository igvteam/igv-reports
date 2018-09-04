#!/usr/bin/env python
# encoding: utf-8

import json

def get_data(filename):
    with open(filename,"r") as f:
        return(bytes(f.read(),"utf-8"))
