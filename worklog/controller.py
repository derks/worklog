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

class ActivityWriter(controller.CementBaseController):
    def _activity(self):
        wl = WorkLog()
        wl.activity = self._meta.label
        wl.description = " ".join(self.pargs.args)
        self.app.session.add(wl)
        self.app.session.commit()

class StartController(ActivityWriter):
    class Meta:
        interface = controller.IController
        stacked_on = 'WorkLog'
        label = 'start'
        description = 'start an activity'
        arguments = [(['args'], dict(metavar='activity', type=str, nargs='+'))]

    @controller.expose(aliases=['s'], help="start activity")
    def default(self):
        self._activity()

class EndController(ActivityWriter):
    class Meta:
        interface = controller.IController
        stacked_on = 'WorkLog'
        label = 'end'
        description = 'end last activity'
        arguments = [(['args'], dict(type=str, nargs='+', metavar='description'))]

    @controller.expose(aliases=['e'], help="end activity")
    def default(self):
        self._activity()


class ResumeController(ActivityWriter):
    class Meta:
        interface = controller.IController
        stacked_on = 'WorkLog'
        label = 'resume'
        description = 'resume last activity'
        arguments = [(['args'], dict(type=str, nargs='+', metavar='description'))]

    @controller.expose(aliases=['r'], help="resume activity")
    def default(self):
        self._activity()

export = [StartController, EndController, ResumeController]
