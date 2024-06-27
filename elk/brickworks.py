from elkpy.sushi_info_types import PluginType
from elkpy import sushicontroller as sc

PLUGINS = {
    'bitcrusher': {
        'display': 'Bitcrusher',
        'type': PluginType.INTERNAL,
        'params': {
            'sr_ratio': {
                'min': 0.0,
                'max': 1.0,
                'interval': 0.1,
                'default': 1.0
            },
            'bit_depth': {
                'min': 1.0,
                'max': 16.0,
                'interval': 1.0,
                'default': 16.0
            }
        }
    },
    'chorus': {
        'display': 'Chorus',
        'type': PluginType.INTERNAL,
        'params': {
            'rate': {
                'min': 0.1,
                'max': 2.0,
                'interval': 0.1,
                'default': 1.0
            },
            'amount': {
                'min': 0.0,
                'max': 1.0,
                'interval': 0.1,
                'default': 0
            }
        }
    },
    'clip': {
        'display': 'Clip',
        'type': PluginType.INTERNAL,
        'params': {
            'bias': {
                'min': -2.5,
                'max': 2.5,
                'interval': 0.25,
                'default': 0
            },
            'gain': {
                'min': 0.0,
                'max': 10.0,
                'interval': 0.5,
                'default': 1.0
            }
        }
    },
    'comb_delay': {
        'display': 'Comb Delay',
        'type': PluginType.INTERNAL,
        'params': {
            'ff_delay': {
                'min': 0.0,
                'max': 1.0,
                'interval': 0.1,
                'default': 0.5
            },
            'fb_delay': {
                'min': 0.0,
                'max': 1.0,
                'interval': 0.1,
                'default': 0.5
            },
            'ff_coeff': {
                'min': -1.0,
                'max': 1.0,
                'interval': 0.1,
                'default': 0
            },
            'fb_coeff': {
                'min': -0.995,
                'max': 0.995,
                'interval': 0.1,
                'default': 0
            }
        }
    },
    'compressor': {
        'display': 'Compressor',
        'type': PluginType.INTERNAL,
        'params': {
            'threshold': {
                'min': -60.0,
                'max': 12.0,
                'interval': 1,
                'default': 0
            },
            'ratio': {
                'min': 0.0,
                'max': 1.0,
                'interval': 0.1,
                'default': 1.0
            },
            'attack': {
                'min': 0.0,
                'max': 1.0,
                'interval': 0.1,
                'default': 0
            },
            'release': {
                'min': 0.0,
                'max': 1.0,
                'interval': 0.1,
                'default': 0
            },
            'gain': {
                'min': -60.0,
                'max': 60.0,
                'interval': 1,
                'default': 0
            }
        }
    },
}

class Brickworks:
    def __init__(self):
        self.plugins = PLUGINS
        self.audio_graph = sc.SushiController().audio_graph
        self.parameter_controller = sc.SushiController().parameters

    def get_plugins(self):
        return self.plugins

    def list_plugins(self):
        plugins = []
        for plugin in self.plugins:
            plugins.append(self.get_plugin_display(plugin))
        return plugins

    def get_plugin(self, plugin_name):
        return self.plugins[plugin_name]

    def get_plugin_params(self, plugin_name):
        return self.plugins[plugin_name]['params']

    def get_plugin_param(self, plugin_name, param_name):
        return self.plugins[plugin_name]['params'][param_name]

    def get_plugin_param_min(self, plugin_name, param_name):
        return self.plugins[plugin_name]['params'][param_name]['min']

    def get_plugin_param_max(self, plugin_name, param_name):
        return self.plugins[plugin_name]['params'][param_name]['max']

    def get_plugin_param_interval(self, plugin_name, param_name):
        return self.plugins[plugin_name]['params'][param_name]['interval']

    def get_plugin_param_default(self, plugin_name, param_name):
        return self.plugins[plugin_name]['params'][param_name]['default']

    def get_plugin_type(self, plugin_name):
        return self.plugins[plugin_name]['type']

    def get_plugin_name(self, display_name):
        for plugin in self.plugins:
            if self.get_plugin_display(plugin) == display_name:
                return plugin
        return None

    def get_plugin_display(self, plugin_name):
        return self.plugins[plugin_name]['display']

    def load_plugin(self, plugin_name):
        uid = f"sushi.brickworks.{plugin_name}"
        self.audio_graph.create_processor_on_track(plugin_name, uid, "", self.get_plugin_type(plugin_name), 0, 0, True)

    def unload_plugin(self, plugin_name):
        id = self.audio_graph.get_processor_id(plugin_name)
        self.audio_graph.delete_processor_from_track(id, 0)

    def get_param_value(self, plugin_name, param_name):
        id = self.audio_graph.get_processor_id(plugin_name)
        param_id = self.parameter_controller.get_parameter_id(id, param_name)
        return self.parameter_controller.get_parameter_value(id, param_id)

    def set_param_value(self, plugin_name, param_name, value):
        id = self.audio_graph.get_processor_id(plugin_name)
        param_id = self.audio_graph.get_parameter_id(id, param_name)
        self.parameter_controller.set_parameter_value(id, param_id, value)

