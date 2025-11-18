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
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import rgba kivy.utils.get_color_from_hex
#:import dp kivy.metrics.dp

<SideButton@Button>:
    size_hint: None, None
    size: dp(80), dp(160)
    background_normal: ''
    background_color: rgba('#00121f')   # color estático
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
    # propiedades que usará la plantilla
    label: ""
    value: ""
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

    # Contenido de la tarjeta (fuera de canvas.before)
        Label:
            text: root.label
            size_hint_y: None
            height: self.texture_size[1]
            color: rgba('#9efcff')
            font_size: '18sp'

        Label:
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
            text: 'PANEL DE VITALES'
            font_size: '30sp'
            color: rgba('#7CFC00')
            size_hint_y: None
            height: self.texture_size[1] + dp(8)

        ScrollView:
            size_hint_y: 1
            do_scroll_x: False
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
    update_interval = 3.0  # segundos, puedes cambiarlo

    # rangos y umbrales para coloración (valores normales/precaución/peligro)
    thresholds = {
        'temperatura': (35.0, 37.5, 39.0),  # (minNormal, maxNormal, danger)
        'glucosa': (70, 140, 250),
        'pulso': (50, 100, 140),
        'oxigeno': (92, 97, 100),  # oxígeno normal >92
        'lactato': (0.5, 2.0, 4.0),
        'cetonas': (0.0, 0.6, 1.5),
        'colesterol': (125, 200, 240),
        'presion_systolic': (90, 120, 160)  # para estimar presión
    }

    def on_enter(self):
        # cargar inmediatamente y luego programar refresco periódico
        self.load_vitals()
        # cancelar previas en caso de múltiples entradas
        Clock.unschedule(self._scheduled_reload) if hasattr(self,'_scheduled_reload') else None
        self._scheduled_reload = Clock.schedule_interval(lambda dt: self.load_vitals(), self.update_interval)

    def on_leave(self):
        # cancelar refresco cuando salgamos de la pantalla
        if hasattr(self, '_scheduled_reload'):
            Clock.unschedule(self._scheduled_reload)

    def get_percent(self, key, value):
        # mapear valor numérico a porcentaje (0-100) según rango lógico
        try:
            if key == 'temperatura':
                # map 34-42
                v = float(value)
                percent = int((v - 34.0) / (42.0 - 34.0) * 100)
            elif key == 'glucosa':
                v = float(value); percent = int((v - 40) / (400 - 40) * 100)
            elif key == 'pulso':
                v = float(value); percent = int((v - 30) / (200 - 30) * 100)
            elif key == 'oxigeno':
                v = float(value); percent = int((v - 50) / (100 - 50) * 100)
            elif key == 'lactato':
                v = float(value); percent = int((v) / 15.0 * 100)
            elif key == 'cetonas':
                v = float(value); percent = int((v) / 10.0 * 100)
            elif key == 'colesterol':
                v = float(value); percent = int((v - 100) / (400 - 100) * 100)
            elif key == 'presion':
                # expect "SYS/DIA", compute based on SYS
                parts = str(value).split('/')
                sys = float(parts[0]) if parts and parts[0].isdigit() else 120.0
                percent = int((sys - 60) / (200 - 60) * 100)
            else:
                percent = 0
        except Exception:
            percent = 0
        # clamp
        if percent < 0: percent = 0
        if percent > 100: percent = 100
        return percent

    def get_color_for(self, key, value):
        # devuelve color rgba (r,g,b,a) según umbrales
        try:
            t = self.thresholds
            if key == 'presion':
                parts = str(value).split('/')
                val = float(parts[0]) if parts and parts[0].isdigit() else 120.0
                minN, maxN, danger = t['presion_systolic']
            else:
                minN, maxN, danger = t.get(key, (0, 1, 2))
                val = float(value)
        except Exception:
            return (0.0, 1.0, 0.9, 1)

        # color logic: green (normal), yellow (caution), red (danger)
        if val <= maxN:
            return (0.0, 1.0, 0.9, 1)  # holographic green
        elif val <= danger:
            return (1.0, 0.8, 0.0, 1)  # amber
        else:
            return (1.0, 0.2, 0.2, 1)  # red

    def load_vitals(self):
        # lee JSON y actualiza la UI
        assets = App.get_running_app().assets_folder
        p = os.path.join(assets, 'datos_usuario.json')
        try:
            if os.path.exists(p):
                with open(p, 'r', encoding='utf-8') as fh:
                    d = json.load(fh)
                    self.vitals = d.get('vitales', {})
            else:
                # valores predeterminados de demostración
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

        # actualizar tarjetas
        self.populate_cards()

    def populate_cards(self):
        grid = self.ids.cards
        grid.clear_widgets()

        order = [
            ('Temperatura', 'temperatura', '°C'),
            ('Presión arterial (SYS/DIA)', 'presion', ''),
            ('Glucosa', 'glucosa', 'mg/dL'),
            ('Pulso', 'pulso', 'BPM'),
            ('Oxigenación', 'oxigeno', '%'),
            ('Lactato', 'lactato', 'mmol/L'),
            ('Cetonas', 'cetonas', 'mmol/L'),
            ('Colesterol', 'colesterol', 'mg/dL')
        ]

        for label, key, unit in order:
            value = self.vitals.get(key, '--')
            percent = self.get_percent(key, value if value != '--' else 0)
            color = self.get_color_for(key, value if value != '--' else 0)

            # create layout for the metric
            from kivy.uix.boxlayout import BoxLayout
            from kivy.uix.label import Label
            from kivy.uix.progressbar import ProgressBar
            from kivy.uix.widget import Widget
            box = BoxLayout(orientation='vertical', size_hint_y=None, height='110dp', padding=(10,8))
            # top row: label and numeric value
            top = BoxLayout(orientation='horizontal', size_hint_y=None, height='30dp')
            l = Label(text=label, halign='left', valign='middle', size_hint_x=0.65, markup=True)
            l.color = (0.7, 1, 0.95, 1)
            l.font_size = '18sp'
            v = Label(text=f"[b]{value} {unit}[/b]", halign='right', valign='middle', size_hint_x=0.35, markup=True)
            v.color = color
            v.font_size = '22sp'
            top.add_widget(l)
            top.add_widget(v)
            # progress bar row
            pb_row = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp', padding=(0,6))
            pb_bg = Widget(size_hint_x=1)
            # progress visual: use Kivy ProgressBar
            pb = ProgressBar(max=100, value=percent)
            pb.size_hint_x = 0.98
            # overlay label percent
            pct = Label(text=f"{percent}%", size_hint_x=0.18, halign='right', valign='middle', markup=True)
            pct.color = (0.8, 1, 0.9, 1)
            pct.font_size = '16sp'
            pb_row.add_widget(pb)
            pb_row.add_widget(pct)
            box.add_widget(top)
            box.add_widget(pb_row)
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
