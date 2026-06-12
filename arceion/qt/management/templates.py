"""
Template strings for project scaffolding
"""

__all__ = [
    "MAIN_PY",
    "APP_PY",
    "ENV_PY",
    "PYPROJECT_TOML",
    "THEME_ENUM",
    "LOCALE_ENUM",
    "APP_THEME",
    "HOME_VIEW",
    "LOCALE_EN_US",
    "LOCALE_SI_LK",
    "ENUMS_INIT",
    "VIEWS_INIT",
    "RES_INIT",
    "COMPONENTS_INIT",
    "MODELS_INIT",
    "REQUESTS_INIT",
    "RESPONSES_INIT",
    "SERVICES_INIT"
]

MAIN_PY = """import faulthandler
import logging
import os
import sys

from env import env
from PyQt6.QtCore import QCoreApplication, Qt
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import QApplication

env.init()

QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
logging.getLogger('urllib3').setLevel(logging.DEBUG)
faulthandler.enable()

if getattr(sys, 'frozen', False):
\tROOTPATH = os.path.dirname(sys.executable)
else:
\tROOTPATH = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOTPATH)
os.environ.setdefault('BASE_PATH', ROOTPATH)
os.environ.setdefault('APP_NAME', '{project_name}')


if __name__ == '__main__':
\tapp = QApplication(sys.argv)

\tfrom arceion.qt.res import Icons
\tapp.setWindowIcon(Icons.settings_applications)

\t# from arceion.qt.util.UI import UI
\t# QFontDatabase.addApplicationFont('res/fonts/YourFont.ttf')
\t# app.setFont(QFont('YourFont', UI.sp(9)))  # default font size : 9

\tfrom {app_class} import {app_class}
\t{app_class}()
\tsys.exit(app.exec())
"""

APP_PY = """from enums import Theme
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPalette
from res import AppTheme

from arceion.qt.core import Window
from arceion.qt.util import UI

__all__ = ['{app_class}']


class {app_class}(Window):
\tdef __init__(self):
\t\tsuper({app_class}, self).__init__(row=4, column=2)

\t\tself.setObjectName('MainWindow')
\t\tself.setWindowTitle('{project_name}')
\t\tAppTheme.setColorTheme(Theme.LIGHT if AppTheme.getSystemTheme() else Theme.DARK)
\t\tself.setWindowIcon(QIcon(UI.pixmap(
\t\t\tAppTheme.images.logoWhiteBg, 32, 32, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
\t\t\tQt.TransformationMode.SmoothTransformation
\t\t)))
\t\tself.setMinimumSize(UI.size(800, 600))
\t\tself.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
\t\tself.setFocus()

\t\tfrom views import HomeView
\t\tself.navigate(HomeView)

\t\tself.show()

\tdef f11(self):
\t\tif self.isFullScreen():
\t\t\tself.showNormal()
\t\telse:
\t\t\tself.showFullScreen()

\tdef updateTheme(self):
\t\tpal = self.palette()
\t\tpal.setColor(QPalette.ColorRole.Window, AppTheme.colors.background)
\t\tpal.setColor(QPalette.ColorRole.WindowText, AppTheme.colors.text)
\t\tself.setPalette(pal)
\t\tsuper(Demo, self).updateTheme()
"""

ENV_PY = """from arceion.qt.env import Env, EnvManager, EnvMode

__all__ = ['env']

env = EnvManager([
\tEnv(
\t\tEnvMode.DEBUG,
\t\tverbose=True
\t),
\tEnv(
\t\tEnvMode.RELEASE,
\t\tverbose=False
\t)
], default=EnvMode.DEBUG)
"""

PYPROJECT_TOML = """[project]
name = "{project_name}"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
\t"arceion-qt",
]
"""

THEME_ENUM = """from enum import Enum

__all__ = ['Theme']


class Theme(Enum):
\tLIGHT = 'light'
\tDARK = 'dark'
"""

LOCALE_ENUM = """from enum import Enum

__all__= ['Locale']


class Locale(Enum):
\tenUS = 'English (United States)'
\tsiLK = 'Sinhala (Sri Lanka)'
"""

APP_THEME = """from arceion.qt.res import Theme as ThemeMeta, ColorTheme, Images, LocaleBuilder
from enums import Theme, Locale

__all__ = ['AppTheme']


class AppTheme(ThemeMeta):
\tcolorTheme = Theme.LIGHT
\tcolorPalette = {
\t\tTheme.LIGHT.value: ColorTheme(
\t\t\tprimary="#4CAF50",
\t\t\tsecondary="#FF9800",
\t\t\tbackground="#F2F8FC",
\t\t\ttext="#212121",
\t\t\taccent="#03A9F4",
\t\t\terror="#F44336",
\t\t),
\t\tTheme.DARK.value: ColorTheme(
\t\t\tprimary="#4CAF50",
\t\t\tsecondary="#FF9800",
\t\t\tbackground="#121212",
\t\t\ttext="#E0E0E0",
\t\t\taccent="#03A9F4",
\t\t\terror="#F44336",
\t\t),
\t}
\tcolors = colorPalette[colorTheme.value]

\timageTheme = Theme.LIGHT
\timages = Images(
\t\ttheme=Theme.LIGHT,
\t\tdefault=Theme.LIGHT,

\t\tlogoTranspatent='Arceion Logo 1024X1024 Transparent Round.png',
\t\tlogoWhiteBg='Arceion Logo 1024X1024 White Round.png',
\t)

\tlocale = LocaleBuilder(locale= Locale.enUS, default=Locale.enUS)
"""

HOME_VIEW = '''from PyQt6.QtWidgets import QVBoxLayout, QToolButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from arceion.qt.core import View, WindowType
from arceion.qt.contrib.widgets.Attr import Margin, Padding
from arceion.qt.contrib.widgets.Widget import GetStarted
from arceion.qt.res import Icons
from arceion.qt.logger import Logger
from arceion.qt.util import UI
from enums import Theme
from res import AppTheme

__all__ = ['HomeView']


class HomeView(View):
\tdef __init__(self, parent: WindowType | None = None):
\t\tsuper().__init__(parent, 'Home')
\t\tself.setObjectName('HomeView')
\t\tself.setContentsMargins(Margin(0))
\t\tself.setStyleSheet("background-color: transparent;")

\t\tself.themeButton = QToolButton(self)
\t\tself.themeButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
\t\tself.themeButton.clicked.connect(lambda: self._toggle_theme())

\t\tself.getStartedWidget = GetStarted(self, AppTheme)

\t\tself.mainLayout = QVBoxLayout(self)
\t\tself.mainLayout.setContentsMargins(Margin(0))
\t\tself.mainLayout.addWidget(self.themeButton, alignment=Qt.AlignmentFlag.AlignRight)
\t\tself.mainLayout.addWidget(self.getStartedWidget)
\t\tself.setLayout(self.mainLayout)

\t\tself._toggle_theme(theme=AppTheme.colorTheme)
\t\tself.updateTheme()

\tdef _toggle_theme(self, theme: Theme | None = None):
\t\tif theme is None:
\t\t\tprint("Toggling theme...")
\t\t\tcurrent_theme = AppTheme.colorTheme
\t\t\tthemes = list(Theme)
\t\t\tcurrent_index = themes.index(current_theme)
\t\t\tnext_index = (current_index + 1) % len(themes)
\t\t\tnew_theme = themes[next_index]
\t\t\tAppTheme.setColorTheme(new_theme)
\t\t\tLogger.debug(f"Theme switched to: {new_theme.value}")
\t\telse:
\t\t\tnew_theme = theme
\t\tself.themeButton.setText(f"{new_theme.value.capitalize()} Theme" if new_theme.value != "system" else "System")
\t\tself.themeButton.setIcon(
\t\t\tQIcon(getattr(Icons.Rounded, f"{new_theme.value}_mode" if new_theme.value != "system" else "desktop_windows").update(
\t\t\t\tcolor=AppTheme.colors.text.name()
\t\t\t).toPixmap())
\t\t)

\tdef onCreate(self) -> None:
\t\tpass

\tdef onResume(self) -> None:
\t\tpass

\tdef onDestroy(self) -> bool:
\t\treturn super().onDestroy()

\tdef updateTheme(self):
\t\tlf.themeButton.setStyleSheet(f"""
\t\tQToolButton {{
\t\t\tcolor: {AppTheme.colors.text.name()};
\t\t\tmargin: {Margin(5, 5, 10, 5).qss};
\t\t\tpadding: {Padding(4, 6).qss};
\t\t}}
\t\t""")
\t\tself.getStartedWidget.updateTheme()
'''


LOCALE_EN_US = """{
\t"welcome_title": "The application worked successfully!",
\t"welcome_subtitle": "Congratulations on your first Arceion Qt application.",
\t"getting_started_title": "Getting Started",
\t"getting_started_desc": "You are seeing this page because you have successfully created an Arceion Qt application.",
\t"next_steps_title": "Next Steps",
\t"next_steps_items": [
\t\t"Create your first view in the views/ directory",
\t\t"Define your models in the models/ directory",
\t\t"Figure your theme in res/AppTheme.py",
\t\t"Localization strings in res/locale/"
\t],
\t"documentation_title": "Documentation",
\t"documentation_items": [
\t\t"Views & Navigation: Learn how to create views and navigate between them",
\t\t"Models & Data: Understand data models and API integration",
\t\t"Themeing: Customize colors, fonts, and styles",
\t\t"Widgets: Explore built-in widgets and create custom ones"
\t],
\t"quick_links_title": "Quick Links",
\t"footer_text": "You're seeing this message because you haven't customized the HomeView yet."
}
"""

LOCALE_SI_LK = """{
\t"welome_title": "යෙදුම සාර්ථකව ක්‍රියා විය!",
\t"welcome_subtitle": "ඔබේ පළමු Arceion Qt යෙදුම සඳහා සුභ පැතුම්.",
\t"getting_started_title": "ආරම්භ කිරීම",
\t"getting_started_desc": "ඔබට මෙම පිටුව පෙනෙන්නේ Arceion Qt යෙදුමක් සාර්ථකව නිර්මාණය කර ඇති නිසාය.",
\t"next_steps_title": "ඊළඟ පියවර",
\t"next_steps_items": [
\t\t"views/ නාමාවලියෙහි ඔබේ පළමු දසුන නිර්මාණය කරන්න",
\t\t"models/ නාමාවලියෙහි ඔබේ ආකෘති අර්ථ දක්වන්න",
\t\tres/AppTheme.py හි ඔබේ තේමාව වින්‍යාස කරන්න",
\t\t"res/locale/ හි භාෂා පරිවර්තන එක් කරන්න"
\t],
\t"documentation_title": "ලේඛන",
\t"documentation_items": [
\t\t"දසුන සහ සංචාලනය: දසුන නිර්මාණය කිරීම සහ ඒවා අතර සංචාලනය කිරීම ඉගෙන ගන්න",
\t\t"ආකෘති සහ දත්ත: දත්ත ආකෘති සහ API ඒකාබද්ධතාවය තේරුම් ගන්න",
\t\t"තේමා කිරීම: වර්ණ, අකුරු සහ මෝස්තර අභිරුචිකරණය කරන්න",
\t\t"විජට්: ඇති විජට් ගවේෂණය කර අභිරුචි ඒවා නිර්මාණය කරන්න"
\t],
\t"quick_links_title": "ඉක්මන් සබැඳි",
\t"footer_text": "ඔබ තවමත් HomeView අභිරුචිකරණය කර නොමැති නිසා මෙම පණිවිඩය දිස්වේ."
}
"""

COMPONENTS_INIT = """
__all__ = []
"""

ENUMS_INIT = """from .Theme import Theme
from .Locale import Locale

__all__ = ['Theme', 'Locale']
"""

MODELS_INIT = """
__all__ = []
"""

REQUESTS_INIT = """
__all__ = []
"""

RESPONSES_INIT = """
__all__ = []
"""

VIEWS_INIT = """from .HomeView import HomeView

__all__ = ['HomeView']
"""

RES_INIT = """from .AppTheme import AppTheme

__all__ = ['AppTheme']
"""

SERVICES_INIT = """
__all__ = []
"""
