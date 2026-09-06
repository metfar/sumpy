#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#pylint:disable=W0301
#  
#  Copyright 2018- William Martinez Bas <metfar@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
import subprocess;
from sumdata import *;
from sumplot import *;
from sumcore.audio_api import audio_engine, beep, play, set_audio_engine, sound, stop_audio, wait_audio;
__version__="0.1.0a6";

def show(plot,block=False,width=8,height=6,dpi=100): return show_plot(plot,block=block,width=width,height=height,dpi=dpi);
def print_plot(plot,block=False,width=8,height=6,dpi=100): return show(plot,block=block,width=width,height=height,dpi=dpi);
def system2(command,args=None,stdout=None,stderr=None,wait=True):
    argv=[str(command)];
    if args is not None:
        if isinstance(args,(list,tuple)): argv.extend(str(item) for item in args);
        else: argv.append(str(args));
    out=subprocess.DEVNULL if stdout is False else None; err=subprocess.DEVNULL if stderr is False else None;
    if wait: return subprocess.run(argv,stdout=out,stderr=err,check=False).returncode;
    subprocess.Popen(argv,stdout=out,stderr=err,start_new_session=True); return 0;

from .screen import *;

# SUM convenience aliases; Python native True/False/None keep their semantics.
TRUE=True; true=True; FALSE=False; false=False; NULL=None; Null=None; null=None; NIL=None; Nil=None; nil=None; none=None;
