

import os

from nicegui import ui
from calculator import project_growth


@ui.page('/')
def home():
    ui.label('Portfolio Growth Calculator').classes('text-h4')

    with ui.row().classes('items-center gap-4'):
        amount = ui.number('Starting Portfolio ($)', value=500000)
        rate = ui.number('Annual Return (%)', value=6)
        years = ui.number('Number of Years', value=20)

    result = ui.label().classes('text-h6')

    chart = ui.echart({
        'title': {'text': 'Portfolio Growth'},
        'tooltip': {
            'trigger': 'axis',
            'valueFormatter': None,
        },
        'xAxis': {
            'type': 'category',
            'name': 'Year',
            'data': [],
        },
        'yAxis': {
            'type': 'value',
            'name': 'Portfolio Value ($)',
        },
        'series': [{
            'name': 'Portfolio Value',
            'type': 'line',
            'smooth': True,
            'data': [],
        }],
    }).classes('w-full h-96')

    def calculate():
        principal = amount.value or 0
        annual_rate = (rate.value or 0) / 100
        duration = int(years.value or 0)

        balances = project_growth(principal, annual_rate, duration)

        result.set_text(
            f'Future Portfolio Value: ${balances[-1]:,.2f}'
        )

        chart.options['xAxis']['data'] = list(range(duration + 1))
        chart.options['series'][0]['data'] = [
            round(balance, 2) for balance in balances
        ]
        chart.update()

    ui.button('Calculate', on_click=calculate)

    calculate()


ui.run(
    host='0.0.0.0',
    port=int(os.environ.get('PORT', 8080)),
)
