from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp

button = lambda instance, x: setattr(mainbutton, 'text', x)
btny = lambda btn: dropdown.select(btn.text)

lista = ["Oi1", "Oi2", "Oi3", "Oi4", "Oi5", "Oi6", "Oi7", "Oi8", "Oi9", "Oi10"]
dropdown = DropDown()
for c in range(10):
    btn = Button(text=f' {lista[c]}', size_hint_y=None, height=44)
    btn.bind(on_release=btny)
    dropdown.add_widget(btn)
mainbutton = Button(text='Hello', size_hint=(None, None))
mainbutton.bind(on_release=dropdown.open)
dropdown.bind(on_select=button)

runTouchApp(mainbutton)


def button (instance, x):
    return setattr(mainbutton, 'text', x)
