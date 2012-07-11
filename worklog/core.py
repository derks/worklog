#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from cement.core import foundation, handler
from . import controller as ctrl

log = logging.getLogger(__name__)

class WorkLogApp(foundation.CementApp):
    class Meta:
        label = 'WorkLog'
        base_controller = ctrl.WorkLogController

def main():
    app = WorkLogApp()
    handler.register(ctrl.StartController)
    app.setup()
    app.run()
