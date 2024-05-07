import math
from loguru import logger

"""Расчет объемов и времени циркуляции"""

# Параметры обсадной колонны
casing_diameter = 0.146  # Диаметр обсадной колонны, м (✔️)
casing_inner_diameter = 0.13  # Внутренний диаметр колонны, м (✔️)
casing_shoe_depth = 2283  # Глубина башмака колонны, м (✔️)

# Параметры бурения
bit_diameter = 0.126  # Диаметр долота, м (✔️)
cavernosity_coefficient_1 = 1.1  # Коэффициент кавернозности (✔️)
hole_depth = 3067  # Забой, м (✔️)
tool_depth = 3067  # Глубина спуска инструмента, м (✔️)

# Параметры бурильных труб
drill_pipe_diameter = 0.089  # Диаметр СБТ, м (✔️)
drill_pipe_inner_diameter = 0.071  # Внутренний диаметр СБТ, м (✔️)

# Параметры насоса
pump_volume = 36  # Объем в мерниках (✔️)
pump_strokes_per_minute = 35  # Количество 2х ходов в минуту (✔️)
piston_diameter = 0.14  # Диаметр поршня, м (✔️)
piston_stroke_length = 0.387  # Длина хода поршня, м (✔️)
filling_coefficient = 0.95  # Коэффициент наполнения (✔️)
number_of_pistons = 3  # Количество поршней (✔️)

# Неизвестные параметры (требуют расчета или уточнения)
landing_string_diameter = 0  # Диаметр ЛБТ (Вводимые данные????)
landing_string_inner_diameter = 0  # Внутренний диаметр ЛБТ (Вводимые данные????)
landing_string_length = 0  # Длина ЛБТ (Вводимые данные????)
upper_drill_pipe_diameter = 0  # Диаметр УБТ (Вводимые данные????)
upper_drill_pipe_length = 0  # Длина УБТ (Вводимые данные????)
upper_drill_pipe_inner_diameter = 0  # Внутренний диаметр УБТ (Вводимые данные????)


# Объемы

def casing_volume():
    """Объем колонны, м^3"""
    casing_volume_variable = 0.785 * math.pow(casing_inner_diameter, 2) * casing_shoe_depth
    return casing_volume_variable


def casing_volume_with_tool():
    """Объем колонны с инструментом в башмаке, м^3"""
    tool_volume_variable = tool_volume()
    casing_volume_variable = casing_volume()
    casing_volume_with_tool = casing_volume_variable - tool_volume_variable
    return casing_volume_with_tool


def wellbore_volume():
    """Объем скважины, м^3"""
    casing_volume_variable = casing_volume()
    wellbore_volume_variable = casing_volume_variable + (pow(bit_diameter, 2) * 0.785 *
                                                         (hole_depth - casing_shoe_depth)) * cavernosity_coefficient_1
    return wellbore_volume_variable


def wellbore_volume_with_tool():
    """Объем скважины с инструментом в башмаке, м^3"""
    tool_volume_variable = tool_volume()  # Объем инструмента в башмаке, м^3
    wellbore_volume_variable = wellbore_volume()  # Объем скважины, м^3
    wellbore_volume_with_tool_variable = wellbore_volume_variable - tool_volume_variable
    return wellbore_volume_with_tool_variable


def annulus_volume():
    """Объем ствола (затрубного пространства), м^3"""
    casing_volume_variable = casing_volume()
    wellbore_volume_variable = wellbore_volume()  # Объем скважины, м^3
    annulus_volume_variable = wellbore_volume_variable - casing_volume_variable
    return annulus_volume_variable


def drill_pipe_volume():
    """Объем СБТ, м^3"""
    drill_pipe_volume_variable = (0.785 * (pow(drill_pipe_diameter, 2) -
                                           pow(drill_pipe_inner_diameter, 2)) *
                                  (tool_depth - landing_string_length - upper_drill_pipe_length))  # Объем СБТ, м^3
    return drill_pipe_volume_variable


def landing_string_volume():
    """Объем ЛБТ, м^3"""
    landing_string_volume_variable = 0.785 * (pow(landing_string_diameter, 2) -
                                              pow(landing_string_inner_diameter, 2)) * landing_string_length
    return landing_string_volume_variable


def upper_drill_pipe_volume():
    """Объем УБТ, м^3"""
    upper_drill_pipe_volume = (0.785 * (pow(upper_drill_pipe_diameter, 2) - pow(upper_drill_pipe_inner_diameter, 2)) *
                               upper_drill_pipe_length)  # Объем УБТ, м^3
    return upper_drill_pipe_volume


def tool_volume():
    """Объем инструмента, м^3"""
    drill_pipe_volume_variable = drill_pipe_volume()
    landing_string_volume_variable = landing_string_volume()  # Объем ЛБТ, м^3
    tool_volume_variable = drill_pipe_volume_variable + landing_string_volume_variable + upper_drill_pipe_volume
    return tool_volume_variable


def tool_internal_volume():
    """Объем в инструменте, м^3"""
    tool_internal_variable = (upper_drill_pipe_length * 0.785 * pow(upper_drill_pipe_inner_diameter, 2) +
                              landing_string_length * 0.785 * pow(landing_string_inner_diameter, 2) + 0.785 *
                              pow(drill_pipe_inner_diameter, 2) * (hole_depth - upper_drill_pipe_length -
                                                                   landing_string_length))
    return tool_internal_variable


def annulus_fluid_volume():
    """Объем в затрубье, м^3"""
    wellbore_volume_variable = wellbore_volume()  # Объем скважины, м^3
    annulus_fluid_volume_variable = wellbore_volume_variable - (upper_drill_pipe_length * 0.785 *
                                                                pow(upper_drill_pipe_diameter, 2) +
                                                                landing_string_length * 0.785 *
                                                                pow(landing_string_diameter, 2) + 0.785 *
                                                                pow(drill_pipe_diameter, 2) * (hole_depth -
                                                                                               upper_drill_pipe_length -
                                                                                               landing_string_length))
    return annulus_fluid_volume_variable


def total_circulation_volume():
    """Общий объем циркуляции, м^3"""
    wellbore_volume_with_tool_variable = wellbore_volume_with_tool()
    total_circulation_volume_variable = wellbore_volume_with_tool_variable + pump_volume
    return total_circulation_volume_variable


# Времена циркуляции
def wellbore_circulation_time():
    """Время циркуляции скважины, мин"""
    wellbore_volume_with_tool_variable = wellbore_volume_with_tool()
    pump_flow_rate_cubic_meter_variable = pump_flow_rate_cubic_meter()
    wellbore_circulation_time_variable = wellbore_volume_with_tool_variable / pump_flow_rate_cubic_meter_variable
    return wellbore_circulation_time_variable


def total_circulation_time():
    """Время циркуляции общая, мин"""
    wellbore_volume_with_tool_variable = wellbore_volume_with_tool()
    pump_flow_rate_cubic_meter_variable = pump_flow_rate_cubic_meter()
    total_circulation_time_variable = ((wellbore_volume_with_tool_variable + pump_volume) /
                                       pump_flow_rate_cubic_meter_variable)
    return total_circulation_time_variable


def annulus_circulation_time():
    """Время циркуляции затрубья, мин"""
    annulus_fluid_volume_variable = annulus_fluid_volume()
    pump_flow_rate_cubic_meter_variable = pump_flow_rate_cubic_meter()
    annulus_circulation_time_variable = annulus_fluid_volume_variable / pump_flow_rate_cubic_meter_variable
    return annulus_circulation_time_variable


def tool_circulation_time():
    """Время циркуляции инструмента, мин"""
    tool_internal_variable = tool_internal_volume()
    pump_flow_rate_cubic_meter_variable = pump_flow_rate_cubic_meter()
    tool_circulation_time_variable = tool_internal_variable / pump_flow_rate_cubic_meter_variable
    return tool_circulation_time_variable


def casing_circulation_time():
    """Время циркуляции колонны"""

    tool_volume_variable = tool_volume()
    casing_volume_variable = casing_volume()
    casing_volume_with_tool = casing_volume_variable - tool_volume_variable  # Объем колонны с инструментом в башмаке

    pump_flow_rate_cubic_meter_variable = pump_flow_rate_cubic_meter()
    casing_circulation_time_variable = casing_volume_with_tool / pump_flow_rate_cubic_meter_variable
    return casing_circulation_time_variable


# Параметры насоса (производительность)
def pump_flow_rate_cubic_meter():
    """Производительность насоса, м^3/мин"""
    pump_flow_rate_cubic_meter_variable = (0.785 * pow(piston_diameter, 2) * piston_stroke_length *
                                           pump_strokes_per_minute * number_of_pistons * filling_coefficient)
    return pump_flow_rate_cubic_meter_variable


def pump_flow_rate_liter_per_second():
    """Производительность насоса, л/сек"""
    pump_flow_rate_cubic_meter_variable = pump_flow_rate_cubic_meter()
    pump_flow_rate_liter_per_second_variable = pump_flow_rate_cubic_meter_variable * 1000 / 60
    return pump_flow_rate_liter_per_second_variable


""" Расчет утяжеления раствора """

# Параметры бурового раствора
initial_density = 1.09  # Начальная плотность, г/см^3 (✔️)
final_density = 1.12  # Конечная плотность, г/см^3 (✔️)
weighting_material_density = 2720  # Плотность утяжелителя, кг/м^3 (✔️)
solution_volume = 20  # Объем раствора, м^3 (✔️)


def weighting_material_mass_calculated():
    """Масса утяжелителя, кг"""
    weighting_material_mass_calculated = (((final_density - initial_density) /
                                           (weighting_material_density / 1000 - final_density)) *
                                          weighting_material_density * solution_volume)
    return weighting_material_mass_calculated


def weighting_material_volume():
    """Объем утяжелителя, м^3"""
    weighting_material_mass_calculated = (((final_density - initial_density) /
                                           (weighting_material_density / 1000 - final_density)) *
                                          weighting_material_density * solution_volume)
    weighting_material_volume = weighting_material_mass_calculated / weighting_material_density
    return weighting_material_volume


def final_solution_volume():
    """Конечный объем раствора, м^3"""
    final_solution_volume = solution_volume + weighting_material_volume
    return final_solution_volume


def number_of_weighting_material_bags():
    """Количество мешков утяжелителя"""
    number_of_weighting_material_bags = weighting_material_mass_calculated / 40
    return number_of_weighting_material_bags


def chalk_concentration():
    """Концентрация мела, кг/м^3"""
    chalk_concentration = weighting_material_mass_calculated / solution_volume
    return chalk_concentration


# Дополнительные параметры (возможно, для другой ситуации или расчета)
weighting_material_mass = 1000  # Масса утяжелителя, кг (✔️)
initial_density_kg_m3 = 1180  # Начальная плотность, кг/м^3 (возможно, дублирование) (✔️)
weighting_material_density_2 = 2000  # Плотность утяжелителя, кг/м^3 (возможно, дублирование) (✔️)
solution_volume_2 = 47  # Объем раствора, м^3 (возможно, дублирование) (✔️)


def final_density_calculated():
    """Конечная плотность, г/см^3"""
    final_density_calculated_variable = ((weighting_material_mass * weighting_material_density_2 +
                                          initial_density_kg_m3 * weighting_material_density_2 * solution_volume_2) /
                                         (weighting_material_density_2 * solution_volume_2 +
                                          weighting_material_mass) / 1000)
    return final_density_calculated_variable


ikkarb_concentration = 0  # Концентрация ИККАРБ, кг/м^3

# Расчет глушения скважины

# Параметры давления и глубины
vertical_depth = 2278  # Глубина по вертикали, м (✔️)
excess_pressure_on_riser = 9  # Избыточное давление на стояке, атм (✔️)
mud_density = 1.11  # Плотность раствора, г/см^3 (✔️)


def equilibrium_density():
    """Плотность равновесия, г/см^3"""
    equilibrium_density_variable = mud_density + (excess_pressure_on_riser / vertical_depth / 0.1)
    return equilibrium_density_variable


#  Параметры смешивания жидкостей (возможно, для расчета конечной плотности)
volume_1 = 30  # Объем первой жидкости (✔️)
density_1 = 1.08  # Плотность первой жидкости (✔️)
volume_2 = 10  # Объем второй жидкости (✔️)
density_2 = 1  # Плотность второй жидкости (✔️)


def final_density_mixture():
    """Конечная плотность смеси"""
    final_density_mixture_variable = ((volume_1 * density_1) + (volume_2 * density_2)) / (volume_1 + volume_2)
    return final_density_mixture_variable


#  Еще один набор параметров смешивания жидкостей
volume_1_mix2 = 30  # Объем первой жидкости (смесь 2) (✔️)
density_1_mix2 = 1.11  # Плотность первой жидкости (смесь 2) (✔️)
volume_2_mix2 = 4  # Объем второй жидкости (смесь 2) (✔️)
density_2_mix2 = 1.01  # Плотность второй жидкости (смесь 2) (✔️)


def final_density_mixture2():
    """Конечная плотность смеси 2"""

    final_density_mixture2_variable = (((volume_1_mix2 * density_1_mix2) + (volume_2_mix2 * density_2_mix2)) /
                                       (volume_1_mix2 + volume_2_mix2))
    return final_density_mixture2_variable


# Параметры для расчета разбавления бурового раствора
initial_mud_density = 1170  # Начальная плотность раствора, кг/м^3
final_mud_density = 1165  # Конечная плотность раствора, кг/м^3

initial_mud_volume = 40  # Начальный объем раствора в циркуляции, м^3
added_water_volume = 18  # Добавлено воды (прирост объема), м^3
water_density = 1065  # Плотность воды (свежего раствора), кг/м^3

wellbore_diameter = 124  # Диаметр скважины, мм
cavernosity_coefficient = 10  # Коэффициент кавернозности (в долях единицы)
drilled_interval = 176  # Проходка, м


def efficiency_of_cleaning_equipment():
    """Эффективность оборудования очистки"""
    efficiency_of_cleaning_equipment_variable = (1 - (initial_mud_volume * (final_mud_density - initial_mud_density) +
                                                      added_water_volume * (final_mud_density - water_density)) /
                                                 (2500 - final_mud_density) / (3.1416 * (wellbore_diameter / 1000) ** 2
                                                                               * (100 + cavernosity_coefficient) *
                                                                               drilled_interval / 400))
    return efficiency_of_cleaning_equipment_variable * 100  # В процентах


if __name__ == '__main__':
    tool_volume_variable = tool_volume()
    logger.info(f"Объем инструмента, м^3: {tool_volume_variable}")
    tool_internal_variable = tool_internal_volume()
    logger.info(f"Объем в инструменте, м^3: {tool_internal_variable}")
    annulus_fluid_volume_variable = annulus_fluid_volume()
    logger.info(f"Объем в затрубье, м^3: {annulus_fluid_volume_variable}")
    total_circulation_volume_variable = total_circulation_volume()
    logger.info(f"Общий объем циркуляции, м^3: {total_circulation_volume_variable}")
    pump_flow_rate_cubic_meter_variable = pump_flow_rate_cubic_meter()
    logger.info(f"Производит насос м3/мин: {pump_flow_rate_cubic_meter_variable}")
    wellbore_circulation_time_variable = wellbore_circulation_time()
    logger.info(f"Время циркуляции скв, мин: {wellbore_circulation_time_variable}")
    total_circulation_time_variable = total_circulation_time()
    logger.info(f"Время циркуляции общая: {total_circulation_time_variable}")
    annulus_circulation_time_variable = annulus_circulation_time()
    logger.info(f"Время циркуляции затрубья, мин: {annulus_circulation_time_variable}")
    tool_circulation_time_variable = tool_circulation_time()
    logger.info(f"Время циркуляции инструмента, мин: {tool_circulation_time_variable}")
    casing_circulation_time_variable = casing_circulation_time()
    logger.info(f"Время циркуляции колонны: {casing_circulation_time_variable}")
    pump_flow_rate_liter_per_second_variable = pump_flow_rate_liter_per_second()
    logger.info(f"Производит насос л/с: {pump_flow_rate_liter_per_second_variable}")
    final_density_mixture2_variable = final_density_mixture2()
    logger.info(f"Конечная плотность: {final_density_mixture2_variable}")
    final_density_mixture_variable = final_density_mixture()
    logger.info(f"Конечная плотность: {final_density_mixture_variable}")
    equilibrium_density_variable = equilibrium_density()
    logger.info(f"Плотность равновесия, г/см3: {equilibrium_density_variable}")
    final_density_calculated_variable = final_density_calculated()
    logger.info(f"Конечная плотность: {final_density_calculated_variable}")
    weighting_material_mass_calculated = weighting_material_mass_calculated()
    logger.info(f"Масса утяжелителя, кг: {weighting_material_mass_calculated}")
    weighting_material_volume = weighting_material_volume()
    logger.info(f"Объем утяжелителя, м^3: {weighting_material_volume}")
    final_solution_volume = final_solution_volume()
    logger.info(f"Конечный объем раствора, м^3: {final_solution_volume}")
    number_of_weighting_material_bags = number_of_weighting_material_bags()
    logger.info(f"Количество мешков утяжелителя: {number_of_weighting_material_bags}")
    chalk_concentration = chalk_concentration()
    logger.info(f"Концентрация мела, кг/м^3: {chalk_concentration}")
    efficiency_of_cleaning_equipment_variable = efficiency_of_cleaning_equipment()
    logger.info(f"Эффективность оборудования очистки: {efficiency_of_cleaning_equipment_variable}")
