from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QScrollArea, QVBoxLayout, QWidget

from arceion.qt.contrib.enums import FontWeight
from arceion.qt.contrib.styles import Card as CardStyle
from arceion.qt.contrib.styles import Label as LabelStyle
from arceion.qt.contrib.widgets.Attr import Margin, Padding
from arceion.qt.res import Icons, SystemIcon, Theme
from arceion.qt.util import UI

__all__ = ["GetStarted"]


class GetStarted(QScrollArea):
    AppTheme: type[Theme]
    loaded: bool = False

    def __init__(self, parent: QWidget, AppTheme: type[Theme]):
        if not parent:
            raise ValueError("Parent widget cannot be None")
        if not issubclass(AppTheme, Theme):
            raise TypeError("AppTheme must be a subclass of Theme")

        super().__init__(parent)
        self.AppTheme = AppTheme

        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Container widget
        container = QFrame()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(UI.dp(40), UI.dp(30), UI.dp(40), UI.dp(30))
        main_layout.setSpacing(UI.dp(30))

        # Header section with logo and welcome message
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.setSpacing(UI.dp(20))

        # Logo
        self.logo_label = QLabel(self)
        logo_pixmap = UI.pixmap(AppTheme.images.logoTranspatent, UI.dp(120), UI.dp(120))
        self.logo_label.setPixmap(logo_pixmap)
        self.logo_label.setFixedSize(UI.dp(120), UI.dp(120))
        self.logo_label.setScaledContents(True)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Welcome title
        self.title_label = QLabel(AppTheme.locale.welcome_title, self)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setWordWrap(True)

        # Subtitle
        self.subtitle_label = QLabel(AppTheme.locale.welcome_subtitle, self)
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setWordWrap(True)

        header_layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.subtitle_label, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(header_layout)

        # Divider
        self.line1 = QFrame()
        self.line1.setFrameShape(QFrame.Shape.HLine)
        self.line1.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(self.line1)

        # Content sections in two columns
        content_layout = QHBoxLayout()
        content_layout.setSpacing(UI.dp(30))

        # Left column
        left_column = QVBoxLayout()
        left_column.setSpacing(UI.dp(20))
        self.getting_started_card = self._create_getting_started_section()
        left_column.addWidget(self.getting_started_card)
        self.next_steps_card = self._create_next_steps_section()
        left_column.addWidget(self.next_steps_card)
        left_column.addStretch()

        # Right column
        right_column = QVBoxLayout()
        right_column.setSpacing(UI.dp(20))
        self.documentation_card = self._create_documentation_section()
        right_column.addWidget(self.documentation_card)
        right_column.addStretch()

        content_layout.addLayout(left_column, 1)
        content_layout.addLayout(right_column, 1)
        main_layout.addLayout(content_layout)

        # Footer
        self.line2 = QFrame()
        self.line2.setFrameShape(QFrame.Shape.HLine)
        self.line2.setFrameShadow(QFrame.Shadow.Sunken)

        self.footer_label = QLabel(AppTheme.locale.footer_text, self)
        self.footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.footer_label.setWordWrap(True)

        main_layout.addStretch()
        main_layout.addWidget(self.line2)
        main_layout.addWidget(self.footer_label)

        container.setLayout(main_layout)
        self.setWidget(container)

        self.loaded = True
        self.updateTheme()

    def _create_section_card(self, title: str, icon_char: SystemIcon | None = None) -> tuple[QFrame, QVBoxLayout]:
        """Create a card container for a section"""
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)

        card.icon_char = icon_char

        layout = QVBoxLayout(card)
        layout.setSpacing(UI.dp(15))

        # Section title with icon
        title_layout = QHBoxLayout()
        title_layout.setSpacing(UI.dp(10))

        if icon_char:
            card.icon_label = QLabel()
            title_layout.addWidget(card.icon_label)

        card.section_title = QLabel(title)
        title_layout.addWidget(card.section_title)
        title_layout.addStretch()

        layout.addLayout(title_layout)

        return card, layout

    def _create_getting_started_section(self) -> QFrame:
        """Create the Getting Started section"""
        card, layout = self._create_section_card(
            self.AppTheme.locale.getting_started_title, Icons.Outlined.rocket_launch
        )

        card.desc = QLabel(self.AppTheme.locale.getting_started_desc)
        card.desc.setWordWrap(True)
        layout.addWidget(card.desc)

        return card

    def _create_next_steps_section(self) -> QFrame:
        """Create the Next Steps section"""
        card, layout = self._create_section_card(self.AppTheme.locale.next_steps_title, Icons.Outlined.checklist)

        card.next_steps_list = []

        for i, step in enumerate(self.AppTheme.locale.next_steps_items, 1):
            step_layout = QHBoxLayout()
            step_layout.setSpacing(UI.dp(10))

            # Number badge
            number_label = QLabel(str(i))
            number_label.setFixedSize(UI.dp(24), UI.dp(24))
            number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Step text
            step_label = QLabel(step)
            step_label.setWordWrap(True)

            step_layout.addWidget(number_label)
            step_layout.addWidget(step_label, 1)

            layout.addLayout(step_layout)
            card.next_steps_list.append([number_label, step_label])

        return card

    def _create_documentation_section(self) -> QFrame:
        """Create the Documentation section"""
        card, layout = self._create_section_card(self.AppTheme.locale.documentation_title, Icons.Outlined.menu_book)

        documentationLinks = [  # noqa: F841
            "https://arceion.com/docs/qt/views-and-navigation",
            "https://arceion.com/docs/qt/models-and-data",
            "https://arceion.com/docs/qt/theming",
            "https://arceion.com/docs/qt/widgets",
        ]

        card.documentation_list = []

        for doc_item in self.AppTheme.locale.documentation_items:
            # Split title and description
            parts = doc_item.split(": ", 1)
            doc_title = parts[0] if len(parts) > 0 else doc_item
            doc_desc = parts[1] if len(parts) > 1 else ""

            doc_layout = QVBoxLayout()
            doc_layout.setSpacing(UI.dp(5))

            # Icon and title
            title_layout = QHBoxLayout()
            title_layout.setSpacing(UI.dp(8))

            icon = QLabel()

            title = QLabel(doc_title)

            title_layout.addWidget(icon)
            title_layout.addWidget(title)
            title_layout.addStretch()

            doc_layout.addLayout(title_layout)

            card.documentation_list.append([icon, title])

            # Description
            if doc_desc:
                desc = QLabel(doc_desc)
                desc.setWordWrap(True)
                desc.setIndent(UI.dp(22))
                doc_layout.addWidget(desc)

                card.documentation_list[-1] += [desc]

            layout.addLayout(doc_layout)

        return card

    def updateTheme(self):
        if self.loaded:
            self.setStyleSheet(CardStyle.defaultScrollArea.qss)

            LabelStyle.label.update(
                color=self.AppTheme.colors.primary.name(),
                fontWeight=FontWeight.Bold,
                fontSize=UI.sp(24),
            ).apply(self.title_label)

            LabelStyle.label.update(
                color=self.AppTheme.colors.text.name(),
                fontSize=UI.sp(14),
            ).apply(self.subtitle_label)

            self.line1.setStyleSheet(
                f"""background-color: {self.AppTheme.colors.text.name()}; max-height: 1px; opacity: 0.2;
				margin: {Margin(0).qss}; padding: {Padding(0).qss};"""
            )

            LabelStyle.label.update(
                color=self.AppTheme.colors.text.name(),
                fontSize=UI.sp(11),
                opacity=0.7,
            ).apply(self.footer_label)

            self.line2.setStyleSheet(
                f"""background-color: {self.AppTheme.colors.text.name()}; max-height: 1px; opacity: 0.2; 
				margin: {Margin(0).qss}; padding: {Padding(0).qss};"""
            )

            cards = [self.getting_started_card, self.next_steps_card, self.documentation_card]
            for card in cards:
                card.setStyleSheet(f"""
					QFrame {{
						background-color: {self.AppTheme.colors.background.lighter(105).name()};
						border: 1px solid {self.AppTheme.colors.text.name()};
						border-radius: {UI.dp(8)}px;
						padding: {UI.dp(20)}px;
					}}
				""")
                if card.icon_char:
                    card.icon_label.setPixmap(
                        card.icon_char.update(
                            color=self.AppTheme.colors.text.name(),
                        ).toPixmap()
                    )
                LabelStyle.label.update(
                    color=self.AppTheme.colors.text.name(),
                    fontSize=UI.sp(20),
                ).apply(card.icon_label)

                LabelStyle.label.update(
                    color=self.AppTheme.colors.text.name(),
                    fontWeight=FontWeight.SemiBold,
                    fontSize=UI.sp(16),
                ).apply(card.section_title)

            LabelStyle.label.update(
                color=self.AppTheme.colors.text.name(),
                fontSize=UI.sp(12),
            ).apply(self.getting_started_card.desc)

            for step in self.next_steps_card.next_steps_list:
                step[0].setStyleSheet(f"""
					background-color: {self.AppTheme.colors.primary.name()};
					color: white;
					border-radius: {UI.dp(12)}px;
					font-weight: bold;
					font-size: {UI.sp(11)}px;
				""")
                LabelStyle.label.update(
                    color=self.AppTheme.colors.text.name(),
                    fontSize=UI.sp(12),
                ).apply(step[1])

            for item in self.documentation_card.documentation_list:
                item[0].setPixmap(
                    Icons.Outlined.arrow_forward.update(
                        color=self.AppTheme.colors.text.name(),
                    ).toPixmap()
                )
                LabelStyle.label.update(
                    color=self.AppTheme.colors.text.name(),
                    fontSize=UI.sp(14),
                ).apply(item[0])

                LabelStyle.label.update(
                    color=self.AppTheme.colors.text.name(),
                    fontWeight=FontWeight.Medium,
                    fontSize=UI.sp(12),
                ).apply(item[1])

                if len(item) > 2:
                    LabelStyle.label.update(
                        color=self.AppTheme.colors.text.name(),
                        fontSize=UI.sp(11),
                        opacity=0.8,
                    ).apply(item[2])
