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
import json;

import pytest;

from sumpy.piano_performance import load_piano_performance, midi_note_name, piano_performance_paths, render_piano_performance, save_piano_performance;


def _events():
    return [
        {"time":0.0,"event":"on","midi":60},
        {"time":0.0,"event":"on","midi":64},
        {"time":0.18,"event":"off","midi":60},
        {"time":0.18,"event":"off","midi":64},
        {"time":0.40,"event":"on","midi":67},
        {"time":0.55,"event":"off","midi":67},
    ];


def test_note_names_and_paths(tmp_path):
    assert midi_note_name(60)=="C4";
    assert midi_note_name(61)=="C#4";
    json_path,text_path=piano_performance_paths(tmp_path/"take");
    assert json_path.name=="take.sumpiano.json";
    assert text_path.name=="take.sumpiano";


def test_save_load_round_trip_creates_machine_and_human_files(tmp_path):
    json_path,text_path=save_piano_performance(tmp_path/"take",_events(),duration=0.70,base_midi=48,octave_shift=1);
    assert json_path.exists() and text_path.exists();
    loaded=load_piano_performance(json_path);
    assert loaded["format"]=="sum-piano-performance";
    assert loaded["version"]==1;
    assert loaded["duration"]==pytest.approx(0.70);
    assert loaded["base_midi"]==48 and loaded["octave_shift"]==1;
    assert loaded["events"]==_events();
    raw=json.loads(json_path.read_text(encoding="utf-8"));
    assert raw["events"][0]=={"time":0.0,"midi":60,"event":"on"};


def test_human_render_preserves_chords_and_silences(tmp_path):
    json_path,text_path=save_piano_performance(tmp_path/"take.sumpiano.json",_events(),duration=0.70);
    human=text_path.read_text(encoding="utf-8");
    assert "[C4 E4]" in human;
    assert "REST" in human;
    assert "G4" in human;
    assert "0.180" in human and "0.220" in human;
    assert "ON    C4" in human;
    assert "OFF   E4" in human;
    assert render_piano_performance(load_piano_performance(json_path))==human;


def test_loader_rejects_wrong_format(tmp_path):
    target=tmp_path/"bad.sumpiano.json";
    target.write_text('{"format":"other","version":1,"events":[]}',encoding="utf-8");
    with pytest.raises(ValueError,match="not a SUM piano performance"): load_piano_performance(target);
