
import json
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
        'tooltip': {'trigger': 'axis'},
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

        balances = project_growth(
            principal, annual_rate, duration
        )

        result.set_text(
            f'Future Portfolio Value: ${balances[-1]:,.2f}'
        )

        chart.options['xAxis']['data'] = list(range(duration + 1))
        chart.options['series'][0]['data'] = [
            round(balance, 2) for balance in balances
        ]
        chart.update()

    def save_scenario():
        scenario = {
            'portfolio': amount.value,
            'annual_return': rate.value,
            'years': years.value,
        }

        json_data = json.dumps(scenario, indent=4)

        ui.download.content(
            json_data.encode('utf-8'),
            filename='portfolio_scenario.json',
            media_type='application/json',
        )

    async def load_scenario(event):
        try:
            # Support both recent and older NiceGUI upload APIs.
            if hasattr(event, 'file'):
                contents = await event.file.read()
            else:
                contents = event.content.read()

            scenario = json.loads(contents)

            portfolio = float(scenario['portfolio'])
            annual_return = float(scenario['annual_return'])
            duration = int(scenario['years'])

            if not (
                0 <= portfolio <= 1_000_000_000_000
                and -100 <= annual_return <= 100
                and 0 <= duration <= 100
            ):
                raise ValueError('Values outside supported ranges')

            amount.value = portfolio
            rate.value = annual_return
            years.value = duration

            calculate()
            ui.notify('Scenario loaded successfully', type='positive')

        except (ValueError, TypeError, KeyError, OverflowError):
            ui.notify('Invalid scenario file', type='negative')
        except (UnicodeDecodeError, json.JSONDecodeError):
            ui.notify('Invalid JSON file', type='negative')

    with ui.row().classes('items-center gap-4'):
        ui.button('Calculate', on_click=calculate)

        ui.button(
            'Save Scenario',
            on_click=save_scenario,
            icon='download',
        )

    ui.upload(
        label='Load Scenario (JSON)',
        on_upload=load_scenario,
        auto_upload=True,
        max_file_size=100_000,
    ).props('accept=.json').classes('w-64')

    calculate()


ui.run(
    host='0.0.0.0',
    port=int(os.environ.get('PORT', 8080)),
)
