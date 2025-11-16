# main.py
import json
import os
from datetime import datetime
from functools import partial

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import DictProperty, ListProperty, StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

# Ajustes de ventana (vertical 1080x1920 recomendado). Cambia si tu pantalla tiene otra resolución.
Window.clearcolor = (0.02, 0.02, 0.02, 1)
# Descomenta si quieres forzar resolución (útil en desarrollo)
# Window.size = (1080, 1920)

KV = r'''
#:import rgba kivy.utils.get_color_from_hex

<SideButton@Button>:
    size_hint: None, None
    size: dp(80), dp(160)
    background_normal: ''
    background_color: rgba('#00121f') if root_direction == 'left' else rgba('#00121f')
    color: rgba('#00FFFF')
    bold: True
    font_size: '20sp'
    opacity: .85

<HeaderLabel@Label>:
    font_size: '28sp'
    color: rgba('#39FF14')
    bold: True
    size_hint_y: None
    height: self.texture_size[1] + dp(10)

<StatCard@BoxLayout>:
    orientation: 'vertical'
    size_hint: None, None
    size: dp(420), dp(180)
    padding: dp(12)
    spacing: dp(8)
    canvas.before:
        Color:
            rgba: rgba('#001f2f')
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [12,]
    Label:
        id=label_name
        text: root.label
        size_hint_y: None
        height: self.texture_size[1]
        color: rgba('#9efcff')
        font_size: '18sp'
    Label:
        id=value
        text: root.value
        font_size: '38sp'
        color: rgba('#00ffff')
        bold: True

ScreenManager:
    id: sm
    transition: FadeTransition(duration=0.45)

    WelcomeScreen:
        name: 'welcome'
    UserScreen:
        name: 'user'
    VitalsScreen:
        name: 'vitals'
    RestartScreen:
        name: 'restart'

<WelcomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(16)
        spacing: dp(8)

        FloatLayout:
            size_hint_y: None
            height: dp(420)
            Image:
                id: gif_anim
                source: root.current_gif
                allow_stretch: True
                keep_ratio: False
                size_hint: 1, 1
                pos_hint: {"center_x": .5, "center_y": .5}
                anim_delay: 0.05

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(220)
            padding: dp(12)
            canvas.before:
                Color:
                    rgba: rgba('#021018')
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [10,]
            Label:
                text: "Bienvenido al Sistema TARS"
                font_size: '36sp'
                color: rgba('#7CFC00')
                bold: True
                size_hint_y: None
                height: self.texture_size[1] + dp(10)

            BoxLayout:
                orientation: 'vertical'
                Label:
                    id: noticias
                    text: root.news_text
                    font_size: '18sp'
                    color: rgba('#bffcff')
                    valign: 'top'
                    text_size: self.width, None
                    size_hint_y: None
                    height: dp(120)

    # Botones laterales
    SideButton:
        root_direction: 'left'
        pos: root.width * 0.01, root.height * 0.4
        text: '<'
        on_release: app.go_prev()
    SideButton:
        root_direction: 'right'
        pos: root.width - self.width - root.width * 0.01, root.height * 0.4
        text: '>'
        on_release: app.go_next()

<UserScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(8)

        BoxLayout:
            size_hint_y: None
            height: dp(420)
            padding: dp(12)
            canvas.before:
                Color:
                    rgba: rgba('#061726')
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [10,]
            Image:
                id: userphoto
                source: root.user_photo
                allow_stretch: True
                keep_ratio: True

        Label:
            text: root.user_name
            font_size: '34sp'
            color: rgba('#39FF14')
            size_hint_y: None
            height: self.texture_size[1] + dp(10)
            halign: 'center'

    SideButton:
        root_direction: 'left'
        pos: root.width * 0.01, root.height * 0.4
        text: '<'
        on_release: app.go_prev()
    SideButton:
        root_direction: 'right'
        pos: root.width - self.width - root.width * 0.01, root.height * 0.4
        text: '>'
        on_release: app.go_next()

<VitalsScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(12)
        spacing: dp(8)

        Label:
            text: 'Panel Vitales'
            font_size: '30sp'
            color: rgba('#7CFC00')
            size_hint_y: None
            height: self.texture_size[1] + dp(8)

        GridLayout:
            id: cards
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            padding: dp(12)
            spacing: dp(12)

    SideButton:
        root_direction: 'left'
        pos: root.width * 0.01, root.height * 0.4
        text: '<'
        on_release: app.go_prev()
    SideButton:
        root_direction: 'right'
        pos: root.width - self.width - root.width * 0.01, root.height * 0.4
        text: '>'
        on_release: app.go_next()

<RestartScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(12)
        Label:
            text: 'Registro completado'
            font_size: '32sp'
            color: rgba('#39FF14')
        Button:
            text: 'Registrar nuevo usuario'
            size_hint_y: None
            height: dp(120)
            background_color: rgba('#002b3a')
            color: rgba('#00ffee')
            font_size: '28sp'
            on_release:
                app.reset_user()
    SideButton:
        root_direction: 'left'
        pos: root.width * 0.01, root.height * 0.4
        text: '<'
        on_release: app.go_prev()
    SideButton:
        root_direction: 'right'
        pos: root.width - self.width - root.width * 0.01, root.height * 0.4
        text: '>'
        on_release: app.go_next()
'''

# Screens
class WelcomeScreen(Screen):
    gifs = ListProperty([])
    current_gif = StringProperty('')
    news_text = StringProperty('Cargando noticias...')

    def on_enter(self):
        # start gif rotation and news load
        if not self.gifs:
            self.gifs = self.load_gifs()
        self.current_index = 0
        if self.gifs:
            self.current_gif = self.gifs[0]
            Clock.schedule_interval(self.switch_gif, 8)
        self.load_news()

    def load_gifs(self):
        assets = App.get_running_app().assets_folder
        folder = os.path.join(assets, 'gifs')
        if not os.path.exists(folder):
            return []
        files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('.gif','.mp4','.webm'))]
        return files

    def switch_gif(self, dt):
        if not self.gifs:
            return
        self.current_index = (self.current_index + 1) % len(self.gifs)
        self.current_gif = self.gifs[self.current_index]

    def load_news(self):
        try:
            assets = App.get_running_app().assets_folder
            with open(os.path.join(assets, 'noticias.json'), 'r', encoding='utf-8') as fh:
                news = json.load(fh)
            lines = []
            for n in news.get('items', [])[:5]:
                lines.append("[b]{}[/b]\n{}".format(n.get('title',''), n.get('summary','')))
            self.news_text = '\n\n'.join(lines) or 'No hay noticias'
        except Exception as e:
            self.news_text = 'Error cargando noticias'

class UserScreen(Screen):
    user_name = StringProperty('Usuario')
    user_photo = StringProperty('')

    def on_enter(self):
        try:
            assets = App.get_running_app().assets_folder
            p = os.path.join(assets, 'usuario.json')
            if os.path.exists(p):
                u = json.load(open(p, 'r', encoding='utf-8'))
                self.user_name = u.get('nombre', 'Usuario')
                photo = u.get('foto', 'usuario.jpg')
                imgpath = os.path.join(assets, photo)
                if os.path.exists(imgpath):
                    self.user_photo = imgpath
                else:
                    self.user_photo = ''
        except Exception as e:
            self.user_name = 'Usuario'

class VitalsScreen(Screen):
    vitals = DictProperty({})

    def on_enter(self):
        self.load_vitals()

    def load_vitals(self):
        self.vitals = {}
        assets = App.get_running_app().assets_folder
        p = os.path.join(assets, 'datos_usuario.json')
        try:
            if os.path.exists(p):
                d = json.load(open(p, 'r', encoding='utf-8'))
                self.vitals = d.get('vitales', {})
            else:
                # default demo values
                self.vitals = {
                    'temperatura': 36.7,
                    'presion': '120/80',
                    'glucosa': 95,
                    'pulso': 72,
                    'oxigeno': 98,
                    'lactato': 1.1,
                    'cetonas': 0.3,
                    'colesterol': 180
                }
        except Exception as e:
            print("Error cargando vitals:", e)
            self.vitals = {}
        # populate cards
        grid = self.ids.cards
        grid.clear_widgets()
        # order for presentation
        order = [
            ('Temperatura', 'temperatura', '°C'),
            ('Presión arterial', 'presion', ''),
            ('Glucosa', 'glucosa', 'mg/dL'),
            ('Pulso', 'pulso', 'BPM'),
            ('Oxigenación', 'oxigeno', '%'),
            ('Lactato', 'lactato', 'mmol/L'),
            ('Cetonas', 'cetonas', 'mmol/L'),
            ('Colesterol', 'colesterol', 'mg/dL')
        ]
        for label, key, unit in order:
            value = self.vitals.get(key, '--')
            from kivy.uix.boxlayout import BoxLayout
            from kivy.uix.label import Label
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height='60dp', padding=10)
            # left label
            l = Label(text=label, size_hint_x=0.6, halign='left', valign='middle', markup=True)
            l.text_size = (self.width * 0.6 - 20, None)
            l.color = (0.8,1,1,1)
            l.font_size = '18sp'
            # right value
            v = Label(text=f"[b]{value} {unit}[/b]", size_hint_x=0.4, halign='right', valign='middle', markup=True)
            v.color = (0.0,1,0.9,1)
            v.font_size = '22sp'
            box.add_widget(l)
            box.add_widget(v)
            grid.add_widget(box)

class RestartScreen(Screen):
    pass

class TARSApp(App):
    assets_folder = StringProperty('assets')

    def build(self):
        # ensure assets folder exists
        if not os.path.exists(self.assets_folder):
            os.makedirs(self.assets_folder)
        Builder.load_string(KV)
        self.sm = self.root
        # set screen order
        self.screen_list = ['welcome','user','vitals','restart']
        # enable touch-friendly behavior
        Window.fullscreen = True
        return self.sm

    def on_start(self):
        # schedule initial show
        Clock.schedule_once(lambda dt: self.go_to('welcome'), 0.1)

    def go_to(self, name):
        if name in self.screen_list:
            self.sm.current = name

    def go_next(self):
        idx = self.screen_list.index(self.sm.current)
        idx = (idx + 1) % len(self.screen_list)
        self.go_to(self.screen_list[idx])

    def go_prev(self):
        idx = self.screen_list.index(self.sm.current)
        idx = (idx - 1) % len(self.screen_list)
        self.go_to(self.screen_list[idx])

    def reset_user(self):
        # reset demo user data (clears JSON)
        assets = self.assets_folder
        p = os.path.join(assets, 'datos_usuario.json')
        if os.path.exists(p):
            try:
                os.remove(p)
            except:
                pass
        # return to welcome
        self.go_to('welcome')

if __name__ == '__main__':
    TARSApp().run()
