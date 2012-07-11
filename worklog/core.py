#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from cement.core import foundation, handler, hook
from . import controller as ctrl
from .model import init

from xdg.BaseDirectory import save_data_path
from os.path import join

log = logging.getLogger(__name__)

class WorkLogApp(foundation.CementApp):
    class Meta:
        label = 'WorkLog'
        base_controller = ctrl.WorkLogController
        config_defaults = {
            'main': {
                'db': 'sqlite+pysqlite:///' +join(save_data_path('worklog'), 'db.sqlite')
            }
        }

def main():
    app = WorkLogApp()
    [handler.register(c) for c in ctrl.export]
    hook.register(name='cement_post_setup_hook')(init)
    app.setup()
    app.run()
