import time
from dials.encoders import Encoders
from dials.switches import Switches
from dials.pixels import Pixels
from display.display import Display
from elkpy import sushicontroller as sc
from elk.brickworks import Brickworks

encoders = Encoders()
pixels = Pixels()
display = Display()
switches = Switches()
sushi = sc.SushiController()
procs = []
param_names = ['', '', '', '']
param_vals = [0.0, 0.0, 0.0, 0.0]
param_ids = [0, 0, 0, 0]

for t in sushi.audio_graph.get_all_tracks():
    for proc in sushi.audio_graph.get_track_processors(t.id):
        procs.append(proc)
active_proc_idx = 0
page = 0
offset = 0
selection = None
plugins = Brickworks().list_plugins()
active = []
while True:
    try:
        if page == 0:
            if switches.get_switch(0) is not switches.get_last_position(0):
                switches.set_last_position(0, switches.get_switch(0))
                if switches.get_switch(0) is False and selection is not None:
                    if selection < plugins.__len__():
                        if plugins[selection] in active:
                            active.remove(plugins[selection])
                            Brickworks().unload_plugin(Brickworks().get_plugin_name(plugins[selection]))
                        else:
                            active.append(plugins[selection])
                            Brickworks().load_plugin(Brickworks().get_plugin_name(plugins[selection]))
                        print('active', active)
        encoder_positions = encoders.get_positions()
        for n, rotary_pos in enumerate(encoder_positions):
            if rotary_pos != encoders.get_last_position(n):
                forward = rotary_pos > encoders.get_last_position(n)
                encoders.set_last_position(n, rotary_pos)
                position = (rotary_pos + 256) % 256
                pixels.set_color(n, position)  # wrap around to 0-256
                pixels.write(n)
                if page == 0 and n == 0:
                    selection = (rotary_pos + (plugins.__len__() + 1)) % (plugins.__len__() + 1)
                    if selection > (offset + 4):
                        if forward:
                            offset += 4
                        else:
                            offset = selection - 3
                    if selection < (offset):
                        if not forward:
                            offset -= 4
                        else:
                            offset = selection

                    if (plugins.__len__() - selection) < 3:
                        if forward:
                            offset = plugins.__len__() - 3
                            print('offset reduced', offset)
                    if offset < 0:
                        offset = 0
                    if selection > (plugins.__len__() - 1):
                        selection = plugins.__len__() - 1
                    if selection < 0:
                        selection = 0

        for i in range(offset, 4 + offset, 1):
            if i >= plugins.__len__():
                display_text = '--'
            else:
                display_text = plugins[i]
                if i == selection:
                    display_text = f'> {display_text}'
                if plugins[i] in active:
                    display_text = f'* {display_text}'
            display.set_text(i - offset, f'{display_text}')
        display.write()


    except KeyboardInterrupt:
        pixels.clear()
        display.clear()
        break