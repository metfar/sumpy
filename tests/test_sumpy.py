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
import sumpy;
def test_exports_common_layers(): assert hasattr(sumpy,"dataset") and hasattr(sumpy,"PlotSpec");

def test_cli_version(capsys):
    from sumpy.cli import main;
    import pytest;
    with pytest.raises(SystemExit) as exc: main(["--version"]);
    assert exc.value.code==0; assert "sumPY 0.1.0a5" in capsys.readouterr().out;


def test_histogram_png(tmp_path,monkeypatch):
    monkeypatch.setenv("MPLBACKEND","Agg");
    p=sumpy.ggplot(sumpy.dataset("mtcars"),sumpy.aes("mpg",sumpy.after_stat("density")))+sumpy.geom_histogram(binwidth=1,fill="#51A8C9"); target=tmp_path/"sumpy.png"; sumpy.ggsave(target,plot=p,width=4,height=3,dpi=80); assert target.read_bytes()[:8]==bytes.fromhex("89504e470d0a1a0a");
