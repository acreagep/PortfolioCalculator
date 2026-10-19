
from nicegui import ui
from calculator import future_value

@ui.page('/')
def home():
    ui.label('Portfolio Growth Calculator').classes('text-h4')

    amount = ui.number('Starting Portfolio ($)', value=500000)
    rate = ui.number('Annual Return (%)', value=6)
    years = ui.number('Number of Years', value=20)

    result = ui.label('Click Calculate to see the result.')

    def calculate():
        value = future_value(amount.value, rate.value / 100, years.value)
        result.set_text(f'Future Portfolio Value: ${value:,.2f}')

    ui.button('Calculate', on_click=calculate)

ui.run()

