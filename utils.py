import ipywidgets as w
from IPython.display import display


####################################################################################################
# Widgets Utilities
####################################################################################################

hcolor='#0969A2'
textLayout = w.Layout(width='180px', height='30px')

rangeLayout = w.Layout(width='400px', justify_content='flex-start')
typeLayout = w.Layout(width='400px', justify_content='center')

smallGroup = w.Layout(width='450px', border='solid 0px', margin='0px',
                      justify_content='center', align_items='center')

bigGroup = w.Layout(width='500px', border='solid 0px', height='530px', padding='20px',
                    justify_content='space-around', align_items='center')

allLayout = w.Layout(border='solid 1px',  padding='20px',
                    justify_content='center', align_items='stretch')

title_style = {'description_width': 'initial'}

facefont = 'Arial'


def widget_header(title, size=6, bold=True, color='#0969A2', face=facefont):
    attr = "<div align='center'><font size='"+str(size)+"px' face='"+face+"' color='"+hcolor+"'>"
    attr_closing = "</font></div>"
    if bold:
        attr += "<b>"
        attr_closing = "</b>" + attr_closing

    return w.HTML(value=attr+title+attr_closing)

def widget_intFrom(value, layout=textLayout):
    return w.BoundedIntText(value=value,
                            step=1,
                            description='від',
                            disabled=False,
                            layout=layout)

def widget_intTo(value, layout=textLayout):
    return w.BoundedIntText(value=value,
                            step=1,
                            description='до',
                            disabled=False,
                            layout=layout)

def widget_range(valueFrom, valueTo):
    return w.HBox([widget_intFrom(valueFrom), widget_intTo(valueTo)])

def widget_rangeBoxInt(title, valueFrom, valueTo, style=title_style, layout=rangeLayout):
    return w.FloatRangeSlider(value=[valueFrom, valueTo],
                            min=valueFrom,
                            max=valueTo,
                            step=1,
                            description=title,
                            disabled=False,
                            continuous_update=False,
                            orientation='horizontal',
                            readout=True,
                            readout_format='d',
                            style=style,
                            layout=layout)

def widget_rangeBoxFloat(title, valueFrom, valueTo, style=title_style, layout=rangeLayout):
    return w.FloatRangeSlider(value=[valueFrom, valueTo],
                            min=valueFrom,
                            max=valueTo,
                            step=0.1,
                            description=title,
                            disabled=False,
                            continuous_update=False,
                            orientation='horizontal',
                            readout=True,
                            readout_format='.1f',
                            style=style,
                            layout=layout)

def widget_rangeBox(title, valueFrom, valueTo, style=title_style, layout=rangeLayout):
    return w.HBox([w.Label(value=title, style=style), widget_range(valueFrom, valueTo)], layout=layout)

def widget_typeBox2(title, options, style=title_style, layout=typeLayout):
    return w.Dropdown(options= dict(zip(options, range(len(options)))),
                      value=0,
                      description=title,
                      style=style,
                      layout=layout)

def widget_typeBox(title, options, style=title_style, layout=typeLayout):
    return w.Dropdown(options=options,
                      value=options[0],
                      description=title,
                      style=style,
                      layout=layout)

def widget_group(title, widgets, layout=smallGroup):
    h = widget_header(title, bold=False, size=4)
    return w.VBox([h, *widgets], layout=layout)

def widget_flag(title):
    return w.Checkbox(
    value=False,
    description=title,
    style = {'description_width': 'initial'},
)



####################################################################################################
# Data Utilities
####################################################################################################

class Part():
    def __init__(self, name, price, weight):
        self.name = name
        self.price = price
        self.weight = weight
        
    def jsonDefault(self):
        return self.__dict__

    
class Body(Part):
    def __init__(self, name, price, weight, portability, material):
        super().__init__(name, price, weight)
        self.portability = portability
        self.material = material

        
class Engine(Part):
    def __init__(self, name, price, weight, engine_type, number, propulsion_type):
        super().__init__(name, price, weight)
        self.engine_type = engine_type
        self.number = number
        self.propulsion_type = propulsion_type

        
class Propeller(Part):
    def __init__(self, name, price, weight, material, number):
        super().__init__(name, price, weight)
        self.material = material
        self.number = number

        
class Software(Part):
    def __init__(self, name, price, GPS, AI, manufacturer):
        super().__init__(name, price, 0)
        self.GPS = GPS
        self.AI = AI
        self.manufacturer = manufacturer
        
        
class CPU(Part):
    def __init__(self, name, price, frequency, num_cores):
        super().__init__(name, price, 0)
        self.frequency = frequency
        self.num_cores = num_cores

        
class Sensor(Part):
    def __init__(self, name, signal_acceptance_distance):
        super().__init__(name, 0, 0)
        self.signal_acceptance_distance = signal_acceptance_distance

        
class Camera(Part):
    def __init__(self, name, price, resolution, angle, IR_illumination):
        super().__init__(name, price, 200)
        self.resolution = resolution
        self.angle = angle
        self.IR_illumination = IR_illumination

        
class Accumulator(Part):
    def __init__(self, name, price, duration, take_off_weight, height):
        super().__init__(name, price, 200)
        self.duration = duration
        self.take_off_weight = take_off_weight
        self.height = height

        
def get_keys(parts):
    return set(map(lambda part: list(part.keys())[0], parts))

def filter_parts(parts, part_name):
    return list(filter(lambda part: list(part.keys())[0] == part_name, parts))

def get_attr(parts, attr_name):
    return sorted(set(list(map(lambda part: part[list(part.keys())[0]][attr_name], parts))))

def get_part_attr(parts, part_name, attr_name):
    return get_attr(filter_parts(parts, part_name), attr_name)

def get_boundaries(parts, part_name, attr_name):
    values = get_attr(filter_parts(parts, part_name), attr_name)
    return (min(values), max(values))