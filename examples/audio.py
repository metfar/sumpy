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
from sumpy import beep, play, sound, stop_audio, wait_audio;

beep(0.25, 0);
sound(440, 18.2);
play("T180O6cdefgabC");
wait_audio();
stop_audio();
