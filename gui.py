import sys
import os
import signal

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentIcon as FIF, setTheme, Theme
from qfluentwidgets import NavigationItemPosition, FluentWindow

import resources.resources_rc  # noqa
from sakura import children_windows
from sakura.components.ui.Home import Home
from sakura.components.ui.PlayerUi import PlayerUi
from sakura.components.ui.Settings import SettingsUi
from sakura.config import conf, save_conf, set_stop_end
from sakura.config.sakura_logging import logger


def shutdown_logger():
    logger.info("Shutting down logger")
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)


class Window(FluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()

        # 初始化主页面
        self.init_window()
        # 创建子界面，实际使用时将 Widget 换成自己的子界面
        self.homeInterface = Home(self)
        self.playerInterface = PlayerUi(self)
        self.settingInterface = SettingsUi(self)
        self.init_navigation()

    def init_navigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, 'Home')
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.playerInterface, FIF.PLAY, 'Player')
        self.addSubInterface(self.settingInterface, FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

    def init_window(self):
        self.setMinimumHeight(800)
        self.setMinimumWidth(1286)
        self.navigationInterface.setExpandWidth(180)
        self.setWindowIcon(QIcon(':/sakura/icon/logo-128x128.ico'))
        self.setWindowTitle('Sky Auto Player')

    def closeEvent(self, event):
        set_stop_end(True)
        save_conf(conf)
        for item in children_windows:
            item.close()
        logger.info("Closing application")
        shutdown_logger()
        super().closeEvent(event)
        
        current_pid = os.getpid()
        os.kill(current_pid, signal.SIGTERM)


if __name__ == '__main__':
    setTheme(Theme.AUTO)
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    screen_rect = screen.availableGeometry()
    w = Window()
    x = (screen_rect.width() - w.width()) // 2
    y = (screen_rect.height() - w.height()) // 2
    w.move(x, y)
    w.show()
    app.exec()
