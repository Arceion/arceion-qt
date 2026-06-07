"""
Template strings for project scaffolding
"""

__all__ = [
    'MAIN_PY',
    'APP_PY',
    'ENV_PY',
    'PYPROJECT_TOML',
    'THEME_ENUM',
    'LOCALE_ENUM',
    'APP_THEME',
    'HOME_VIEW',
    'LOCALE_EN_US',
    'LOCALE_SI_LK',
    'ENUMS_INIT',
    'VIEWS_INIT',
    'RES_INIT',
]

MAIN_PY = '''import faulthandler
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
\t# QFontDatabase.addApplicationFont('res/fonts/YourFont.ttf')
\t# app.setFont(QFont('YourFont', 9))

\tfrom arceion.qt.res import Icons
\tapp.setWindowIcon(Icons.settings_applications)

\tfrom {app_class} import {app_class}
\t{app_class}()
\tsys.exit(app.exec())
'''

APP_PY = '''from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPalette

from enums import Theme
from arceion.qt.core import Window
from arceion.qt.util import UI
from res import AppTheme

__all__ = ['{app_class}']


class {app_class}(Window):
\tdef __init__(self):
\t\tsuper({app_class}, self).__init__(row=4, column=2)

\t\tself.setObjectName('MainWindow')
\t\tself.setWindowTitle('{project_name}')
\t\tAppTheme.setColorTheme(Theme.DARK)
\t\tself.setWindowIcon(QIcon(UI.pixmap(
\t\t\tAppTheme.images.logoWhiteBg, 32, 32, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
\t\t\tQt.TransformationMode.SmoothTransformation
\t\t)))
\t\tself.setMinimumSize(UI.size(560, 360))
\t\tself.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
\t\tpal = self.palette()
\t\tpal.setColor(QPalette.ColorRole.Window, AppTheme.colors.background)
\t\tpal.setColor(QPalette.ColorRole.WindowText, AppTheme.colors.text)
\t\tself.setPalette(pal)
\t\tself.setFocus()

\t\tfrom views import HomeView
\t\tself.navigate(HomeView)

\t\tself.show()

\tdef f11(self):
\t\tif self.isFullScreen():
\t\t\tself.showNormal()
\t\telse:
\t\t\tself.showFullScreen()
'''

ENV_PY = '''from arceion.qt.env import Env, EnvManager, EnvMode

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
'''

PYPROJECT_TOML = '''[project]
name = "{project_name}"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
\t"arceion-qt",
\t"pyqt6>=6.11.0",
]
'''

THEME_ENUM = '''from enum import Enum

__all__ = ['Theme']


class Theme(Enum):
\tLIGHT = 'light'
\tDARK = 'dark'
'''

LOCALE_ENUM = '''from enum import Enum

__all__= ['Locale']


class Locale(Enum):
\tenUS = 'English (United States)'
\tsiLK = 'Sinhala (Sri Lanka)'
'''

APP_THEME = '''from arceion.qt.res import Theme as ThemeMeta, ColorTheme, Images, LocaleBuilder
from enums import Theme, Locale

__all__ = ['AppTheme']


class AppTheme(ThemeMeta):
\tcolorTheme = Theme.LIGHT
\tcolorPalette = {
\t\tTheme.LIGHT.value: ColorTheme(
\t\t\tprimary="#4CAF50",
\t\t\tsecondary="#FF9800",
\t\t\tbackground="#FFFFFF",
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
'''

HOME_VIEW = '''from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QWidget
from arceion.qt.contrib.enums import FontWeight
from arceion.qt.core import View, WindowType
from arceion.qt.contrib.styles import Label as LabelStyle
from arceion.qt.util import UI
from arceion.qt.res import Icons
from res import AppTheme

__all__ = ['HomeView']


class HomeView(View):
\tdef __init__(self, parent: WindowType | None = None):
\t\tsuper(HomeView, self).__init__(parent, 'Home')
\t\tself.setObjectName('HomeView')

\t\t# Main scroll area
\t\tscroll = QScrollArea(self)
\t\tscroll.setWidgetResizable(True)
\t\tscroll.setFrameShape(QFrame.Shape.NoFrame)
\t\tscroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

\t\t# Container widget
\t\tcontainer = QWidget()
\t\tmain_layout = QVBoxLayout(container)
\t\tmain_layout.setContentsMargins(UI.dp(40), UI.dp(30), UI.dp(40), UI.dp(30))
\t\tmain_layout.setSpacing(UI.dp(30))

\t\t# Header section with logo and welcome message
\t\theader_layout = QVBoxLayout()
\t\theader_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
\t\theader_layout.setSpacing(UI.dp(20))

\t\t# Logo
\t\tlogo_label = QLabel(self)
\t\tlogo_pixmap = UI.pixmap(AppTheme.images.logoTranspatent, UI.dp(120), UI.dp(120))
\t\tlogo_label.setPixmap(logo_pixmap)
\t\tlogo_label.setFixedSize(UI.dp(120), UI.dp(120))
\t\tlogo_label.setScaledContents(True)
\t\tlogo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

\t\t# Welcome title
\t\ttitle_label = QLabel(AppTheme.locale.welcome_title, self)
\t\ttitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
\t\ttitle_label.setWordWrap(True)
\t\tLabelStyle.label.update(
\t\t\tcolor=AppTheme.colors.primary.name(),
\t\t\tfontWeight=FontWeight.Bold,
\t\t\tfontSize=UI.sp(24),
\t\t).apply(title_label)

\t\t# Subtitle
\t\tsubtitle_label = QLabel(AppTheme.locale.welcome_subtitle, self)
\t\tsubtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
\t\tsubtitle_label.setWordWrap(True)
\t\tLabelStyle.label.update(
\t\t\tcolor=AppTheme.colors.text.name(),
\t\t\tfontSize=UI.sp(14),
\t\t).apply(subtitle_label)

\t\theader_layout.addWidget(logo_label)
\t\theader_layout.addWidget(title_label)
\t\theader_layout.addWidget(subtitle_label)
\t\tmain_layout.addLayout(header_layout)

\t\t# Divider
\t\tmain_layout.addWidget(self._create_divider())

\t\t# Content sections in two columns
\t\tcontent_layout = QHBoxLayout()
\t\tcontent_layout.setSpacing(UI.dp(30))

\t\t# Left column
\t\tleft_column = QVBoxLayout()
\t\tleft_column.setSpacing(UI.dp(20))
\t\tleft_column.addWidget(self._create_getting_started_section())
\t\tleft_column.addWidget(self._create_next_steps_section())
\t\tleft_column.addStretch()

\t\t# Right column
\t\tright_column = QVBoxLayout()
\t\tright_column.setSpacing(UI.dp(20))
\t\tright_column.addWidget(self._create_documentation_section())
\t\tright_column.addStretch()

\t\tcontent_layout.addLayout(left_column, 1)
\t\tcontent_layout.addLayout(right_column, 1)
\t\tmain_layout.addLayout(content_layout)

\t\t# Footer
\t\tmain_layout.addStretch()
\t\tmain_layout.addWidget(self._create_divider())
\t\tfooter_label = QLabel(AppTheme.locale.footer_text, self)
\t\tfooter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
\t\tfooter_label.setWordWrap(True)
\t\tLabelStyle.label.update(
\t\t\tcolor=AppTheme.colors.text.name(),
\t\t\tfontSize=UI.sp(11),
\t\t).apply(footer_label)
\t\tfooter_label.setStyleSheet(f"color: {AppTheme.colors.text.name()}; opacity: 0.7;")
\t\tmain_layout.addWidget(footer_label)

\t\tcontainer.setLayout(main_layout)
\t\tscroll.setWidget(container)

\t\t# Main layout
\t\tview_layout = QVBoxLayout(self)
\t\tview_layout.setContentsMargins(0, 0, 0, 0)
\t\tview_layout.addWidget(scroll)
\t\tself.setLayout(view_layout)

\tdef _create_divider(self) -> QFrame:
\t\t"""Create a horizontal divider line"""
\t\tline = QFrame()
\t\tline.setFrameShape(QFrame.Shape.HLine)
\t\tline.setFrameShadow(QFrame.Shadow.Sunken)
\t\tline.setStyleSheet(f"background-color: {AppTheme.colors.text.name()}; max-height: 1px; opacity: 0.2;")
\t\treturn line

\tdef _create_section_card(self, title: str, icon_char: str = None) -> tuple[QFrame, QVBoxLayout]:
\t\t"""Create a card container for a section"""
\t\tcard = QFrame()
\t\tcard.setFrameShape(QFrame.Shape.StyledPanel)
\t\tcard.setStyleSheet(f"""
\t\t\tQFrame {{
\t\t\t\tbackground-color: {AppTheme.colors.background.lighter(105).name()};
\t\t\t\tborder: 1px solid {AppTheme.colors.text.name()};
\t\t\t\tborder-radius: {UI.dp(8)}px;
\t\t\t\tpadding: {UI.dp(20)}px;
\t\t\t}}
\t\t""")

\t\tlayout = QVBoxLayout(card)
\t\tlayout.setSpacing(UI.dp(15))

\t\t# Section title with icon
\t\ttitle_layout = QHBoxLayout()
\t\ttitle_layout.setSpacing(UI.dp(10))

\t\tif icon_char:
\t\t\ticon_label = QLabel(icon_char)
\t\t\ticon_label.setFont(Icons.font(UI.sp(20)))
\t\t\tLabelStyle.label.update(
\t\t\t\tcolor=AppTheme.colors.primary.name(),
\t\t\t\tfontSize=UI.sp(20),
\t\t\t).apply(icon_label)
\t\t\ttitle_layout.addWidget(icon_label)

\t\tsection_title = QLabel(title)
\t\tLabelStyle.label.update(
\t\t\tcolor=AppTheme.colors.text.name(),
\t\t\tfontWeight=FontWeight.SemiBold,
\t\t\tfontSize=UI.sp(16),
\t\t).apply(section_title)
\t\ttitle_layout.addWidget(section_title)
\t\ttitle_layout.addStretch()

\t\tlayout.addLayout(title_layout)

\t\treturn card, layout

\tdef _create_getting_started_section(self) -> QFrame:
\t\t"""Create the Getting Started section"""
\t\tcard, layout = self._create_section_card(AppTheme.locale.getting_started_title, Icons.Outlined.rocket_launch)

\t\tdesc = QLabel(AppTheme.locale.getting_started_desc)
\t\tdesc.setWordWrap(True)
\t\tLabelStyle.label.update(
\t\t\tcolor=AppTheme.colors.text.name(),
\t\t\tfontSize=UI.sp(12),
\t\t).apply(desc)
\t\tlayout.addWidget(desc)

\t\treturn card

\tdef _create_next_steps_section(self) -> QFrame:
\t\t"""Create the Next Steps section"""
\t\tcard, layout = self._create_section_card(AppTheme.locale.next_steps_title, Icons.Outlined.checklist)

\t\tfor i, step in enumerate(AppTheme.locale.next_steps_items, 1):
\t\t\tstep_layout = QHBoxLayout()
\t\t\tstep_layout.setSpacing(UI.dp(10))

\t\t\t# Number badge
\t\t\tnumber_label = QLabel(str(i))
\t\t\tnumber_label.setFixedSize(UI.dp(24), UI.dp(24))
\t\t\tnumber_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
\t\t\tnumber_label.setStyleSheet(f"""
\t\t\t\tbackground-color: {AppTheme.colors.primary.name()};
\t\t\t\tcolor: white;
\t\t\t\tborder-radius: {UI.dp(12)}px;
\t\t\t\tfont-weight: bold;
\t\t\t\tfont-size: {UI.sp(11)}px;
\t\t\t""")

\t\t\t# Step text
\t\t\tstep_label = QLabel(step)
\t\t\tstep_label.setWordWrap(True)
\t\t\tLabelStyle.label.update(
\t\t\t\tcolor=AppTheme.colors.text.name(),
\t\t\t\tfontSize=UI.sp(12),
\t\t\t).apply(step_label)

\t\t\tstep_layout.addWidget(number_label)
\t\t\tstep_layout.addWidget(step_label, 1)

\t\t\tlayout.addLayout(step_layout)

\t\treturn card

\tdef _create_documentation_section(self) -> QFrame:
\t\t"""Create the Documentation section"""
\t\tcard, layout = self._create_section_card(AppTheme.locale.documentation_title, Icons.Outlined.menu_book)

\t\tfor doc_item in AppTheme.locale.documentation_items:
\t\t\t# Split title and description
\t\t\tparts = doc_item.split(': ', 1)
\t\t\tdoc_title = parts[0] if len(parts) > 0 else doc_item
\t\t\tdoc_desc = parts[1] if len(parts) > 1 else ""

\t\t\tdoc_layout = QVBoxLayout()
\t\t\tdoc_layout.setSpacing(UI.dp(5))

\t\t\t# Icon and title
\t\t\ttitle_layout = QHBoxLayout()
\t\t\ttitle_layout.setSpacing(UI.dp(8))

\t\t\ticon = QLabel(Icons.Outlined.arrow_forward)
\t\t\ticon.setFont(Icons.font(UI.sp(14)))
\t\t\tLabelStyle.label.update(
\t\t\t\tcolor=AppTheme.colors.accent.name(),
\t\t\t\tfontSize=UI.sp(14),
\t\t\t).apply(icon)

\t\t\ttitle = QLabel(doc_title)
\t\t\tLabelStyle.label.update(
\t\t\t\tcolor=AppTheme.colors.text.name(),
\t\t\t\tfontWeight=FontWeight.Medium,
\t\t\t\tfontSize=UI.sp(12),
\t\t\t).apply(title)

\t\t\ttitle_layout.addWidget(icon)
\t\t\ttitle_layout.addWidget(title)
\t\t\ttitle_layout.addStretch()

\t\t\tdoc_layout.addLayout(title_layout)

\t\t\t# Description
\t\t\tif doc_desc:
\t\t\t\tdesc = QLabel(doc_desc)
\t\t\t\tdesc.setWordWrap(True)
\t\t\t\tdesc.setIndent(UI.dp(22))
\t\t\t\tLabelStyle.label.update(
\t\t\t\t\tcolor=AppTheme.colors.text.name(),
\t\t\t\t\tfontSize=UI.sp(11),
\t\t\t\t).apply(desc)
\t\t\t\tdesc.setStyleSheet(f"color: {AppTheme.colors.text.name()}; opacity: 0.8;")
\t\t\t\tdoc_layout.addWidget(desc)

\t\t\tlayout.addLayout(doc_layout)

\t\treturn card

\tdef onCreate(self) -> None:
\t\tpass

\tdef onResume(self) -> None:
\t\tpass

\tdef onDestroy(self) -> bool:
\t\treturn super().onDestroy()
'''

LOCALE_EN_US = '''{
  "welcome_title": "The application worked successfully!",
  "welcome_subtitle": "Congratulations on your first Arceion Qt application.",
  "getting_started_title": "Getting Started",
  "getting_started_desc": "You are seeing this page because you have successfully created an Arceion Qt application.",
  "next_steps_title": "Next Steps",
  "next_steps_items": [
    "Create your first view in the views/ directory",
    "Define your models in the models/ directory",
    "Configure your theme in res/AppTheme.py",
    "Add localization strings in res/locale/"
  ],
  "documentation_title": "Documentation",
  "documentation_items": [
    "Views & Navigation: Learn how to create views and navigate between them",
    "Models & Data: Understand data models and API integration",
    "Theming: Customize colors, fonts, and styles",
    "Widgets: Explore built-in widgets and create custom ones"
  ],
  "quick_links_title": "Quick Links",
  "footer_text": "You're seeing this message because you haven't customized the HomeView yet."
}
'''

LOCALE_SI_LK = '''{
  "welcome_title": "යෙදුම සාර්ථකව ක්‍රියා විය!",
  "welcome_subtitle": "ඔබේ පළමු Arceion Qt යෙදුම සඳහා සුභ පැතුම්.",
  "getting_started_title": "ආරම්භ කිරීම",
  "getting_started_desc": "ඔබට මෙම පිටුව පෙනෙන්නේ Arceion Qt යෙදුමක් සාර්ථකව නිර්මාණය කර ඇති නිසාය.",
  "next_steps_title": "ඊළඟ පියවර",
  "next_steps_items": [
    "views/ නාමාවලියෙහි ඔබේ පළමු දසුන නිර්මාණය කරන්න",
    "models/ නාමාවලියෙහි ඔබේ ආකෘති අර්ථ දක්වන්න",
    "res/AppTheme.py හි ඔබේ තේමාව වින්‍යාස කරන්න",
    "res/locale/ හි භාෂා පරිවර්තන එක් කරන්න"
  ],
  "documentation_title": "ලේඛන",
  "documentation_items": [
    "දසුන සහ සංචාලනය: දසුන නිර්මාණය කිරීම සහ ඒවා අතර සංචාලනය කිරීම ඉගෙන ගන්න",
    "ආකෘති සහ දත්ත: දත්ත ආකෘති සහ API ඒකාබද්ධතාවය තේරුම් ගන්න",
    "තේමා කිරීම: වර්ණ, අකුරු සහ මෝස්තර අභිරුචිකරණය කරන්න",
    "විජට්: ඇති විජට් ගවේෂණය කර අභිරුචි ඒවා නිර්මාණය කරන්න"
  ],
  "quick_links_title": "ඉක්මන් සබැඳි",
  "footer_text": "ඔබ තවමත් HomeView අභිරුචිකරණය කර නොමැති නිසා මෙම පණිවිඩය දිස්වේ."
}
'''

ENUMS_INIT = '''from .Theme import Theme
from .Locale import Locale

__all__ = ['Theme', 'Locale']
'''

VIEWS_INIT = '''from .HomeView import HomeView

__all__ = ['HomeView']
'''

RES_INIT = '''from .AppTheme import AppTheme

__all__ = ['AppTheme']
'''
