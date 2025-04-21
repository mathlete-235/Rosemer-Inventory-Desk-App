

DARK_THEME_1 = """
QWidget { background-color: #1e1e2f; color: #ffffff; } /* Deep Indigo */
QPushButton { background-color: #ff6f61; color: white; border-radius: 5px; padding: 5px; } /* Reddish Orange Buttons */
QPushButton:hover { background-color: #ff1744; } /* Bright Red Hover */
QTableWidget { background-color: #2a2a3d; color: white; gridline-color: #444; } /* Dark Purple Table */
QHeaderView::section { background-color: #4a148c; color: white; padding: 5px; font-weight: bold; } /* Deep Purple Headers */
QTableWidget::item:selected { background-color: #00e676; color: black; } /* Neon Green Selection */
"""
LIGHT_THEME_1 = """
QWidget { background-color: #f0f8ff; color: #333; } /* Light Blue Background */
QPushButton { background-color: #87cefa; color: #000; border-radius: 5px; padding: 5px; } /* Sky Blue Buttons */
QPushButton:hover { background-color: #4682b4; color: white; } /* Deep Sky Blue Hover */
QTableWidget { background-color: #ffffff; color: #333; gridline-color: #dcdcdc; } /* White Table */
QHeaderView::section { background-color: #ffcccb; color: black; padding: 5px; font-weight: bold; } /* Coral Column Headers */
QTableWidget::item:selected { background-color: #ffeb3b; color: black; } /* Yellow Selection */
"""

DARK_THEME_2 = """
QWidget { background-color: #002b36; color: #a7ffeb; } /* Deep Sea Blue Background */
QPushButton { background-color: #00796b; color: white; border-radius: 5px; padding: 5px; } /* Dark Turquoise Buttons */
QPushButton:hover { background-color: #004d40; } /* Deep Green Hover */
QTableWidget { background-color: #004d40; color: #a7ffeb; gridline-color: #00695c; } /* Deep Green Table */
QHeaderView::section { background-color: #009688; color: white; padding: 5px; font-weight: bold; } /* Rich Aquamarine Headers */
QTableWidget::item:selected { background-color: #cddc39; color: black; } /* Lime Green Selection */
"""

LIGHT_THEME_2 = """
QWidget { background-color: #e0f7fa; color: #004d40; } /* Soft Aquamarine Background */
QPushButton { background-color: #80deea; color: #004d40; border-radius: 5px; padding: 5px; } /* Light Sea Blue Buttons */
QPushButton:hover { background-color: #26c6da; color: white; } /* Deep Turquoise Hover */
QTableWidget { background-color: #ffffff; color: #004d40; gridline-color: #b2dfdb; } /* White Table */
QHeaderView::section { background-color: #4db6ac; color: white; padding: 5px; font-weight: bold; } /* Deep Aquamarine Headers */
QTableWidget::item:selected { background-color: #a7ffeb; color: #004d40; } /* Light Green Selection */
"""


LIGHT_THEME = """
QWidget { background-color: white; color: black; }
QPushButton { background-color: lightgray; color: black; }
QTableWidget { background-color: white; color: black;  border: 1px solid gray;} 
QHeaderView::section {font-weight: bold; padding: 6px; }

"""
#QTableWidget::item {    padding: 10px; /* Spacing size */ }

DARK_THEME = """
QWidget { background-color: #121212; color: white; }
QPushButton { background-color: #333; color: white; }
QTableWidget { background-color: #222; color: white; border: 1px solid gray; }
QHeaderView::section { background-color: #333; color: white; padding: 5px; }
"""

NEON_CYBERPUNK = """
        QMainWindow {
            background-color: #0a0a0a;        }
        QTableWidget {
            background-color: #1a1a1a;
            gridline-color: #ff00ff;
            color: #00ff9f;   border: 1px;
        }
        QHeaderView::section {
            background-color: #ff00ff;
            color: #0a0a0a;
            font-weight: bold;
            padding: 6px;
        }
        QPushButton {
            background-color: #00ff9f;
            color: #0a0a0a;
            border: 2px solid #ff00ff;
            border-radius: 5px;
            padding: 5px;
            min-width: 80px;
        }
        QPushButton:hover {
            background-color: #ff00ff;
            color: #00ff9f;
        }
        QMenuBar {
            background-color: #0a0a0a;
            color: #00ff9f;
        }
        QMenuBar::item:selected {
            background-color: #ff00ff;
            color: #0a0a0a;
        }
        """

SUNSET_GRADIENT = """
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                      stop:0 #ff6b6b, stop:1 #ff9f43);
        }
        QTableWidget {
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 8px;
            color: #2d3436;
        }
        QHeaderView::section {
            background-color: #ff9f43;
            color: #ffffff;
            padding: 5px;
            border-radius: 4px;
        }
        QPushButton {
            background-color: #2d3436;
            color: #ffffff;
            border-radius: 15px;
            padding: 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #ff6b6b;
        }
        QMenuBar {
            background-color: rgba(45, 52, 54, 0.8);
            color: #ffffff;
        }
        """
CANDY_LAND = """
        QMainWindow {
            background-color: #f8a5c2;
        }
        QTableWidget {
            background-color: #ffffff;
            border: 3px solid #f78fb3;
            border-radius: 10px;
        }
        QHeaderView::section {
            background-color: #f78fb3;
            color: #ffffff;
            font-size: 14px;
            padding: 5px
        }
        QPushButton {
            background-color: #63cdda;
            color: #ffffff;
            border: none;
            border-radius: 20px;
            padding: 10px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #ea8685;
        }
        QMenuBar {
            background-color: #f8a5c2;
            color: #ffffff;
        }
        QMenuBar::item:selected {
            background-color: #63cdda;
        }
        """
NEON_NIGHTS =  """* {
    background-color: #1a1a1a;
    color: #ffffff;
}

QMenuBar, QMenu {
    background-color: #2d2d2d;
    border: 2px solid #ff00ff;
}

QMenu::item:selected { 
    background-color: #00ff00;
    color: #000000;
}

QPushButton {
    background: #ff00ff;
    border-radius: 8px;
    padding: 6px;
    color: #000000;
}
QHeaderView::section {font-weight: bold; padding: 6px; }
        """

OCEAN_DEPTHS =  """
        QMainWindow {
            background-color: #0a192f;
        }
        QTableWidget {
            background-color: #172a45;
            color: #64ffda;
            border: 2px solid #64ffda;
        }
        QHeaderView::section {
            background-color: #64ffda;
            color: #0a192f;
            font-weight: bold;
            padding: 5px;
        }
        QPushButton {
            background-color: #233554;
            color: #64ffda;
            border: 1px solid #64ffda;
            border-radius: 3px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #64ffda;
            color: #0a192f;
        }
        QMenuBar {
            background-color: #0a192f;
            color: #64ffda;
            border-bottom: 1px solid #64ffda;
        }
        """

SUNSET_GLOW =  """* {
    background: #ffd3b6;
    color: #d64161;
}
QHeaderView::section {font-weight: bold; padding: 6px; }

QMenu {
    background: #ffaaa5;
    border: 2px solid #d64161;
}

QPushButton {
    background: #d64161;
    color: white;
    border-radius: 10px;
}

QLineEdit {
    border: 2px solid #d64161;
    background: #fff;
}
        """
GALAXY_EXPLORER =  """QWidget {
    background: #2b1055;
    color: #ffffff;
}
QHeaderView::section {font-weight: bold; padding: 6px; }

QMenuBar {
    background: #7c43bd;
}

QPushButton {
    background: #ff7676;
    border: 2px solid #ffffff;
    color: #2b1055;
}

QScrollBar:vertical {
    background: #7c43bd;
}
        """
ELECTRIC_FOREST = """
        QMainWindow {
            background-color: #2a2a2a;
        }
        QTableWidget {
            background-color: #3d3d3d;
            color: #7fff00;
            gridline-color: #00ff7f;
        }
        QHeaderView::section {
            background-color: #00ff7f;
            color: #2a2a2a;
            font-weight: bold;
            padding: 5px;
        }
        QPushButton {
            background-color: #7fff00;
            color: #2a2a2a;
            border: 2px solid #00ff7f;
            border-radius: 8px;
            padding: 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #00ff7f;
            color: #2a2a2a;
        }
        QMenuBar {
            background-color: #3d3d3d;
            color: #7fff00;
        }
        QMenuBar::item:selected {
            background-color: #00ff7f;
            color: #2a2a2a;
        }
        """

 

MAC = """

QMainWindow {
    background-color:#ececec;
}
QPushButton, QToolButton, QCommandLinkButton{
    padding: 0 5px 0 5px;
    border-style: solid;
    border-top-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #c1c9cf, stop:1 #d2d8dd);
    border-right-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);
    border-bottom-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);
    border-left-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);
    border-width: 2px;
    border-radius: 8px;
    color: #616161;
    font-weight: bold;
    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #fbfdfd, stop:0.5 #ffffff, stop:1 #fbfdfd);
}
QPushButton::default, QToolButton::default, QCommandLinkButton::default{
    border: 2px solid transparent;
    color: #FFFFFF;
    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #84afe5, stop:1 #1168e4);
}
QPushButton:hover, QToolButton:hover, QCommandLinkButton:hover{
    color: #3d3d3d;
}
QPushButton:pressed, QToolButton:pressed, QCommandLinkButton:pressed{
    color: #aeaeae;
    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #ffffff, stop:0.5 #fbfdfd, stop:1 #ffffff);
}
QPushButton:disabled, QToolButton:disabled, QCommandLinkButton:disabled{
    color: #616161;
    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #dce7eb, stop:0.5 #e0e8eb, stop:1 #dee7ec);
}
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QTimeEdit, QDateEdit, QDateTimeEdit {
    border-width: 2px;
    border-radius: 8px;
    border-style: solid;
    border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);
    border-right-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);
    border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #c1c9cf, stop:1 #d2d8dd);
    border-left-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);
    background-color: #f4f4f4;
    color: #3d3d3d;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTimeEdit:focus, QDateEdit:focus, QDateTimeEdit:focus {
    border-width: 2px;
    border-radius: 8px;
    border-style: solid;
    border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);
    border-right-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);
    border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #85b7e3, stop:1 #9ec1db);
    border-left-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);
    background-color: #f4f4f4;
    color: #3d3d3d;
}
QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled, QTimeEdit:disabled, QDateEdit:disabled, QDateTimeEdit:disabled {
    color: #b9b9b9;
}
QSpinBox::up-button, QDoubleSpinBox::up-button, QTimeEdit::up-button, QDateEdit::up-button, QDateTimeEdit::up-button {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;
    color: #272727;
    border-left-width: 1px;
    border-left-color: darkgray;
    border-left-style: solid;
    border-top-right-radius: 3px;
    padding: 3px;
}
QSpinBox::down-button, QDoubleSpinBox::down-button, QTimeEdit::down-button, QDateEdit::down-button, QDateTimeEdit::down-button {
    subcontrol-origin: padding;
    subcontrol-position: bottom right;
    width: 15px;
    color: #272727;
    border-left-width: 1px;
    border-left-color: darkgray;
    border-left-style: solid;
    border-bottom-right-radius: 3px;
    padding: 3px;
}
QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed, QTimeEdit::up-button:pressed, QDateEdit::up-button:pressed, QDateTimeEdit::up-button:pressed {
    color: #aeaeae;
    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #ffffff, stop:0.5 #fbfdfd, stop:1 #ffffff);
}
QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed, QTimeEdit::down-button:pressed, QDateEdit::down-button:pressed, QDateTimeEdit::down-button:pressed {
    color: #aeaeae;
    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #ffffff, stop:0.5 #fbfdfd, stop:1 #ffffff);
}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover, QTimeEdit::up-button:hover, QDateEdit::up-button:hover, QDateTimeEdit::up-button:hover {
    color: #FFFFFF;
    border-top-right-radius: 5px;
    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #84afe5, stop:1 #1168e4);
    
}
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover, QTimeEdit::down-button:hover, QDateEdit::down-button:hover, QDateTimeEdit::down-button:hover {
    color: #FFFFFF;
    border-bottom-right-radius: 5px;
    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #84afe5, stop:1 #1168e4);
}
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow, QTimeEdit::up-arrow, QDateEdit::up-arrow, QDateTimeEdit::up-arrow {
    image: url(/usr/share/icons/Adwaita/16x16/actions/go-up-symbolic.symbolic.png);
}
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow, QTimeEdit::down-arrow, QDateEdit::down-arrow, QDateTimeEdit::down-arrow {
    image: url(/usr/share/icons/Adwaita/16x16/actions/go-down-symbolic.symbolic.png);
}
QProgressBar {
    max-height: 8px;
    text-align: center;
    font: italic bold 11px;
    color: #3d3d3d;
    border: 1px solid transparent;
    border-radius:4px;
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #ddd5d5, stop:0.5 #dad3d3, stop:1 #ddd5d5);
}
QProgressBar::chunk {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #467dd1, stop:0.5 #3b88fc, stop:1 #467dd1);
    border-radius: 4px;
}
QProgressBar:disabled {
    color: #616161;
}
QProgressBar::chunk:disabled {
    background-color: #aeaeae;
}
QSlider::groove {
    border: 1px solid #bbbbbb;
    background-color: #52595d;
    border-radius: 4px;
}
QSlider::groove:horizontal {
    height: 6px;
}
QSlider::groove:vertical {
    width: 6px;
}
QSlider::handle:horizontal {
    background: #ffffff;
    border-style: solid;
    border-width: 1px;
    border-color: rgb(207,207,207);
    width: 12px;
    margin: -5px 0;
    border-radius: 7px;
}
QSlider::handle:vertical {
    background: #ffffff;
    border-style: solid;
    border-width: 1px;
    border-color: rgb(207,207,207);
    height: 12px;
    margin: 0 -5px;
    border-radius: 7px;
}
QSlider::add-page, QSlider::sub-page {
    border: 1px transparent;
    background-color: #52595d;
    border-radius: 4px;
}
QSlider::add-page:horizontal {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #ddd5d5, stop:0.5 #dad3d3, stop:1 #ddd5d5);
}
QSlider::sub-page:horizontal {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #467dd1, stop:0.5 #3b88fc, stop:1 #467dd1);
}
QSlider::add-page:vertical {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #467dd1, stop:0.5 #3b88fc, stop:1 #467dd1);
}
QSlider::sub-page:vertical {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #ddd5d5, stop:0.5 #dad3d3, stop:1 #ddd5d5);
}
QSlider::add-page:horizontal:disabled, QSlider::sub-page:horizontal:disabled, QSlider::add-page:vertical:disabled, QSlider::sub-page:vertical:disabled {
    background: #b9b9b9;
}
QComboBox, QFontComboBox {
    border-width: 2px;
    border-radius: 8px;
    border-style: solid;
    border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);
    border-right-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);
    border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #c1c9cf, stop:1 #d2d8dd);
    border-left-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);
    background-color: #f4f4f4;
    color: #272727;
    padding-left: 5px;
}
QComboBox:editable, QComboBox:!editable, QComboBox::drop-down:editable, QComboBox:!editable:on, QComboBox::drop-down:editable:on {
    background: #ffffff;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;
    color: #272727;
    border-left-width: 1px;
    border-left-color: darkgray;
    border-left-style: solid;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
}
QComboBox::down-arrow {
    image: url(/usr/share/icons/Adwaita/16x16/actions/go-down-symbolic.symbolic.png); /*Adawaita icon thene*/
}

QComboBox::down-arrow:on {
    top: 1px;
    left: 1px;
}
QComboBox QAbstractItemView {
    border: 1px solid darkgray;
    border-radius: 8px;
    selection-background-color: #dadada;
    selection-color: #272727;
    color: #272727;
    background: white;
}
QLabel, QCheckBox, QRadioButton {
    color: #272727;
}
QCheckBox {
    padding: 2px;
}
QCheckBox:disabled, QRadioButton:disabled {
    color: #808086;
    padding: 2px;
}

QCheckBox:hover {
    border-radius:4px;
    border-style:solid;
    padding-left: 1px;
    padding-right: 1px;
    padding-bottom: 1px;
    padding-top: 1px;
    border-width:1px;
    border-color: transparent;
}
QCheckBox::indicator:checked {
    image: url(/usr/share/icons/Adwaita/16x16/actions/object-select-symbolic.symbolic.png);
    height: 15px;
    width: 15px;
    border-style:solid;
    border-width: 1px;
    border-color: #48a5fd;
    color: #ffffff;
    border-radius: 3px;
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #48a5fd, stop:0.5 #329cfb, stop:1 #48a5fd);
}
QCheckBox::indicator:unchecked {
    
    height: 15px;
    width: 15px;
    border-style:solid;
    border-width: 1px;
    border-color: #48a5fd;
    border-radius: 3px;
    background-color: #fbfdfa;
}
QLCDNumber {
    color: #616161;;
}
QMenuBar {
    background-color: #ececec;
}
QMenuBar::item {
    color: #616161;
    spacing: 3px;
    padding: 1px 4px;
    background-color: #ececec;
}

QMenuBar::item:selected {
    background-color: #dadada;
    color: #3d3d3d;
}
QMenu {
    background-color: #ececec;
}
QMenu::item:selected {
    background-color: #dadada;
    color: #3d3d3d;
}
QMenu::item {
    color: #616161;;
    background-color: #e0e0e0;
}
QTabWidget {
    color:rgb(0,0,0);
    background-color:#000000;
}
QTabWidget::pane {
    border-color: #050a0e;
    background-color: #e0e0e0;
    border-width: 1px;
    border-radius: 4px;
    position: absolute;
    top: -0.5em;
    padding-top: 0.5em;
}

QTabWidget::tab-bar {
    alignment: center;
}

QTabBar::tab {
    border-bottom: 1px solid #c0c0c0;
    padding: 3px;
    color: #272727;
    background-color: #fefefc;
    margin-left:0px;
}
QTabBar::tab:!last {
    border-right: 1px solid;
    border-right-color: #c0c0c0;
    border-bottom-color: #c0c0c0;
}
QTabBar::tab:first {
    border-top-left-radius: 4px;
    border-bottom-left-radius: 4px;
}
QTabBar::tab:last {
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
}
QTabBar::tab:selected, QTabBar::tab:last:selected, QTabBar::tab:hover {
    color: #FFFFFF;
    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #84afe5, stop:1 #1168e4);
}
QRadioButton::indicator {
    height: 14px;
    width: 14px;
    border-style:solid;
    border-radius:7px;
    border-width: 1px;
}
QRadioButton::indicator:checked {
    border-color: #48a5fd;
    background-color: qradialgradient(cx:0.5, cy:0.5, radius:0.4,fx:0.5, fy:0.5, stop:0 #ffffff, stop:0.5 #ffffff, stop:0.6 #48a5fd, stop:1 #48a5fd);
}
QRadioButton::indicator:!checked {
    border-color: #a9b7c6;
    background-color: #fbfdfa;
}
QStatusBar {
    color:#027f7f;
}

QDial {
    background: #16a085;
}

QToolBox {
    color: #a9b7c6;
    background-color: #222b2e;
}
QToolBox::tab {
    color: #a9b7c6;
    background-color:#222b2e;
}
QToolBox::tab:selected {
    color: #FFFFFF;
    background-color:#222b2e;
}
QScrollArea {
    color: #FFFFFF;
    background-color:#222b2e;
}

QScrollBar:horizontal {
	max-height: 10px;
	border: 1px transparent grey;
	margin: 0px 20px 0px 20px;
	background: transparent;
}
QScrollBar:vertical {
	max-width: 10px;
	border: 1px transparent grey;
	margin: 20px 0px 20px 0px;
	background: transparent;
}
QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
	background: #52595d;
	border-style: transparent;
	border-radius: 4px;
	min-height: 25px;
}
QScrollBar::handle:horizontal:hover, QScrollBar::handle:vertical:hover {
	background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #467dd1, stop:0.5 #3b88fc, stop:1 #467dd1);
}
QScrollBar::add-line, QScrollBar::sub-line {
    border: 2px transparent grey;
    border-radius: 4px;
    subcontrol-origin: margin;
    background: #b9b9b9;
}
QScrollBar::add-line:horizontal {
    width: 20px;
    subcontrol-position: right;
}
QScrollBar::add-line:vertical {
    height: 20px;
    subcontrol-position: bottom;
}
QScrollBar::sub-line:horizontal {
    width: 20px;
    subcontrol-position: left;
}
QScrollBar::sub-line:vertical {
    height: 20px;
    subcontrol-position: top;
}
QScrollBar::add-line:vertical:pressed, QScrollBar::add-line:horizontal:pressed, QScrollBar::sub-line:horizontal:pressed, QScrollBar::sub-line:vertical:pressed {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #467dd1, stop:0.5 #3b88fc, stop:1 #467dd1);
}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal, QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
QScrollBar::up-arrow:vertical {
    image: url(/usr/share/icons/Adwaita/16x16/actions/go-up-symbolic.symbolic.png);
}
QScrollBar::down-arrow:vertical {
    image: url(/usr/share/icons/Adwaita/16x16/actions/go-down-symbolic.symbolic.png);
}
QScrollBar::left-arrow:horizontal {
    image: url(/usr/share/icons/Adwaita/16x16/actions/go-previous-symbolic.symbolic.png);
}
QScrollBar::right-arrow:horizontal {
    image: url(/usr/share/icons/Adwaita/16x16/actions/go-next-symbolic.symbolic.png);
}

"""


 
COMBINEAR = """
QWidget
{
	background-color: #3a3a3a;
	color: #fff;
	selection-background-color: #b78620;
	selection-color: #000;

}


/*-----QLabel-----*/
QLabel
{
	background-color: transparent;
	color: #fff;

}


/*-----QMenuBar-----*/
QMenuBar 
{
	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 57, 57, 255),stop:1 rgba(50, 50, 50, 255));
	border: 1px solid #000;
	color: #fff;

}


QMenuBar::item 
{
	background-color: transparent;

}


QMenuBar::item:selected 
{
	background-color: rgba(183, 134, 32, 20%);
	border: 1px solid #b78620;
	color: #fff;

}


QMenuBar::item:pressed 
{
	background-color: rgb(183, 134, 32);
	border: 1px solid #b78620;
	color: #fff;

}


/*-----QMenu-----*/
QMenu
{
    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 57, 57, 255),stop:1 rgba(50, 50, 50, 255));
    border: 1px solid #222;
    padding: 4px;
	color: #fff;

}


QMenu::item
{
    background-color: transparent;
    padding: 2px 20px 2px 20px;

}


QMenu::separator
{
   	background-color: rgb(183, 134, 32);
	height: 1px;

}


QMenu::item:disabled
{
    color: #555;
    background-color: transparent;
    padding: 2px 20px 2px 20px;

}


QMenu::item:selected
{
	background-color: rgba(183, 134, 32, 20%);
	border: 1px solid #b78620;
	color: #fff;

}


/*-----QToolBar-----*/
QToolBar
{
	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(69, 69, 69, 255),stop:1 rgba(58, 58, 58, 255));
	border-top: none;
	border-bottom: 1px solid #4f4f4f;
	border-left: 1px solid #4f4f4f;
	border-right: 1px solid #4f4f4f;

}


QToolBar::separator
{
	background-color: #2e2e2e;
	width: 1px;

}


/*-----QToolButton-----*/
QToolButton 
{
	background-color: transparent;
	color: #fff;
	padding: 5px;
	padding-left: 8px;
	padding-right: 8px;
	margin-left: 1px;
}


QToolButton:hover
{
	background-color: rgba(183, 134, 32, 20%);
	border: 1px solid #b78620;
	color: #fff;
	
}


QToolButton:pressed
{
	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 57, 57, 255),stop:1 rgba(50, 50, 50, 255));
	border: 1px solid #b78620;

}


QToolButton:checked
{
	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 57, 57, 255),stop:1 rgba(50, 50, 50, 255));
	border: 1px solid #222;
}


/*-----QPushButton-----*/
QPushButton
{
	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(84, 84, 84, 255),stop:1 rgba(59, 59, 59, 255));
	color: #ffffff;
	min-width: 80px;
	border-style: solid;
	border-width: 1px;
	border-radius: 3px;
	border-color: #051a39;
	padding: 5px;

}


QPushButton::flat
{
	background-color: transparent;
	border: none;
	color: #fff;

}


QPushButton::disabled
{
	background-color: #404040;
	color: #656565;
	border-color: #051a39;

}


QPushButton::hover
{
	background-color: rgba(183, 134, 32, 20%);
	border: 1px solid #b78620;

}


QPushButton::pressed
{
	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(74, 74, 74, 255),stop:1 rgba(49, 49, 49, 255));
	border: 1px solid #b78620;

}


QPushButton::checked
{
	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(74, 74, 74, 255),stop:1 rgba(49, 49, 49, 255));
	border: 1px solid #222;

}


/*-----QLineEdit-----*/
QLineEdit
{
	background-color: #131313;
	color : #eee;
	border: 1px solid #343434;
	border-radius: 2px;
	padding: 3px;
	padding-left: 5px;

}


/*-----QPlainTExtEdit-----*/
QPlainTextEdit
{
	background-color: #131313;
	color : #eee;
	border: 1px solid #343434;
	border-radius: 2px;
	padding: 3px;
	padding-left: 5px;

}


/*-----QTabBar-----*/
QTabBar::tab
{
	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(84, 84, 84, 255),stop:1 rgba(59, 59, 59, 255));
	color: #ffffff;
	border-style: solid;
	border-width: 1px;
	border-color: #666;
	border-bottom: none;
	padding: 5px;
	padding-left: 15px;
	padding-right: 15px;

}


QTabWidget::pane 
{
	background-color: red;
	border: 1px solid #666;
	top: 1px;

}


QTabBar::tab:last
{
	margin-right: 0; 

}


QTabBar::tab:first:!selected
{
	background-color: #0c0c0d;
	margin-left: 0px;

}


QTabBar::tab:!selected
{
	color: #b1b1b1;
	border-bottom-style: solid;
	background-color: #0c0c0d;

}


QTabBar::tab:selected
{
	margin-bottom: 0px;

}


QTabBar::tab:!selected:hover
{
	border-top-color: #b78620;

}


/*-----QComboBox-----*/
QComboBox
{
    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(84, 84, 84, 255),stop:1 rgba(59, 59, 59, 255));
    border: 1px solid #000;
    padding-left: 6px;
    color: #ffffff;
    height: 20px;

}


QComboBox::disabled
{
	background-color: #404040;
	color: #656565;
	border-color: #051a39;

}


QComboBox:on
{
    background-color: #b78620;
	color: #000;

}


QComboBox QAbstractItemView
{
    background-color: #383838;
    color: #ffffff;
    border: 1px solid black;
    selection-background-color: #b78620;
    outline: 0;

}


QComboBox::drop-down
{
	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 57, 57, 255),stop:1 rgba(50, 50, 50, 255));
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;
    border-left-width: 1px;
    border-left-color: black;
    border-left-style: solid; 

}


QComboBox::down-arrow
{
    image: url(://arrow-down.png);
    width: 8px;
    height: 8px;
}


/*-----QSpinBox & QDateTimeEdit-----*/
QSpinBox,
QDateTimeEdit 
{
    background-color: #131313;
	color : #eee;
	border: 1px solid #343434;
	padding: 3px;
	padding-left: 5px;
    border-radius : 2px;

}


QSpinBox::up-button, 
QDateTimeEdit::up-button
{
	border-top-right-radius:2px;
	background-color: #777777;
    width: 16px; 
    border-width: 1px;

}


QSpinBox::up-button:hover, 
QDateTimeEdit::up-button:hover
{
	background-color: #585858;

}


QSpinBox::up-button:pressed, 
QDateTimeEdit::up-button:pressed
{
	background-color: #252525;
    width: 16px; 
    border-width: 1px;

}


QSpinBox::up-arrow,
QDateTimeEdit::up-arrow
{
    image: url(://arrow-up.png);
    width: 7px;
    height: 7px;

}


QSpinBox::down-button, 
QDateTimeEdit::down-button
{
	border-bottom-right-radius:2px;
	background-color: #777777;
    width: 16px; 
    border-width: 1px;

}


QSpinBox::down-button:hover, 
QDateTimeEdit::down-button:hover
{
	background-color: #585858;

}


QSpinBox::down-button:pressed, 
QDateTimeEdit::down-button:pressed
{
	background-color: #252525;
    width: 16px; 
    border-width: 1px;

}


QSpinBox::down-arrow,
QDateTimeEdit::down-arrow
{
    image: url(://arrow-down.png);
    width: 7px;
    height: 7px;

}


/*-----QGroupBox-----*/
QGroupBox 
{
    border: 1px solid;
    border-color: #666666;
	border-radius: 5px;
    margin-top: 20px;

}


QGroupBox::title  
{
    background-color: transparent;
    color: #eee;
    subcontrol-origin: margin;
    padding: 5px;
	border-top-left-radius: 3px;
	border-top-right-radius: 3px;

}


/*-----QHeaderView-----*/
QHeaderView::section
{
    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(60, 60, 60, 255),stop:1 rgba(50, 50, 50, 255));
	border: 1px solid #000;
    color: #fff;
    text-align: left;
	padding: 4px;
	
}


QHeaderView::section:disabled
{
    background-color: #525251;
    color: #656565;

}


QHeaderView::section:checked
{
    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(60, 60, 60, 255),stop:1 rgba(50, 50, 50, 255));
    color: #fff;

}


QHeaderView::section::vertical::first,
QHeaderView::section::vertical::only-one
{
    border-top: 1px solid #353635;

}


QHeaderView::section::vertical
{
    border-top: 1px solid #353635;

}


QHeaderView::section::horizontal::first,
QHeaderView::section::horizontal::only-one
{
    border-left: 1px solid #353635;

}


QHeaderView::section::horizontal
{
    border-left: 1px solid #353635;

}


QTableCornerButton::section
{
    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(60, 60, 60, 255),stop:1 rgba(50, 50, 50, 255));
	border: 1px solid #000;
    color: #fff;

}


/*-----QTreeWidget-----*/
QTreeView
{
	show-decoration-selected: 1;
	alternate-background-color: #3a3a3a;
	selection-color: #fff;
	background-color: #2d2d2d;
	border: 1px solid gray;
	padding-top : 5px;
	color: #fff;
	font: 8pt;

}


QTreeView::item:selected
{
	color:#fff;
	background-color: #b78620;
	border-radius: 0px;

}


QTreeView::item:!selected:hover
{
    background-color: #262626;
    border: none;
    color: white;

}


QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings 
{
	image: url(://tree-closed.png);

}


QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings  
{
	image: url(://tree-open.png);

}


/*-----QListView-----*/
QListView 
{
	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(83, 83, 83, 255),stop:0.293269 rgba(81, 81, 81, 255),stop:0.634615 rgba(79, 79, 79, 255),stop:1 rgba(83, 83, 83, 255));
    border : none;
    color: white;
    show-decoration-selected: 1; 
    outline: 0;
	border: 1px solid gray;

}


QListView::disabled 
{
	background-color: #656565;
	color: #1b1b1b;
    border: 1px solid #656565;

}


QListView::item 
{
	background-color: #2d2d2d;
    padding: 1px;

}


QListView::item:alternate 
{
    background-color: #3a3a3a;

}


QListView::item:selected 
{
	background-color: #b78620;
	border: 1px solid #b78620;
	color: #fff;

}


QListView::item:selected:!active 
{
	background-color: #b78620;
	border: 1px solid #b78620;
	color: #fff;

}


QListView::item:selected:active 
{
	background-color: #b78620;
	border: 1px solid #b78620;
	color: #fff;

}


QListView::item:hover {
    background-color: #262626;
    border: none;
    color: white;

}


/*-----QCheckBox-----*/
QCheckBox
{
	background-color: transparent;
    color: lightgray;
	border: none;

}


QCheckBox::indicator
{
    background-color: #323232;
    border: 1px solid darkgray;
    width: 12px;
    height: 12px;

}


QCheckBox::indicator:checked
{
    image:url("./ressources/check.png");
	background-color: #b78620;
    border: 1px solid #3a546e;

}


QCheckBox::indicator:unchecked:hover
{
	border: 1px solid #b78620; 

}


QCheckBox::disabled
{
	color: #656565;

}


QCheckBox::indicator:disabled
{
	background-color: #656565;
	color: #656565;
    border: 1px solid #656565;

}


/*-----QRadioButton-----*/
QRadioButton 
{
	color: lightgray;
	background-color: transparent;

}


QRadioButton::indicator::unchecked:hover 
{
	background-color: lightgray;
	border: 2px solid #b78620;
	border-radius: 6px;
}


QRadioButton::indicator::checked 
{
	border: 2px solid #b78620;
	border-radius: 6px;
	background-color: rgba(183,134,32,20%);  
	width: 9px; 
	height: 9px; 

}


/*-----QSlider-----*/
QSlider::groove:horizontal 
{
	background-color: transparent;
	height: 3px;

}


QSlider::sub-page:horizontal 
{
	background-color: #b78620;

}


QSlider::add-page:horizontal 
{
	background-color: #131313;

}


QSlider::handle:horizontal 
{
	background-color: #b78620;
	width: 14px;
	margin-top: -6px;
	margin-bottom: -6px;
	border-radius: 6px;

}


QSlider::handle:horizontal:hover 
{
	background-color: #d89e25;
	border-radius: 6px;

}


QSlider::sub-page:horizontal:disabled 
{
	background-color: #bbb;
	border-color: #999;

}


QSlider::add-page:horizontal:disabled 
{
	background-color: #eee;
	border-color: #999;

}


QSlider::handle:horizontal:disabled 
{
	background-color: #eee;
	border: 1px solid #aaa;
	border-radius: 3px;

}


/*-----QScrollBar-----*/
QScrollBar:horizontal
{
    border: 1px solid #222222;
    background-color: #3d3d3d;
    height: 15px;
    margin: 0px 16px 0 16px;

}


QScrollBar::handle:horizontal
{
	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(97, 97, 97, 255),stop:1 rgba(90, 90, 90, 255));
	border: 1px solid #2d2d2d;
    min-height: 20px;

}


QScrollBar::add-line:horizontal
{
	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(97, 97, 97, 255),stop:1 rgba(90, 90, 90, 255));
	border: 1px solid #2d2d2d;
    width: 15px;
    subcontrol-position: right;
    subcontrol-origin: margin;

}


QScrollBar::sub-line:horizontal
{
	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(97, 97, 97, 255),stop:1 rgba(90, 90, 90, 255));
	border: 1px solid #2d2d2d;
    width: 15px;
    subcontrol-position: left;
    subcontrol-origin: margin;

}


QScrollBar::right-arrow:horizontal
{
    image: url(://arrow-right.png);
    width: 6px;
    height: 6px;

}


QScrollBar::left-arrow:horizontal
{
    image: url(://arrow-left.png);
    width: 6px;
    height: 6px;

}


QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
{
    background: none;

}


QScrollBar:vertical
{
    background-color: #3d3d3d;
    width: 16px;
	border: 1px solid #2d2d2d;
    margin: 16px 0px 16px 0px;

}


QScrollBar::handle:vertical
{
    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(97, 97, 97, 255),stop:1 rgba(90, 90, 90, 255));
	border: 1px solid #2d2d2d;
    min-height: 20px;

}


QScrollBar::add-line:vertical
{
	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(97, 97, 97, 255),stop:1 rgba(90, 90, 90, 255));
	border: 1px solid #2d2d2d;
    height: 15px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;

}


QScrollBar::sub-line:vertical
{
	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(97, 97, 97, 255),stop:1 rgba(90, 90, 90, 255));
	border: 1px solid #2d2d2d;
    height: 15px;
    subcontrol-position: top;
    subcontrol-origin: margin;

}


QScrollBar::up-arrow:vertical
{
    image: url(://arrow-up.png);
    width: 6px;
    height: 6px;

}


QScrollBar::down-arrow:vertical
{
    image: url(://arrow-down.png);
    width: 6px;
    height: 6px;

}


QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
{
    background: none;

}


/*-----QProgressBar-----*/
QProgressBar
{
    border: 1px solid #666666;
    text-align: center;
	color: #000;
	font-weight: bold;

}


QProgressBar::chunk
{
    background-color: #b78620;
    width: 30px;
    margin: 0.5px;

}

"""

 
 
FIBERS= """
QWidget
{
	background-color: #8f1e28;
	color: #fff;
	selection-background-color: #aa7e82;
	selection-color: #000;

}


/*-----QLabel-----*/
QLabel
{
	background-color: transparent;
	color: #fff;

}


/*-----QMenuBar-----*/
QMenuBar 
{
	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(70, 70, 70, 255),stop:1 rgba(3, 2, 5, 255));
	color: #fff;

}


QMenuBar::item 
{
	background-color: transparent;
	border-left: 1px solid gray;
	padding: 5px;
	padding-left: 15px;
	padding-right: 15px;

}


QMenuBar::item:selected 
{
	background-color: #af272e;
	border: 1px solid #8f1e28;
	color: #fff;

}


QMenuBar::item:pressed 
{
	background-color: #6e181c;
	border: 1px solid #6e181c;
	color: #fff;

}


/*-----QMenu-----*/
QMenu
{
    background-color: #e8d9d7;
    border: 1px solid #4a5157;
	color: #000;

}


QMenu::item
{
    background-color: transparent;
    padding: 2px 20px 2px 20px;
	min-width: 100px;

}


QMenu::separator
{
   	background-color: #6e181c;
	height: 1px;

}


QMenu::item:disabled
{
    color: #555;
    background-color: transparent;
    padding: 2px 20px 2px 20px;

}


QMenu::item:selected
{
	background-color: #ab7f83;
	border: 1px solid #ab7f83;
	color: #fff;

}


/*-----QPushButton-----*/
QPushButton
{
	background-color: #6384ff;
	color: #fff;
	border: none;
	min-width: 80px;
	padding: 5px;

}


QPushButton::flat
{
	background-color: transparent;
	border: none;
	color: #000;

}


QPushButton::disabled
{
	background-color: #606060;
	color: #959595;
	border: none;

}


QPushButton::hover
{
	background-color: #718fff;
	border: 1px solid #718fff;

}


QPushButton::pressed
{
	background-color: #446cff;
	border: 1px solid #446cff;

}


QPushButton::checked
{
	background-color: #3761ff;
	border: 1px solid #3761ff;

}


/*-----QLineEdit-----*/
QLineEdit
{
	background-color: #e8d9d7;
	color : #000;
	border: 1px solid #1d1d1d;
	padding: 3px;
	padding-left: 5px;

}


/*-----QPlainTExtEdit-----*/
QPlainTextEdit
{
	background-color: #e8d9d7;
	color : #000;
	border: 1px solid #1d1d1d;
	padding: 3px;
	padding-left: 5px;

}


/*-----QToolBox-----*/
QToolBox
{
	background-color: transparent;
	border: 1px solid #410d12;

}


QToolBox::tab
{
	background-color: #640000;
	border: 1px solid #640000;

}


QToolBox::tab:hover
{
	background-color: #640000;
	border: 1px solid #1d1d1d;

}


/*-----QComboBox-----*/
QComboBox
{
    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(70, 70, 70, 255),stop:1 rgba(3, 2, 5, 255));
    padding-left: 6px;
	border: 1px solid #1d1d1d;
    color: #fff;
    height: 20px;

}


QComboBox::disabled
{
	background-color: #404040;
	color: #656565;
	border-color: #051a39;

}


QComboBox:on
{
    background-color: #4a5157;
	color: #fff;

}


QComboBox QAbstractItemView
{
    background-color: #e8d9d7;
    color: #000;
    selection-background-color: #aa7e82;
	selection-color: #fff;
    outline: 0;

}


QComboBox::drop-down
{
	background-color: #4a5157;
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;

}


QComboBox::down-arrow
{
    image: url(://arrow-down.png);
    width: 8px;
    height: 8px;

}


/*-----QDoubleSpinBox & QCalendarWidget-----*/
QDoubleSpinBox,
QCalendarWidget QSpinBox 
{
	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(70, 70, 70, 255),stop:1 rgba(3, 2, 5, 255));
	color : #fff;
	border: 1px solid #1d1d1d;
	padding: 3px;
	padding-left: 5px;

}


QDoubleSpinBox::up-button, 
QCalendarWidget QSpinBox::up-button
{
	background-color: #4a5157;
    width: 16px; 
    border-width: 1px;
	border-color: #1d1d1d;

}


QDoubleSpinBox::up-button:hover, 
QCalendarWidget QSpinBox::up-button:hover
{
	background-color: #585858;

}


QDoubleSpinBox::up-button:pressed, 
QCalendarWidget QSpinBox::up-button:pressed
{
	background-color: #252525;
    width: 16px; 
    border-width: 1px;

}


QDoubleSpinBox::up-arrow,
QCalendarWidget QSpinBox::up-arrow
{
    image: url(://arrow-up.png);
    width: 7px;
    height: 7px;

}


QDoubleSpinBox::down-button, 
QCalendarWidget QSpinBox::down-button
{
	background-color: #4a5157;
    width: 16px; 
    border-width: 1px;
	border-color: #1d1d1d;

}


QDoubleSpinBox::down-button:hover, 
QCalendarWidget QSpinBox::down-button:hover
{
	background-color: #585858;

}


QDoubleSpinBox::down-button:pressed, 
QCalendarWidget QSpinBox::down-button:pressed
{
	background-color: #252525;
    width: 16px; 
    border-width: 1px;

}


QDoubleSpinBox::down-arrow,
QCalendarWidget QSpinBox::down-arrow
{
    image: url(://arrow-down.png);
    width: 7px;
    height: 7px;

}


/*-----QGroupBox-----*/
QGroupBox 
{
	background-color: #640000;
    border: 1px solid;
    border-color: #410d12;
    margin-top: 23px;

}


QGroupBox::title  
{
    background-color: #640000;
    color: #fff;
	subcontrol-position: top left;
    subcontrol-origin: margin;
    padding: 5px;
	min-width: 100px;
	border: 1px solid #410d12;
	border-bottom: none;

}


/*-----QHeaderView-----*/
QHeaderView::section
{
    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(70, 70, 70, 255),stop:1 rgba(3, 2, 5, 255));
	border-top: 0px solid gray;
	border-bottom: 0px solid gray;
	border-right: 1px solid gray;
	border-left: 0px solid gray;
    color: #fff;
	padding: 4px;
	
}


QHeaderView::section:disabled
{
    background-color: #525251;
    color: #656565;

}


QHeaderView::section::vertical::first,
QHeaderView::section::vertical::only-one
{
    border-left: 1px solid #003333;

}


QHeaderView::section::vertical
{
    border-left: 1px solid #003333;
}


QHeaderView::section::horizontal::first,
QHeaderView::section::horizontal::only-one
{
    border-left: 1px solid #003333;

}


QHeaderView::section::horizontal
{
    border-left: 1px solid #003333;

}


/*-----QCalendarWidget-----*/
QCalendarWidget QMenu 
{
	width: 100px;
	left: 20px;
	color: #fff;

}


QCalendarWidget QWidget 
{ 
	alternate-background-color: #1d1d1d; 
	border: 1px solid #410d12;
	color: #000;

}


QCalendarWidget QAbstractItemView:enabled 
{
	color: #fff;  
	background-color: #1d1d1d;
	selection-background-color: #8f1e28; 
	selection-color: #fff; 

}


QCalendarWidget QAbstractItemView:disabled 
{ 
	color: #404040; 

}


/*-----QTreeWidget-----*/
QTreeView
{
	show-decoration-selected: 0;
	alternate-background-color: transparent;
	background-color: #e8d9d7;
   	border: 1px solid #410d12;
	color: #000;
	font: 8pt;

}


QTreeView::item:selected
{
	color:#fff;
	background-color: #af272e;
	border-radius: 0px;

}


QTreeView::item:!selected:hover
{
    background-color: #ab7f83;
    border: none;
    color: white;

}


QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings 
{
	image: url(://tree-closed.png);

}


QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings  
{
	image: url(://tree-open.png);

}


/*-----QListView-----*/
QListView 
{
	background-color: #e8d9d7;
	alternate-background-color: transparent;
    border : none;
    color: #000;
    show-decoration-selected: 1; 
    outline: 0;
   	border: 1px solid #410d12;

}


QListView::disabled 
{
	background-color: #656565;
	color: #1b1b1b;
    border: 1px solid #656565;

}


QListView::item 
{
	background-color: transparent;
    padding: 1px;

}


QListView::item:selected 
{
	background-color: #af272e;
	border: 1px solid #af272e;
	color: #fff;

}


QListView::item:selected:!active 
{
	background-color: #af272e;
	border: 1px solid #af272e;
	color: #fff;

}


QListView::item:selected:active 
{
	background-color: #af272e;
	border: 1px solid #af272e;
	color: #fff;

}


QListView::item:hover {
    background-color: #ab7f83;
    border: none;
    color: #000;

}


/*-----QCheckBox-----*/
QCheckBox
{
	background-color: transparent;
    color: #fff;
	border: none;

}


QCheckBox::indicator
{
    background-color: lightgray;
    border: 1px solid #000;
    width: 12px;
    height: 12px;

}


QCheckBox::indicator:checked
{
    image:url("./ressources/check.png");
	background-color: #cd70ff;
    border: 1px solid #3a546e;

}


QCheckBox::indicator:unchecked:hover
{
	border: 1px solid #46a2da; 

}


QCheckBox::disabled
{
	color: #656565;

}


QCheckBox::indicator:disabled
{
	background-color: #656565;
	color: #656565;
    border: 1px solid #656565;

}


/*-----QRadioButton-----*/
QRadioButton 
{
	color: #fff;
	background-color: transparent;

}


QRadioButton::indicator::unchecked:hover 
{
	background-color: #d3d3d3;
	border: 2px solid #462657;
	border-radius: 6px;
}


QRadioButton::indicator::checked 
{
	border: 2px solid #462657;
	border-radius: 6px;
	background-color: #cd70ff;  
	width: 9px; 
	height: 9px; 

}


/*-----QScrollBar-----*/
QScrollBar:vertical 
{
   border: none;
   width: 12px;

}


QScrollBar::handle:vertical 
{
   border: none;
   background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(70, 70, 70, 255),stop:1 rgba(3, 2, 5, 255));
   min-height: 80px;
   width : 12px;

}


QScrollBar::handle:vertical:pressed
{
   background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(102, 40, 40, 255),stop:0.480769 rgba(64, 19, 19, 255),stop:1 rgba(58, 0, 0, 255));

}


QScrollBar::add-line:vertical
{
   border: none;
   background: transparent;
   height: 0px;
   subcontrol-position: bottom;
   subcontrol-origin: margin;

}


QScrollBar::add-line:vertical:hover 
{
   background-color: transparent;

}


QScrollBar::add-line:vertical:pressed 
{
   background-color: #3f3f3f;

}


QScrollBar::sub-line:vertical
{
   border: none;
   background: transparent;
   height: 0px;

}


QScrollBar::sub-line:vertical:hover 
{
   background-color: transparent;

}


QScrollBar::sub-line:vertical:pressed 
{
   background-color: #3f3f3f;

}


QScrollBar::up-arrow:vertical
{
   width: 0px;
   height: 0px;
   background: transparent;

}


QScrollBar::down-arrow:vertical 
{
   width: 0px;
   height: 0px;
   background: transparent;

}


QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
{
   background-color: #e8d9d7;
	
}


QScrollBar:horizontal 
{
   border: none;
   height: 12px;

}


QScrollBar::handle:horizontal 
{
   border: none;
   border-radius : 0px;
   background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(70, 70, 70, 255),stop:1 rgba(3, 2, 5, 255));
   min-height: 80px;
   height : 12px;

}


QScrollBar::handle:horizontal:pressed
{
   background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(102, 40, 40, 255),stop:0.480769 rgba(64, 19, 19, 255),stop:1 rgba(58, 0, 0, 255)); 

}


QScrollBar::add-line:horizontal
{
   border: none;
   background: transparent;
   height: 0px;
   subcontrol-position: bottom;
   subcontrol-origin: margin;

}


QScrollBar::add-line:horizontal:hover 
{
   background-color: transparent;

}


QScrollBar::add-line:horizontal:pressed 
{
   background-color: #3f3f3f;

}


QScrollBar::sub-line:horizontal
{
   border: none;
   background: transparent;
   height: 0px;

}


QScrollBar::sub-line:horizontal:hover 
{
   background-color: transparent;

}


QScrollBar::sub-line:horizontal:pressed 
{
   background-color: #3f3f3f;

}


QScrollBar::up-arrow:horizontal
{
   width: 0px;
   height: 0px;
   background: transparent;

}


QScrollBar::down-arrow:horizontal 
{
   width: 0px;
   height: 0px;
   background: transparent;

}


QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
{
   background-color: #e8d9d7;
	
}


/*-----QProgressBar-----*/
QProgressBar
{
	border: 1px solid #410d12;
    text-align: center;
	color: #000;
	font-weight: bold;

}


QProgressBar::chunk
{
    background-color: #cd70ff;
    margin: 0.5px;

}

 
QStatusBar
{
	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(70, 70, 70, 255),stop:1 rgba(3, 2, 5, 255));
	color: #ffffff;
	border-color: #051a39;

}

 
QSizeGrip 
{
	background-color: image("./ressources/sizegrip.png"); 
	border: none;

}
""" 
MATERIAL_DARK = """
QMainWindow {
	background-color:#1e1d23;
}
QDialog {
	background-color:#1e1d23;
}
QColorDialog {
	background-color:#1e1d23;
}
QTextEdit {
	background-color:#1e1d23;
	color: #a9b7c6;
}
QPlainTextEdit {
	selection-background-color:#007b50;
	background-color:#1e1d23;
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: transparent;
	border-width: 1px;
	color: #a9b7c6;
}
QPushButton{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: transparent;
	border-width: 1px;
	border-style: solid;
	color: #a9b7c6;
	padding: 2px;
	background-color: #1e1d23;
}
QPushButton::default{
	border-style: inset;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #04b97f;
	border-width: 1px;
	color: #a9b7c6;
	padding: 2px;
	background-color: #1e1d23;
}
QToolButton {
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #04b97f;
	border-bottom-width: 1px;
	border-style: solid;
	color: #a9b7c6;
	padding: 2px;
	background-color: #1e1d23;
}
QToolButton:hover{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #37efba;
	border-bottom-width: 2px;
	border-style: solid;
	color: #FFFFFF;
	padding-bottom: 1px;
	background-color: #1e1d23;
}
QPushButton:hover{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #37efba;
	border-bottom-width: 1px;
	border-style: solid;
	color: #FFFFFF;
	padding-bottom: 2px;
	background-color: #1e1d23;
}
QPushButton:pressed{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #37efba;
	border-bottom-width: 2px;
	border-style: solid;
	color: #37efba;
	padding-bottom: 1px;
	background-color: #1e1d23;
}
QPushButton:disabled{
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #808086;
	border-bottom-width: 2px;
	border-style: solid;
	color: #808086;
	padding-bottom: 1px;
	background-color: #1e1d23;
}
QLineEdit {
	border-width: 1px; border-radius: 4px;
	border-color: rgb(58, 58, 58);
	border-style: inset;
	padding: 0 8px;
	color: #a9b7c6;
	background:#1e1d23;
	selection-background-color:#007b50;
	selection-color: #FFFFFF;
}
QLabel {
	color: #a9b7c6;
}
QLCDNumber {
	color: #37e6b4;
}
QProgressBar {
	text-align: center;
	color: rgb(240, 240, 240);
	border-width: 1px; 
	border-radius: 10px;
	border-color: rgb(58, 58, 58);
	border-style: inset;
	background-color:#1e1d23;
}
QProgressBar::chunk {
	background-color: #04b97f;
	border-radius: 5px;
}
QMenuBar {
	background-color: #1e1d23;
}
QMenuBar::item {
	color: #a9b7c6;
  	spacing: 3px;
  	padding: 1px 4px;
  	background: #1e1d23;
}

QMenuBar::item:selected {
  	background:#1e1d23;
	color: #FFFFFF;
}
QMenu::item:selected {
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: #04b97f;
	border-bottom-color: transparent;
	border-left-width: 2px;
	color: #FFFFFF;
	padding-left:15px;
	padding-top:4px;
	padding-bottom:4px;
	padding-right:7px;
	background-color: #1e1d23;
}
QMenu::item {
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: transparent;
	border-bottom-width: 1px;
	border-style: solid;
	color: #a9b7c6;
	padding-left:17px;
	padding-top:4px;
	padding-bottom:4px;
	padding-right:7px;
	background-color: #1e1d23;
}
QMenu{
	background-color:#1e1d23;
}
QTabWidget {
	color:rgb(0,0,0);
	background-color:#1e1d23;
}
QTabWidget::pane {
		border-color: rgb(77,77,77);
		background-color:#1e1d23;
		border-style: solid;
		border-width: 1px;
    	border-radius: 6px;
}
QTabBar::tab {
	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: transparent;
	border-bottom-width: 1px;
	border-style: solid;
	color: #808086;
	padding: 3px;
	margin-left:3px;
	background-color: #1e1d23;
}
QTabBar::tab:selected, QTabBar::tab:last:selected, QTabBar::tab:hover {
  	border-style: solid;
	border-top-color: transparent;
	border-right-color: transparent;
	border-left-color: transparent;
	border-bottom-color: #04b97f;
	border-bottom-width: 2px;
	border-style: solid;
	color: #FFFFFF;
	padding-left: 3px;
	padding-bottom: 2px;
	margin-left:3px;
	background-color: #1e1d23;
}

QCheckBox {
	color: #a9b7c6;
	padding: 2px;
}
QCheckBox:disabled {
	color: #808086;
	padding: 2px;
}

QCheckBox:hover {
	border-radius:4px;
	border-style:solid;
	padding-left: 1px;
	padding-right: 1px;
	padding-bottom: 1px;
	padding-top: 1px;
	border-width:1px;
	border-color: rgb(87, 97, 106);
	background-color:#1e1d23;
}
QCheckBox::indicator:checked {

	height: 10px;
	width: 10px;
	border-style:solid;
	border-width: 1px;
	border-color: #04b97f;
	color: #a9b7c6;
	background-color: #04b97f;
}
QCheckBox::indicator:unchecked {

	height: 10px;
	width: 10px;
	border-style:solid;
	border-width: 1px;
	border-color: #04b97f;
	color: #a9b7c6;
	background-color: transparent;
}
QRadioButton {
	color: #a9b7c6;
	background-color: #1e1d23;
	padding: 1px;
}
QRadioButton::indicator:checked {
	height: 10px;
	width: 10px;
	border-style:solid;
	border-radius:5px;
	border-width: 1px;
	border-color: #04b97f;
	color: #a9b7c6;
	background-color: #04b97f;
}
QRadioButton::indicator:!checked {
	height: 10px;
	width: 10px;
	border-style:solid;
	border-radius:5px;
	border-width: 1px;
	border-color: #04b97f;
	color: #a9b7c6;
	background-color: transparent;
}
QStatusBar {
	color:#027f7f;
}
QSpinBox {
	color: #a9b7c6;	
	background-color: #1e1d23;
}
QDoubleSpinBox {
	color: #a9b7c6;	
	background-color: #1e1d23;
}
QTimeEdit {
	color: #a9b7c6;	
	background-color: #1e1d23;
}
QDateTimeEdit {
	color: #a9b7c6;	
	background-color: #1e1d23;
}
QDateEdit {
	color: #a9b7c6;	
	background-color: #1e1d23;
}
QComboBox {
	color: #a9b7c6;	
	background: #1e1d23;
}
QComboBox:editable {
	background: #1e1d23;
	color: #a9b7c6;
	selection-background-color: #1e1d23;
}
QComboBox QAbstractItemView {
	color: #a9b7c6;	
	background: #1e1d23;
	selection-color: #FFFFFF;
	selection-background-color: #1e1d23;
}
QComboBox:!editable:on, QComboBox::drop-down:editable:on {
	color: #a9b7c6;	
	background: #1e1d23;
}
QFontComboBox {
	color: #a9b7c6;	
	background-color: #1e1d23;
}
QToolBox {
	color: #a9b7c6;
	background-color: #1e1d23;
}
QToolBox::tab {
	color: #a9b7c6;
	background-color: #1e1d23;
}
QToolBox::tab:selected {
	color: #FFFFFF;
	background-color: #1e1d23;
}
QScrollArea {
	color: #FFFFFF;
	background-color: #1e1d23;
}
QSlider::groove:horizontal {
	height: 5px;
	background: #04b97f;
}
QSlider::groove:vertical {
	width: 5px;
	background: #04b97f;
}
QSlider::handle:horizontal {
	background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
	border: 1px solid #5c5c5c;
	width: 14px;
	margin: -5px 0;
	border-radius: 7px;
}
QSlider::handle:vertical {
	background: qlineargradient(x1:1, y1:1, x2:0, y2:0, stop:0 #b4b4b4, stop:1 #8f8f8f);
	border: 1px solid #5c5c5c;
	height: 14px;
	margin: 0 -5px;
	border-radius: 7px;
}
QSlider::add-page:horizontal {
    background: white;
}
QSlider::add-page:vertical {
    background: white;
}
QSlider::sub-page:horizontal {
    background: #04b97f;
}
QSlider::sub-page:vertical {
    background: #04b97f;
}
"""