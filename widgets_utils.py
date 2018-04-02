####################################################################################################
# Widget Utilities
####################################################################################################
import ipywidgets as w
from IPython.display import display


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

allLayout_without_border = w.Layout(border='solid 0px',  padding='20px',
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

def create_tab(window_requirements, window_paretto, window_priority):
    tab_titles = ['Требования', 'Множество структур Паретто', 'Приоритетное требование']
    children = [window_requirements, window_paretto, window_priority]
    tab = w.Tab()
    tab.children = children
    for i in range(len(children)):
        tab.set_title(i, tab_titles[i])
    return tab