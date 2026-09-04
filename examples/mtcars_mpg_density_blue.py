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
from sumpy import after_stat, aes, dataset, geom_histogram, ggsave, ggplot, show, system2;

datacamp_light_blue = "#51A8C9";
mtcars = dataset("mtcars");
p = ggplot(mtcars, aes("mpg", after_stat("density"))) + geom_histogram(binwidth=1, fill=datacamp_light_blue);
show(p, block=False);
ggsave("mtcars_mpg_density_blue_sumpy.png", plot=p, width=8, height=6, dpi=150);
system2("xdg-open", "mtcars_mpg_density_blue_sumpy.png", stdout=False, stderr=False, wait=False);
