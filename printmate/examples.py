from base import *

if __name__ == '__main__':
    pla = PLA()
    abs = ABS()
    ender5 = Ender5Plus()
    ender3 = Ender3Pro()

    messeturm = MultiPart(
        name="Messeturm",
        parts=[
            Part(
                name="tower_main",
                filament_type=pla,
                hours=2 * 24 + 5,
                grams=350,
                printer=ender3,
            ),
            Part(
                name='socket_pos',
                filament_type=abs,
                hours=21,
                grams=350,
                printer=ender3,
            ),
            Part(
                name='socket_neg',
                filament_type=abs,
                hours=20,
                grams=350,
                printer=ender3,
            ),
            Part(
                name='spire',
                filament_type=pla,
                hours=6,
                grams=80,
                printer=ender3,
            ),
            NonPrintedPart(
                name='LED',
                cost=5,
            ),
            NonPrintedPart(
                name='GU10 Lamp Socket',
                cost=6,
            ),
        ],
        attributes={'scale': '1:750', 'type': 'desk_light'}
    )
    stonks = MultiPart(
        name='Stonks',
        parts=[
            Part(
                name='frame',
                filament_type=abs,
                hours=21,
                printer=ender5,
                grams=311,
            ),
            Part(
                name='background',
                filament_type=pla,
                hours=5,
                printer=ender3,
                grams=20,
                attributes={'color': 'blue'},
            ),
            Part(
                name='arrow',
                filament_type=pla,
                hours=3,
                printer=ender3,
                grams=20,
                attributes={'color': 'red'},
            ),
            Part(
                name='stonks_guy',
                filament_type=pla,
                hours=9,
                printer=ender3,
                grams=40,
                attributes={'color': 'black'},
            ),
            Part(
                name='text_plate',
                filament_type=pla,
                hours=6,
                printer=ender3,
                grams=30,
                attributes={'color': 'white'},
            ),
            NonPrintedPart(
                name='LED',
                cost=5,
            ),
            NonPrintedPart(
                name='GU10 Lamp Socket',
                cost=6,
            ),
        ],
        attributes={'type': 'desk_light'}
    )

    print(f'Messeturm Total Cost: {messeturm.calculate_cost()}')
    print(f'Stonks Total Cost: {stonks.calculate_cost()}')

    CostVisualization(parts=[messeturm, stonks])
