import sys

from PyQt5 import QtGui
from PyQt5.QtCore import QTimer, QSize
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton, QGroupBox, QRadioButton, QButtonGroup, QCheckBox, \
    QStatusBar, QSlider, QWidget, QMainWindow

from app_controllers.controller import Controller
from app_controllers.utils.camera_helper import get_connected_camera_alias
from app_controllers.utils.update_helper import is_update
from app_views.threads.worker_thread_pause_screen import WorkerThreadPauseScreen
from app_views.threads.worker_thread_system_resource import WorkerThreadSystemResource

'''Class for creating the application app_views
'''


class View(QMainWindow):

    def __init__(self, model):
        super().__init__()
        # window properties
        self.gui_width = 935
        self.gui_height = 560
        # element x coordinate
        self.button_line_x = 15
        self.model = model
        self.setWindowTitle('Sitting Posture Detector [commit {} - {}]'.format(model.get_commit_hash(), is_update()))
        self.setGeometry(100, 100, self.gui_width, self.gui_height)
        self.setFixedSize(self.gui_width, self.gui_height)
        # centers the window
        Controller.center_window(self)
        # Set taskbar icon in Windows
        if sys.platform.startswith('win'):
            import ctypes
            # Specify app name
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(str(model.commit_hash))

        self.combobox_camera_list = QComboBox(self)
        self.combobox_camera_list.addItems(get_connected_camera_alias())
        self.combobox_camera_list.move(20, self.button_line_x)
        self.combobox_camera_list.setFixedWidth(200)
        self.combobox_camera_list.setFixedHeight(28)

        # QLabel properties
        self.label_stream = QLabel(self)
        self.label_stream.setStyleSheet('border: 2px solid #4269b9; background-color: black;')
        self.label_stream_width = 640
        self.label_stream_height = 480
        self.label_stream.setFixedWidth(self.label_stream_width)
        self.label_stream.setFixedHeight(self.label_stream_height)
        self.label_stream.move(20, 50)
        self.label_stream.setAlignment(Qt.AlignCenter)
        self.label_stream.setHidden(True)

        self.button_fullscreen = QPushButton('Fullscreen', self.label_stream)
        self.button_fullscreen.move(self.label_stream.width() - 90, self.label_stream.height() - 40)
        self.button_fullscreen.setFixedWidth(80)
        self.button_fullscreen.setFixedHeight(30)
        self.button_fullscreen.setToolTip('Enable/Disable fullscreen')

        # image label properties
        self.label_no_camera = QLabel(self)
        self.label_no_camera.setStyleSheet('border: 0px solid black')
        self.label_no_camera.setFixedWidth(self.label_stream_width)
        self.label_no_camera.setFixedHeight(self.label_stream_height)
        self.label_no_camera.move(20, 50)

        # start button properties
        self.button_start = QPushButton('Start', self)
        self.button_start.setFixedHeight(29)
        self.button_start.setFixedWidth(80)
        self.button_start.move(225, self.button_line_x)

        # stop button properties
        self.button_stop = QPushButton('Stop', self)
        self.button_stop.setFixedHeight(29)
        self.button_stop.setFixedWidth(80)
        self.button_stop.move(310, self.button_line_x)

        # refresh button properties
        self.button_refresh = QPushButton('Refresh', self)
        self.button_refresh.setToolTip('Refresh camera list')
        self.button_refresh.setFixedHeight(29)
        self.button_refresh.setFixedWidth(80)
        self.button_refresh.move(395, self.button_line_x)

        # groupbox properties
        self.groupbox_frame_options = QGroupBox(self)
        self.groupbox_frame_options.setTitle('General Options')
        self.groupbox_frame_options.setFixedHeight(self.label_stream_height)
        self.groupbox_frame_options.setFixedWidth(250)
        self.groupbox_frame_options.move(665, 50)

        # flip horizontal button
        self.button_flip_horizontal = QPushButton('H-Flip', self.groupbox_frame_options)
        self.button_flip_horizontal.move(10, 355)
        self.button_flip_horizontal.setToolTip('Flip image horizontal')
        self.button_flip_horizontal.setFixedWidth(60)
        self.button_flip_horizontal.setFixedHeight(28)

        # flip vertical button
        self.button_flip_vertical = QPushButton('V-Flip', self.groupbox_frame_options)
        self.button_flip_vertical.move(80, 355)
        self.button_flip_vertical.setToolTip('Flip image vertical')
        self.button_flip_vertical.setFixedWidth(60)
        self.button_flip_vertical.setFixedHeight(28)

        # rotate button
        self.button_rotate = QPushButton('Rotate', self.groupbox_frame_options)
        self.button_rotate.move(150, 355)
        self.button_rotate.setToolTip('Rotate image by 90 degrees')
        self.button_rotate.setFixedWidth(60)
        self.button_rotate.setFixedHeight(28)

        # radio buttons properties
        self.current_rb_selected = None
        self.button_group = QButtonGroup(self)
        self.radiobutton_bl = QRadioButton('Bottom-left', self.groupbox_frame_options)
        self.radiobutton_bl.move(10, 65)
        self.radiobutton_bl.setToolTip('Displays information in the bottom-left corner')
        self.radiobutton_br = QRadioButton('Bottom-right', self.groupbox_frame_options)
        self.radiobutton_br.move(110, 65)
        self.radiobutton_br.setToolTip('Displays information in the bottom-right corner')
        self.radiobutton_tl = QRadioButton('Top-left', self.groupbox_frame_options)
        self.radiobutton_tl.move(10, 30)
        self.radiobutton_tl.setToolTip('Displays information in the top-left corner')
        self.radiobutton_tr = QRadioButton('Top-right', self.groupbox_frame_options)
        self.radiobutton_tr.move(110, 30)
        self.radiobutton_tr.setToolTip('Displays information in the top-right corner')
        self.radiobutton_bl.setChecked(True)
        self.button_group.addButton(self.radiobutton_bl, 1)
        self.button_group.addButton(self.radiobutton_br, 2)
        self.button_group.addButton(self.radiobutton_tl, 3)
        self.button_group.addButton(self.radiobutton_tr, 4)

        # checkbox properties
        self.cbox_enable_bbox = QCheckBox('Bounding box', self.groupbox_frame_options)
        self.cbox_enable_bbox.move(10, 110)
        self.cbox_enable_bbox.setToolTip('Enable/Disable bounding box')
        self.cbox_enable_class = QCheckBox('Class', self.groupbox_frame_options)
        self.cbox_enable_class.move(10, 170)
        self.cbox_enable_class.setToolTip('Enable/Disable class name')
        self.cbox_enable_conf = QCheckBox('Confidence', self.groupbox_frame_options)
        self.cbox_enable_conf.move(10, 140)
        self.cbox_enable_conf.setToolTip('Enable/Disable confidence score')
        self.cbox_enable_info_background = QCheckBox('Background', self.groupbox_frame_options)
        self.cbox_enable_info_background.move(10, 200)
        self.cbox_enable_info_background.setToolTip('Enable/Disable background box')
        self.cbox_enable_bbox.setChecked(True)
        self.cbox_enable_class.setChecked(True)
        self.cbox_enable_conf.setChecked(True)
        self.cbox_enable_info_background.setChecked(True)

        # statusbar properties
        self.status_bar = QStatusBar()
        self.status_bar.setSizeGripEnabled(False)
        self.status_bar.setProperty('last_msg_time', QDateTime.currentDateTime().toSecsSinceEpoch())
        self.setStatusBar(self.status_bar)
        self.label_class_info = QLabel('Class: -')
        self.status_bar.addPermanentWidget(self.label_class_info)
        self.label_conf = QLabel('Confidence: 0.00')
        self.status_bar.addPermanentWidget(self.label_conf)
        self.label_dim = QLabel('Image size: -')
        self.status_bar.addPermanentWidget(self.label_dim)
        self.label_fps = QLabel('FPS: 0.00')
        self.status_bar.addPermanentWidget(self.label_fps)
        self.label_memory_usage = QLabel('Memory: -')
        self.status_bar.addPermanentWidget(self.label_memory_usage)
        self.label_cpu_usage = QLabel('CPU: -')
        self.status_bar.addPermanentWidget(self.label_cpu_usage)
        self.status_bar.showMessage('Idle')

        # create timer for buttons
        self.timer_start = QTimer()
        self.timer_stop = QTimer()

        # Color box buttons
        self.button_color_box = QPushButton('', self.groupbox_frame_options)
        self.button_color_box.setFixedHeight(20)
        self.button_color_box.setFixedWidth(20)
        self.button_color_class = QPushButton('', self.groupbox_frame_options)
        self.button_color_class.setFixedHeight(20)
        self.button_color_class.setFixedWidth(20)
        self.button_color_confidence = QPushButton('', self.groupbox_frame_options)
        self.button_color_confidence.setFixedHeight(20)
        self.button_color_confidence.setFixedWidth(20)
        self.button_color_bg = QPushButton('', self.groupbox_frame_options)
        self.button_color_bg.setFixedHeight(20)
        self.button_color_bg.setFixedWidth(20)

        # Move buttons to align with the labels, centered horizontally
        button_x_position = 140  # Position for the color buttons
        button_offset = -5  # Horizontal offset to ensure centering

        self.button_color_box.move(button_x_position, 118+button_offset)  # Bounding Box
        self.button_color_class.move(button_x_position, 178+button_offset)  # Class
        self.button_color_confidence.move(button_x_position, 148+button_offset)  # Confidence
        self.button_color_bg.move(button_x_position, 208+button_offset)  # Background

        # Set the colors as needed from the model
        self.button_color_box.setStyleSheet(
            f"background-color: rgb({model.box_color[0]}, {model.box_color[1]}, {model.box_color[2]});border: 1px solid white;")
        self.button_color_class.setStyleSheet(
            f"background-color: rgb({model.text_color_class[0]}, {model.text_color_class[1]}, {model.text_color_class[2]});border: 1px solid white;")
        self.button_color_confidence.setStyleSheet(
            f"background-color: rgb({model.text_color_conf[0]}, {model.text_color_conf[1]}, {model.text_color_conf[2]});border: 1px solid white;")
        self.button_color_bg.setStyleSheet(
            f"background-color: rgb({model.text_color_bg[0]}, {model.text_color_bg[1]}, {model.text_color_bg[2]});border: 1px solid white;")

        self.checkbox_enable_debug = QCheckBox('Debug info', self.groupbox_frame_options)
        self.checkbox_enable_debug.move(10, 400)
        self.checkbox_enable_debug.setToolTip('Enable/Disable debug information in the status bar')
        self.checkbox_enable_debug.setChecked(True)

        # slider properties - brightness
        self.label_brightness_control = QLabel('Brightness:', self.groupbox_frame_options)
        self.label_brightness_control.move(10, 245)
        self.slider_brightness = QSlider(Qt.Horizontal, self.groupbox_frame_options)
        self.slider_brightness.move(10, 265)
        self.slider_brightness.setFixedWidth(100)
        self.slider_brightness.setMinimum(0)
        self.slider_brightness.setMaximum(300)
        self.slider_brightness.setValue(100)
        self.slider_brightness.setSingleStep(1)
        self.slider_brightness.setTickInterval(10)
        self.label_brightness_control = QLabel(str(self.slider_brightness.value()) + '%', self.groupbox_frame_options)
        self.label_brightness_control.move(115, 270)

        # slider properties - contrast
        self.label_contrast_control = QLabel('Contrast:', self.groupbox_frame_options)
        self.label_contrast_control.move(10, 290)
        self.slider_contrast = QSlider(Qt.Horizontal, self.groupbox_frame_options)
        self.slider_contrast.move(10, 310)
        self.slider_contrast.setFixedWidth(100)
        self.slider_contrast.setMinimum(0)
        self.slider_contrast.setMaximum(300)
        self.slider_contrast.setValue(100)
        self.slider_contrast.setSingleStep(1)
        self.slider_contrast.setTickInterval(10)
        self.label_contrast_control = QLabel(str(self.slider_contrast.value()) + '%', self.groupbox_frame_options)
        self.label_contrast_control.move(115, 315)

        self.button_reset_brightness = QPushButton('Reset', self.groupbox_frame_options)
        self.button_reset_contrast = QPushButton('Reset', self.groupbox_frame_options)

        self.button_reset_brightness.setFixedWidth(68)
        self.button_reset_brightness.setFixedHeight(20)
        self.button_reset_contrast.setFixedWidth(68)
        self.button_reset_contrast.setFixedHeight(20)
        self.button_reset_contrast.move(160, 312)
        self.button_reset_brightness.move(160, 267)

        self.checkbox_switch_bbox_mode = QCheckBox('Default bounding box color', self.groupbox_frame_options)
        self.checkbox_switch_bbox_mode.move(10, 430)
        self.checkbox_switch_bbox_mode.setToolTip('Enable/Disable default bounding box color')
        self.checkbox_switch_bbox_mode.setChecked(True)

        # start memory thread
        self.worker_thread_memory = WorkerThreadSystemResource()
        self.worker_thread_memory.update_memory.connect(lambda: Controller.update_system_resource(model, self))
        self.worker_thread_memory.start()

        model.worker_thread_pause_screen = WorkerThreadPauseScreen(self, self.label_stream_width,
                                                                   self.label_stream_height)
        model.worker_thread_pause_screen.update_pause_screen.connect(Controller.update_pause_frame)
        model.worker_thread_pause_screen.start()

        # disable stop button on start
        self.button_stop.setEnabled(False)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E2E2E;
            }
            QGroupBox {
                background-color: #3C3C3C;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                margin-top: 1ex;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
            }
            QLabel {
                color: white;
            }
            QCheckBox {
                color: white;
            }
            QRadioButton {
                color: white;
            }
            QPushButton {
                background-color: #4269b9;
                color: white;
                border: 1px solid white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #2c4f7a;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #AAAAAA;
                border: 1px solid #555555;
            }
            QComboBox {
                background-color: #3C3C3C;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px;
            }
            QStatusBar {
                background-color: #3555a0;
                color: white;
                font-weight: bold;
            }
            QSlider::groove:horizontal {
                border: 1px solid #555555;
                height: 8px;
                background: #3C3C3C;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #4269b9;
                border: 1px solid #555555;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
        """)

        self.checkbox_enable_debug.stateChanged.connect(lambda: Controller.set_debug_mode(self))
        self.slider_brightness.valueChanged.connect(
            lambda: Controller.update_slider_text(self.slider_brightness, self.label_brightness_control))
        self.slider_contrast.valueChanged.connect(
            lambda: Controller.update_slider_text(self.slider_contrast, self.label_contrast_control))

        self.combobox_camera_list.currentTextChanged.connect(
            lambda: Controller.on_combobox_camera_list_changed(self, model))
        self.button_start.clicked.connect(lambda: Controller.on_button_start_clicked(self, model))
        self.button_stop.clicked.connect(lambda: Controller.on_button_stop_clicked(self, model))
        self.timer_start.timeout.connect(lambda: Controller.timer_timeout_start(self))
        self.timer_stop.timeout.connect(lambda: Controller.timer_timeout_stop(self))
        self.button_color_box.clicked.connect(
            lambda: Controller.show_color_picker(model, 'color_box', self.button_color_box))
        self.button_color_class.clicked.connect(
            lambda: Controller.show_color_picker(model, 'color_class', self.button_color_class))
        self.button_color_confidence.clicked.connect(
            lambda: Controller.show_color_picker(model, 'color_conf', self.button_color_confidence))
        self.button_color_bg.clicked.connect(
            lambda: Controller.show_color_picker(model, 'color_bg', self.button_color_bg))
        self.button_reset_brightness.clicked.connect(lambda: self.slider_brightness.setValue(100))
        self.button_reset_contrast.clicked.connect(lambda: self.slider_contrast.setValue(100))
        self.button_rotate.clicked.connect(lambda: Controller.update_frame_rotation_degrees(model))
        self.button_flip_vertical.clicked.connect(lambda: Controller.update_frame_flip_vertical(model))
        self.button_flip_horizontal.clicked.connect(lambda: Controller.update_frame_flip_horizontal(model))
        self.button_fullscreen.clicked.connect(lambda: Controller.show_fullscreen(model))
        self.button_refresh.clicked.connect(lambda: Controller.update_combobox_camera_list_items(self, model))
        self.checkbox_switch_bbox_mode.stateChanged.connect(lambda: Controller.set_bbox_mode(self, model))

    def closeEvent(self, event):
        Controller.stop_worker_thread_camera(self.model)
        self.worker_thread_memory.stop()