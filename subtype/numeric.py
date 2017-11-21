#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def isfloat(value):
    try:
        float(value)
        return True
        
    except ValueError:
        return False
            
            
def isint(value):
    try:
        int(value)
        return True
        
    except ValueError:
        return False