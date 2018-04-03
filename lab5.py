import ipywidgets as w
from IPython.display import display, clear_output
import json
import numpy as np

from widgets_utils import *
from utils import *

# Functions
def find_Pareto(parts, restriction):
    
    def combinations(parts, k):
        if k > 1:
            comb = [(*x, y) for x in combinations(parts, k-1) for y in parts[k]]
            return comb
        else:
            comb = [(x, y) for x in parts[k-1] for y in parts[k]]
            return comb
        
    def get_attribute_sum(comb, attr):
        attr_sum = 0
        for part in comb:
            attr_sum += list(part.values())[0][attr]
        return attr_sum
        
    new_parts = []
    for part in get_keys(parts): #restriction.keys():
        particular_parts = filter_parts(parts, part)
        for example in particular_parts:
            example_satisfies_conditions = True
            for attr in restriction[part].keys():
                if isinstance(restriction[part][attr], str):
                    condition = example[part][attr] == restriction[part][attr]
                elif isinstance(restriction[part][attr], tuple):
                    min_value, max_value = restriction[part][attr]
                    condition = example[part][attr] >= min_value and example[part][attr] <= max_value
                elif isinstance(restriction[part][attr], bool):
                    condition = not restriction[part][attr] or (example[part][attr] 
                                                                and restriction[part][attr])
                if not condition:
                    example_satisfies_conditions = False
                    break
            if example_satisfies_conditions:
                new_parts.append(example)

#     print(list(map(lambda part: '{}: {}'.format(part, filter_parts(new_parts, part) != []), get_keys(parts))))
    if not all(filter_parts(new_parts, part) != [] for part in get_keys(parts)):
        return []
        
    new_pparts = []
    for part in get_keys(new_parts):
        new_pparts.append(filter_parts(new_parts, part))
    filtered_combinations = []
    for comb in combinations(new_pparts, len(new_pparts)-1):
        min_cost, max_cost = restriction['Total']['cost']
        min_weight, max_weight = restriction['Total']['weight']
        comb_cost = get_attribute_sum(comb, 'price')
        comb_weight = get_attribute_sum(comb, 'weight')
        if comb_cost >= min_cost and comb_cost <= max_cost and \
        comb_weight >= min_weight and comb_weight <= max_weight:
            filtered_combinations.append(comb)
    return filtered_combinations

def analyse(b, parts, w1, w2, w3, w4, w5):
    restriction = {}
    for key in get_keys(parts):
        restriction[key] = {}
        
    restriction['Body']['material'] = w1.children[1].value
    restriction['Body']['portability'] = w1.children[2].value

    restriction['Engine']['engine_type'] = w2.children[1].value
    restriction['Engine']['number'] = w2.children[2].value
    restriction['Engine']['propulsion_type'] = w2.children[3].value
    restriction['Propeller']['material'] = w2.children[4].value
    restriction['Propeller']['number'] = w2.children[5].value

    restriction['Software']['GPS'] = w3.children[1].value
    restriction['Software']['AI'] = w3.children[2].value
    restriction['Software']['manufacturer'] = w3.children[3].value
    restriction['CPU']['frequency'] = w3.children[4].value
    restriction['CPU']['num_cores'] = w3.children[5].value
    restriction['Sensor']['signal_acceptance_distance'] = w3.children[6].value
    restriction['Camera']['resolution'] = w3.children[7].value
    restriction['Camera']['angle'] = w3.children[8].value
    restriction['Camera']['IR_illumination'] = w3.children[9].value

    restriction['Accumulator']['duration'] = w4.children[1].value
    restriction['Accumulator']['take_off_weight'] = w4.children[2].value
    restriction['Accumulator']['height'] = w4.children[3].value
    
    restriction['Total'] = {}
    restriction['Total']['cost'] = w5.children[1].value
    restriction['Total']['weight'] = w5.children[2].value
    
    Pareto_structures = find_Pareto(parts, restriction)
    visualize_structure(b, Pareto_structures, 1)

def calculate(rw1, rw2, rw3, rw4, rw5):
    rw5.children[1].children[1].value = str(get_price(parts, rw1.children[1].value,
                                                      rw2.children[1].value, rw2.children[2].value,
                                                      rw3.children[1].value, rw3.children[2].value,
                                                      rw3.children[3].value, rw3.children[4].value,
                                                      rw4.children[1].value)) + ' грн'
    rw5.children[2].children[1].value = str(get_weight(parts, rw1.children[1].value,
                                                       rw2.children[1].value, rw2.children[2].value,
                                                       rw3.children[1].value, rw3.children[2].value,
                                                       rw3.children[3].value, rw3.children[4].value,
                                                       rw4.children[1].value)) + ' г'
     
def set_structure(combinations, i, rw1, rw2, rw3, rw4, rw5):
    rw1.children[1].value = combinations[i]['Body']['name'] # get_comb_attr(combinations, 'Body', 'name')[i]
    rw2.children[1].value = combinations[i]['Engine']['name'] # get_comb_attr(combinations, 'Engine', 'name')[i]
    rw2.children[2].value = combinations[i]['Propeller']['name'] # get_comb_attr(combinations, 'Propeller', 'name')[i]
    rw3.children[1].value = combinations[i]['CPU']['name'] # get_comb_attr(combinations, 'CPU', 'name')[i]
    rw3.children[2].value = combinations[i]['Sensor']['name'] # get_comb_attr(combinations, 'Sensor', 'name')[i]
    rw3.children[3].value = combinations[i]['Software']['name'] # get_comb_attr(combinations, 'Software', 'name')[i]
    rw3.children[4].value = combinations[i]['Camera']['name'] # get_comb_attr(combinations, 'Camera', 'name')[i]
    rw4.children[1].value = combinations[i]['Accumulator']['name'] # get_comb_attr(combinations, 'Accumulator', 'name')[i]
    calculate(rw1, rw2, rw3, rw4, rw5)
        
def get_template_structures(combinations):    
    if len(combinations) == 0:
        all_widgets = w.Label('К сожалению, нет структуры, которая бы удовлетворяла текущие требования.',
                       layout=allLayout_without_border)
        return all_widgets
    
    ####################################################################################################
    # Іміджева складова
    ####################################################################################################
    rw1_widgets = [
        widget_typeBox('Корпус', get_comb_attr(combinations, 'Body', 'name'), disabled=True),
    ]

    rw1 = widget_group('Внешний вид', rw1_widgets)

    ####################################################################################################
    # Механічна складова
    ####################################################################################################
    rw2_widgets = [
        widget_typeBox('Двигатели', get_comb_attr(combinations, 'Engine', 'name'), disabled=True),

        widget_typeBox('Пропеллеры', get_comb_attr(combinations, 'Propeller', 'name'), disabled=True),
    ]
    rw2 = widget_group('Механика', rw2_widgets)

    ####################################################################################################
    # Апаратна складова
    ####################################################################################################
    rw3_widgets = [
        widget_typeBox('Процессор', get_comb_attr(combinations, 'CPU', 'name'), disabled=True),

        widget_typeBox('Датчик связи', get_comb_attr(combinations, 'Sensor', 'name'), disabled=True),

        widget_typeBox('Программное обеспечение', get_comb_attr(combinations, 'Software', 'name'),
                       disabled=True),
        widget_typeBox('Камера', get_comb_attr(combinations, 'Camera', 'name'), disabled=True),
    ]
    rw3 = widget_group('Аппаратная составляющая', rw3_widgets)

    ####################################################################################################
    # Акумулятор
    ####################################################################################################
    rw4_widgets = [
        widget_typeBox('Аккумулятор', get_comb_attr(combinations, 'Accumulator', 'name'), disabled=True),
    ]
    rw4 = widget_group('Аккумулятор', rw4_widgets)

    ####################################################################################################
    # Total
    ####################################################################################################
    totalLayout = w.Layout(width='200px', justify_content='flex-end')
    rw5_widgets = [
          w.HBox([w.Label(value='Общая стоимость:', style=title_style),
                  w.Label(value='', style=title_style)], layout=totalLayout),
          w.HBox([w.Label(value='Общий вес:', style=title_style),
                  w.Label(value='', style=title_style)], layout=totalLayout),
    ]
    rw5 = widget_group('', rw5_widgets)
    return rw1, rw2, rw3, rw4, rw5

def get_Pareto_structures(combinations):
    rw1, rw2, rw3, rw4, rw5 = get_template_structures(combinations)
    
    rs1 = w.IntSlider(value=1, min=1, max=len(combinations), step=1,
                      description='Структура')
    
    rs2 = w.interactive_output(lambda x: set_structure(combinations, x-1,
                                                       rw1, rw2, rw3, rw4, rw5), {'x': rs1})
        
    all_widgets = w.HBox([w.VBox([rw1, rw2, rw5], layout=bigGroup),
                          w.VBox([rw3, rw4, rs1], layout=bigGroup)],
                         layout=allLayout_without_border)
    return all_widgets

def get_numerical_parameters(combination):
    options = []
    for element_key in combination.keys():
        for param_key in list(filter(lambda key: key != 'price' and key != 'weight',
                                     combination[element_key].keys())):
            if not isinstance(combination[element_key][param_key], str) and \
            not isinstance(combination[element_key][param_key], bool) and \
            np.random.rand() < 0.5:
#                 print(element_key, param_key, combination[element_key][param_key])
                options.append('The highest value of {} {}'.format(element_key, param_key))
                options.append('The least value of {} {}'.format(element_key, param_key))
    return options

def find_priority_structure(combinations, element_key, param_key, value_type):
    values = np.array([combination[element_key][param_key] for combination in combinations])
    if value_type == 'highest' or value_type == 'max':
        return values.argmax()
    return values.argmin()

def find_priority_structure_by_total(combinations, attr_name, value_type):
    values = []
    for combination in combinations:
        value = 0
        for element_key in combination.keys():
            value += combination[element_key][attr_name]
        values.append(value)
    values = np.array(values)
    if value_type == 'max':
        return values.argmax()
    return values.argmin()

def change_values_and_set_structure(combinations, x, rw1, rw2, rw3, rw4, rw5):
    if x == 'The cheapest':
        i = find_priority_structure_by_total(combinations, 'price', 'min')
    elif x == 'The most expensive':
        i = find_priority_structure_by_total(combinations, 'price', 'max')
    elif x == 'The most lightweight':
        i = find_priority_structure_by_total(combinations, 'weight', 'min')
    else:
        x_list = x.split(' ')
        i = find_priority_structure(combinations, x_list[4], x_list[5], x_list[1])
    set_structure(combinations, i, rw1, rw2, rw3, rw4, rw5)

def get_priority_structure(combinations, i=0):
    rw1, rw2, rw3, rw4, rw5 = get_template_structures(combinations)
    
#     w.interact(lambda x: set_structure(combinations, x, rw1, rw2, rw3, rw4, rw5), x=rs1)
    
    options = get_numerical_parameters(combinations[0])
    options.append('The cheapest')
    options.append('The most expensive')
    options.append('The most lightweight')
    
    rc1 = widget_typeBox('CHOOSING BY', options)
    rc2 = w.interactive_output(lambda x: change_values_and_set_structure(combinations, x,
                                                                         rw1, rw2, rw3, rw4, rw5),
                               {'x': rc1})
    
    set_structure(combinations, i, rw1, rw2, rw3, rw4, rw5)
    
    all_widgets = w.HBox([w.VBox([rw1, rw2, rw5], layout=bigGroup),
                          w.VBox([rw3, rw4, rc1], layout=bigGroup)],
                         layout=allLayout_without_border)
    return all_widgets

def visualize_structure(b, Pareto_structures, i):
    
    def simplify_data_structure(combinations):
        new_combinations = []
        for combination in combinations:
            new_combination = {}
            for element in combination:
                new_combination[list(element.keys())[0]] = list(element.values())[0]
            new_combinations.append(new_combination)
        return new_combinations

    simplified_Pareto_structures = simplify_data_structure(Pareto_structures)
    all_widgets = get_Pareto_structures(simplified_Pareto_structures)
    window_paretto = w.VBox([widget_header('Lab 5', bold=False, face=facefont),
        widget_header('Дрон. Множество структур Паретто', bold=False, size=5, face=facefont),
        widget_header('(мощность множества: {})'.format(len(Pareto_structures)),
                      bold=False, size=5, face=facefont),
        all_widgets], layout=allLayout)
    
    np.random.seed(0)
    i = np.random.randint(0, len(simplified_Pareto_structures))
    all_widgets = get_priority_structure(simplified_Pareto_structures, i)
    window_priority = w.VBox([widget_header('Lab 5', bold=False, face=facefont),
        widget_header('Дрон. Приоритетное требование', bold=False, size=5, face=facefont),
        all_widgets], layout=allLayout)
    
    tab = create_tab(window_requirements, window_paretto, window_priority)
    clear_output()
    display(tab)
    

# Visualization
def get_main_window_requirements(parts):
    ####################################################################################################
    # Іміджева складова
    ####################################################################################################
    w1_widgets = [
        widget_typeBox('Материал корпуса', get_part_attr(parts, 'Body', 'material')),
        widget_flag('Портативность')
    ]
    w1 = widget_group('Внешний вид', w1_widgets)

    ####################################################################################################
    # Механічна складова
    ####################################################################################################
    w2_widgets = [
        widget_typeBox('Тип двигателя', get_part_attr(parts, 'Engine', 'engine_type')),
        widget_rangeBoxInt('Число двигателей', *get_boundaries(parts, 'Engine', 'number')),
        widget_typeBox('Тип движителя', get_part_attr(parts, 'Engine', 'propulsion_type')),

        widget_typeBox('Материал пропеллера', get_part_attr(parts, 'Propeller', 'material')),
        widget_rangeBoxInt('Число пропеллеров', *get_boundaries(parts, 'Propeller', 'number')),
    ]
    w2 = widget_group('Механика', w2_widgets)

    ####################################################################################################
    # Апаратна складова
    ####################################################################################################
    w3_widgets = [
        widget_flag('Наличие GPS'),
        widget_flag('Наличие ИИ'),
        widget_typeBox('Производитель ', get_part_attr(parts, 'Software', 'manufacturer')),

        widget_rangeBoxFloat('Частота процессора, Гц', *get_boundaries(parts, 'CPU', 'frequency')),
        widget_rangeBoxInt('Количество ядер процессора', *get_boundaries(parts, 'CPU', 'num_cores')),

        widget_rangeBoxFloat('Дальность приема сигнала, м', *get_boundaries(parts, 'Sensor',
                                                                            'signal_acceptance_distance')),

        widget_rangeBoxFloat('Разрешение матрицы, Мп', *get_boundaries(parts, 'Camera', 'resolution')),
        widget_rangeBoxInt('Угол обзора', *get_boundaries(parts, 'Camera', 'angle')),
        widget_rangeBoxInt('Дальность ИК подсветки, м', *get_boundaries(parts, 'Camera', 'IR_illumination')),
    ]
    w3 = widget_group('Аппаратная составляющая', w3_widgets)

    ####################################################################################################
    # Акумулятор
    ####################################################################################################
    w4_widgets = [
        widget_rangeBoxInt('Продолжительность полета, мин', *get_boundaries(parts, 'Accumulator', 'duration')),
        widget_rangeBoxInt('Взлетная масса, кг', *get_boundaries(parts, 'Accumulator', 'take_off_weight')),
        widget_rangeBoxInt('Высота полета, м', *get_boundaries(parts, 'Accumulator', 'height')),
    ]
    w4 = widget_group('Аккумулятор', w4_widgets)

    ####################################################################################################
    # Total
    ####################################################################################################
    w5_widgets = [
    #     widget_rangeBox('Общая стоимость', 0, 1000),
    #     widget_rangeBox('Общий вес', 0, 1000)
         widget_rangeBoxInt('Стоимость, грн', 0, 30000),
         widget_rangeBoxInt('Общий вес, г', 0, 1000),
    ]
    layout = w.Layout(width='480px', border='solid 0px', margin='10px',
                      justify_content='center', align_items='center')
    w5 = widget_group('', w5_widgets, layout=layout)

    b1 = w.Button(
        description='Анализ',
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
    )

    b1.on_click(lambda b: analyse(b, parts, w1, w2, w3, w4, w5))
    all_widgets = w.HBox([w.VBox([w1, w2, w5, b1], layout=bigGroup), w.VBox([w3, w4], layout=bigGroup)])
    return all_widgets

if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        parts = json.load(f)

    all_widgets = get_main_window_requirements(parts)
    window_requirements = w.VBox([widget_header('Lab 5', bold=False, face=facefont),
                widget_header('Дрон. Требования к функциональным элементам', bold=False, size=5, face=facefont),
                all_widgets], layout=allLayout)

    window_paretto = w.VBox([widget_header('Lab 5', bold=False, face=facefont),
            widget_header('Дрон. Множество структур Паретто', bold=False, size=5, face=facefont),
            w.Label('')], layout=allLayout)

    window_priority = w.VBox([widget_header('Lab 5', bold=False, face=facefont),
            widget_header('Дрон. Приоритетная структура', bold=False, size=5, face=facefont),
            w.Label('')], layout=allLayout)

    tab = create_tab(window_requirements, window_paretto, window_priority)
    display(tab)