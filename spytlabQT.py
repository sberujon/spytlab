import sys

if 'qt' not in sys.modules:
    try:
        from PyQt5.QtCore import *
        from PyQt5.QtGui import *
        from PyQt5.QtWidgets import *
        try:
            #In case PyQwt is compiled with QtSvg
            from PyQt5.QtSvg import *
        except:
            pass
    except:
        from qt import *
else:
    from qt import *
