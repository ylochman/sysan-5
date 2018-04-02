####################################################################################################
# Data Utilities
####################################################################################################

#######################
# Class PART
#######################
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

##########################
# For searching in parts
##########################        
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

#################################
# For searching in combinations
#################################
def get_comb_attr(combinations, part_name, attr_name):
    return [comb[part_name][attr_name] for comb in combinations]


#######################
# Final calculations
#######################
def get_price(parts, body, engine, propellers, cpu, sensor, software, camera, accumulator):
    names = list(map(lambda part: list(part.values())[0]['name'], parts))
    price = 0
    for name in [body, engine, propellers, cpu, sensor, software, camera, accumulator]:
        assert name in names, '{} is not a valid name'.format(name)
        price += get_attr(list(filter(lambda part: list(part.values())[0]['name'] == name, parts)), 'price')[0]
    return price

def get_weight(parts, body, engine, propellers, cpu, sensor, software, camera, accumulator):
    names = list(map(lambda part: list(part.values())[0]['name'], parts))
    weight = 0
    for name in [body, engine, propellers, cpu, sensor, software, camera, accumulator]:
        assert name in names, '{} is not a valid name'.format(name)
        weight += get_attr(list(filter(lambda part: list(part.values())[0]['name'] == name, parts)), 'weight')[0]
    return weight