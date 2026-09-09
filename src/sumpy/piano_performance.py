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
import os;
from pathlib import Path;
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union;

PIANO_PERFORMANCE_FORMAT="sum-piano-performance";
PIANO_PERFORMANCE_VERSION=1;
NOTE_NAMES=("C","C#","D","D#","E","F","F#","G","G#","A","A#","B");
PathLike=Union[str,os.PathLike];


def midi_note_name(midi:int)->str:
    midi=int(midi);
    return NOTE_NAMES[midi%12]+str(midi//12-1);


def _normalise_event(raw:Mapping[str,object],index:int)->Dict[str,object]:
    try: timestamp=float(raw.get("time",0.0));
    except (TypeError,ValueError) as exc: raise ValueError(f"event {index}: invalid time") from exc;
    if timestamp<0.0: raise ValueError(f"event {index}: time must be >= 0");
    try: midi=int(raw["midi"]);
    except (KeyError,TypeError,ValueError) as exc: raise ValueError(f"event {index}: invalid MIDI note") from exc;
    action=str(raw.get("event","on")).strip().lower();
    if action not in ("on","off"): raise ValueError(f"event {index}: event must be 'on' or 'off'");
    return {"time":timestamp,"midi":midi,"event":action,"_order":int(index)};


def normalise_piano_performance(events:Iterable[Mapping[str,object]],duration:Optional[float]=None,
                                base_midi:int=48,octave_shift:int=0)->Dict[str,object]:
    normalised=[_normalise_event(item,index) for index,item in enumerate(events)];
    normalised.sort(key=lambda item:(float(item["time"]),int(item["_order"])));
    clean=[];
    for item in normalised: clean.append({"time":round(float(item["time"]),6),"midi":int(item["midi"]),"event":str(item["event"])});
    last_event=max((float(item["time"]) for item in clean),default=0.0);
    if duration is None: duration=last_event;
    try: duration_value=max(0.0,float(duration));
    except (TypeError,ValueError) as exc: raise ValueError("invalid performance duration") from exc;
    duration_value=max(duration_value,last_event);
    return {
        "format":PIANO_PERFORMANCE_FORMAT,
        "version":PIANO_PERFORMANCE_VERSION,
        "duration":round(duration_value,6),
        "base_midi":int(base_midi),
        "octave_shift":int(octave_shift),
        "events":clean,
    };


def _validate_document(document:Mapping[str,object])->Dict[str,object]:
    if str(document.get("format",""))!=PIANO_PERFORMANCE_FORMAT: raise ValueError("not a SUM piano performance file");
    try: version=int(document.get("version",0));
    except (TypeError,ValueError) as exc: raise ValueError("invalid performance format version") from exc;
    if version!=PIANO_PERFORMANCE_VERSION: raise ValueError(f"unsupported SUM piano performance version: {version}");
    events=document.get("events",[]);
    if not isinstance(events,list): raise ValueError("performance events must be a list");
    return normalise_piano_performance(events,duration=document.get("duration"),base_midi=int(document.get("base_midi",48)),octave_shift=int(document.get("octave_shift",0)));


def piano_performance_paths(path:PathLike)->Tuple[Path,Path]:
    target=Path(path).expanduser();
    name=target.name;
    if name.endswith(".sumpiano.json"):
        json_path=target;
        text_path=target.with_name(name[:-5]);
    elif name.endswith(".sumpiano"):
        text_path=target;
        json_path=target.with_name(name+".json");
    elif target.suffix.lower()==".json":
        json_path=target;
        text_path=target.with_suffix(".sumpiano");
    else:
        json_path=target.with_name(name+".sumpiano.json");
        text_path=target.with_name(name+".sumpiano");
    return json_path,text_path;


def _timeline_segments(performance:Mapping[str,object])->List[Tuple[float,float,Tuple[int,...]]]:
    events=list(performance.get("events",[]));
    duration=max(0.0,float(performance.get("duration",0.0)));
    by_time:Dict[float,List[Mapping[str,object]]]={};
    for event in events: by_time.setdefault(float(event["time"]),[]).append(event);
    active=set();
    segments=[];
    cursor=0.0;
    for timestamp in sorted(by_time):
        timestamp=max(cursor,float(timestamp));
        if timestamp>cursor: segments.append((cursor,timestamp-cursor,tuple(sorted(active))));
        for event in by_time[timestamp]:
            midi=int(event["midi"]);
            if str(event["event"])=="off": active.discard(midi);
            else: active.add(midi);
        cursor=timestamp;
    if duration>cursor: segments.append((cursor,duration-cursor,tuple(sorted(active))));
    return segments;


def render_piano_performance(performance:Mapping[str,object])->str:
    perf=_validate_document(performance);
    duration=float(perf["duration"]);
    base_midi=int(perf["base_midi"]);
    octave_shift=int(perf["octave_shift"]);
    events=list(perf["events"]);
    lines=[
        "SUM Piano Performance",
        f"Format: {PIANO_PERFORMANCE_FORMAT}/{PIANO_PERFORMANCE_VERSION}",
        f"Duration: {duration:.3f} s",
        f"Base: {midi_note_name(base_midi)} (MIDI {base_midi})",
        f"Display octave shift: {octave_shift:+d}",
        f"Events: {len(events)}",
        "",
        "Timeline",
        "Start      Duration   Notes",
        "---------- ---------- ----------------------------------------",
    ];
    segments=_timeline_segments(perf);
    if not segments: lines.append("0.000      0.000      REST");
    for start,length,notes in segments:
        label="REST" if not notes else "["+" ".join(midi_note_name(midi) for midi in notes)+"]" if len(notes)>1 else midi_note_name(notes[0]);
        lines.append(f"{start:10.3f} {length:10.3f} {label}");
    lines.extend(["","Events","Time       Event Note       MIDI","---------- ----- ---------- -----"]);
    for event in events:
        midi=int(event["midi"]);
        lines.append(f"{float(event['time']):10.3f} {str(event['event']).upper():5s} {midi_note_name(midi):10s} {midi:5d}");
    return "\n".join(lines)+"\n";


def _atomic_write(path:Path,text:str)->None:
    path.parent.mkdir(parents=True,exist_ok=True);
    temp=path.with_name(path.name+".tmp");
    temp.write_text(text,encoding="utf-8");
    os.replace(temp,path);


def save_piano_performance(path:PathLike,events:Iterable[Mapping[str,object]],duration:Optional[float]=None,
                           base_midi:int=48,octave_shift:int=0)->Tuple[Path,Path]:
    perf=normalise_piano_performance(events,duration=duration,base_midi=base_midi,octave_shift=octave_shift);
    json_path,text_path=piano_performance_paths(path);
    payload=json.dumps(perf,ensure_ascii=False,indent=2,sort_keys=False)+"\n";
    _atomic_write(json_path,payload);
    _atomic_write(text_path,render_piano_performance(perf));
    return json_path,text_path;


def load_piano_performance(path:PathLike)->Dict[str,object]:
    source=Path(path).expanduser();
    if source.name.endswith(".sumpiano"): source=source.with_name(source.name+".json");
    document=json.loads(source.read_text(encoding="utf-8"));
    if not isinstance(document,dict): raise ValueError("performance root must be a JSON object");
    return _validate_document(document);
