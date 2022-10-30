from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior

class ImageButton(ButtonBehavior, Image):  # O button behavior basicamente transforma o outro item em um botão, mas deve ser passado na primeira posição
    pass

class LabelButton(ButtonBehavior, Label):
    pass