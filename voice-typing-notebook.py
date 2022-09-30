'''
    Written in 2022 by Theodore Jones tjones2@fastmail.com

    To the extent possible under law, the author(s) have dedicated all copyright and related and neighboring rights to this software to the public domain worldwide. This software is distributed without any warranty.

    You should have received a copy of the CC0 Public Domain Dedication along with this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>. 
'''

from nicegui import ui

with ui.row():
    ui.markdown('''This is **Markdown**.''')
    ui.input(label='Text', placeholder='press ENTER to apply',
         on_change=lambda e: input_result.set_text('you typed: ' + e.value))



ui.run()
