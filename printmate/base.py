import matplotlib.pyplot as plt
from typing import List, Union


class Part:
    def __init__(self, name, filament_type, hours, grams, printer, attributes=None):
        self.name = name
        self.filament_type = filament_type
        self.hours = hours
        self.grams = grams
        self.attributes = attributes or {}
        self.printer = printer

    def calculate_cost(self):
        return self.printer.price_per_hour * self.hours + self.filament_type.price_per_gram * self.grams

    def get_filament_cost(self):
        return self.filament_type.price_per_gram * self.grams

    def get_other_costs(self):
        return 0

    def get_printer_cost(self):
        return self.printer.price_per_hour * self.hours

    def get_power_cost(self):
        return self.printer.power_consumption * self.printer.price_per_watt * self.hours


class NonPrintedPart(Part):
    def __init__(self, name, cost, attributes=None):
        self.name = name
        self.cost = cost
        self.attributes = attributes or {}

    def calculate_cost(self):
        return self.cost

    def get_other_costs(self):
        return self.cost

    def get_filament_cost(self):
        return 0

    def get_printer_cost(self):
        return 0

    def get_power_cost(self):
        return 0


class MultiPart(Part):
    def __init__(self, name: str, parts: List[Part], attributes=None):
        self.name = name
        self.parts = parts
        self.attributes = attributes or {}

    def calculate_cost(self):
        return sum(x.calculate_cost() for x in self.parts)

    def get_other_costs(self):
        return sum(x.get_other_costs() for x in self.parts)

    def get_filament_cost(self):
        return sum(x.get_filament_cost() for x in self.parts)

    def get_printer_cost(self):
        return sum(x.get_printer_cost() for x in self.parts)

    def get_power_cost(self):
        return sum(x.get_power_cost() for x in self.parts)


class Filament:
    def __init__(self, price_per_gram):
        self.price_per_gram = price_per_gram


class ABS(Filament):
    def __init__(self, price_per_gram=9 / 1000):
        super(ABS, self).__init__(price_per_gram)


class PLA(Filament):
    def __init__(self, price_per_gram=20 / 1000):
        super(PLA, self).__init__(price_per_gram)


class Printer:
    def __init__(self, initial_cost, power_consumption, price_per_watt=0.28 / 1000, repay_period_hours=3 * 30 * 24,
                 price_per_hour=None):
        self.initial_cost = initial_cost
        self.repay_period = repay_period_hours
        self.power_consumption = power_consumption
        self.price_per_watt = price_per_watt
        self.price_per_hour = price_per_hour or (initial_cost / repay_period_hours + price_per_watt * power_consumption)


class Ender3Pro(Printer):
    def __init__(self):
        super(Ender3Pro, self).__init__(initial_cost=220, power_consumption=20)


class Ender5Plus(Printer):
    def __init__(self):
        super(Ender5Plus, self).__init__(initial_cost=500, power_consumption=125)


class CostFeature:
    def __init__(self, p: Union[MultiPart, Part, NonPrintedPart]):
        self.cost = p.calculate_cost()


class Material(CostFeature):
    name = 'Material Costs'

    def __init__(self, p):
        self.p = p
        self.cost = p.get_filament_cost()


class PrintingTime(CostFeature):
    name = 'Printing Time Costs'

    def __init__(self, p):
        self.p = p
        self.cost = p.get_printer_cost()


class Power(CostFeature):
    name = 'Power Costs'

    def __init__(self, p):
        self.p = p
        self.cost = p.get_power_cost()


class Other(CostFeature):
    name = 'Other Costs'

    def __init__(self, p):
        self.p = p
        self.cost = p.get_other_costs()


class CostVisualization:
    def __init__(self, parts: List[Union[Part, MultiPart]], features=(
            Other,
            Material,
            PrintingTime,
            Power,
    )):
        fig, ax = plt.subplots()

        feature_values = []

        for f in features:
            ps = []
            for p in parts:
                ps.append(f(p))
            feature_values.append(ps)

        labels = [x.p.name + f' ({str(round(x.p.calculate_cost(), 2))}€)' for x in feature_values[0]]
        print(labels)
        partial_costs = [[ftr[item_idx].cost for ftr in feature_values] for item_idx in range(len(feature_values[0]))]
        print(partial_costs)
        partial_sums = [[sum(ftr[item_idx].cost for ftr in feature_values[:y]) for y in range(len(feature_values))] for
                        item_idx in range(len(feature_values[0]))]
        print(partial_sums)
        print(features)

        for ftr_idx, ftr in enumerate(features):
            ax.bar(labels, [x[ftr_idx] for x in partial_costs], bottom=[x[ftr_idx] for x in partial_sums],
                   label=ftr.name)

        for item_id in range(len(partial_costs[0])):
            for idx, (sub_sum, sub_cost) in enumerate(zip(partial_sums, partial_costs)):
                ax.text(idx - 0.35, sub_sum[item_id] + 0.3, str(round(sub_cost[item_id], 2)) + '€', color='black',
                        fontweight='bold',
                        fontsize=12, fontfamily='Oxygen-Sans')

        plt.legend()
        plt.show()
