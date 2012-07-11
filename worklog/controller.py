#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from cement.core import foundation, controller, handler
from .model import WorkLog

log = logging.getLogger(__name__)

class WorkLogController(controller.CementBaseController):
    """
        commands:
            start <activity>
            end
            resume
            diff (since last entry)
            pop (display last activity, time spent and archive those records) --keep (do not archive, only display)
            maybe list (display activities)
    """
    class Meta:
        label = 'WorkLog'
        description = 'WorkLog entry point'

class StartController(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        stacked_on = 'WorkLog'
        label = 'start'
        description = 'start an activity'
        arguments = [(['activity'], dict(type=str, nargs='+'))]

    @controller.expose(aliases=['s'], help="start activity")
    def default(self):
        wl = WorkLog()
        wl.activity = "start"
        wl.description = " ".join(self.pargs.activity)
        self.app.session.add(wl)
        self.app.session.commit()
