from nicegui import ui

ui.label('Model')
ModelOptions = ui.select({'tiny': 'Tiny', 'base': 'Base', 'small': 'Small'})


ui.run()
