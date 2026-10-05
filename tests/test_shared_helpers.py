#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sumpy import repeat,mid,instr,trim,ilike,numformat,boolformat;

def test_shared_helpers():
    assert repeat("x",5)=="xxxxx";
    assert mid("abc",0,1)=="a";
    assert instr("abc","b")==1;
    assert trim("..x..",".")=="x";
    assert ilike("Hello","he%");
    assert numformat(5,"$ 0000.00")=="$ 0005.00";
    assert boolformat(None,"FALSE|TRUE|UNKNOWN")=="UNKNOWN";
