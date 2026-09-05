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
# sumPY r20.2: common aliases, dynamic text grid, cursor and graphics plane.
from sumpy import *;

print("aliases:", TRUE, true, FALSE, false, NULL, NIL, none);
print("text grid:", cols(), "x", rows());
print("cursor hidden:", cursor(False));
print("cursor normal:", cursor(True));
print("cursor block:", cursor("block"));
cursor(True);

configure_graphics(lambda: (640, 480, 16));
print("graphics:", gwidth(), "x", gheight(), "colors=", gcolors());
print("GPRINT command:", gprint(20, 30, "sumPY graphics text"));
print("GPRINTF command:", gprintf(20, 60, "size=%dx%d", gwidth(), gheight()));

paper(0);
border(1);
print("border width:", border_width(24));
