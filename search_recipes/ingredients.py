from pint import UnitRegistry
from pint.errors import UndefinedUnitError, DimensionalityError
ureg = UnitRegistry()

def extract_ingredient_data(ingredient_json):
    amount, unit, name = parse_ingredient_str(ingredient_json['text'])
    obj = {}
    obj[name] = {
        'amount': amount,
        'unit': unit,
        # 'processing': processing
    }
    return obj

# assumes ingredient_str has three or more words
# TODO optimize this method!!!!
# TODO not accounting for case where quantity takes up two words e.g. '1 1/2 lbs'
def parse_ingredient_str(ingredient_str):
    word_list = ingredient_str.split(' ')
    unit_word_cnt = 2
    units = ' '.join(word_list[:unit_word_cnt])
    quantity = try_parse_units(units)
    if quantity == None:
        quantity = try_parse_units(word_list[0])
        unit_word_cnt = 1

    if quantity == None:
        return [1, 'each', ingredient_str]

    if type(quantity) == int or type(quantity) == float:
        return [quantity, 'each', ' '.join(word_list[1:])]

    name = ' '.join(word_list[unit_word_cnt:])
    return [quantity.magnitude, quantity.units.__str__(), name]

def try_parse_units(s):
    try:
        return ureg.parse_expression(s)
    except (UndefinedUnitError, DimensionalityError):
        return None
