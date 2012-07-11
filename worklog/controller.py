#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
from cement.core import foundation, controller, handler
from .model import WorkLog
from datetime import datetime

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

    @controller.expose(aliases=['s'])
    def default(self):
        self._activity()

class EndController(ActivityWriter):
    class Meta:
        interface = controller.IController
        stacked_on = 'WorkLog'
        label = 'end'
        description = 'end last activity'
        arguments = [(['args'], dict(type=str, nargs='+', metavar='description'))]

    @controller.expose(aliases=['e'])
    def default(self):
        self._activity()


class ResumeController(ActivityWriter):
    class Meta:
        interface = controller.IController
        stacked_on = 'WorkLog'
        label = 'resume'
        description = 'resume last activity'
        arguments = [(['args'], dict(type=str, nargs='+', metavar='description'))]

    @controller.expose(aliases=['r'])
    def default(self):
        self._activity()

class ListController(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        stacked_on = 'WorkLog'
        label = 'list'
        description = 'list log'
        arguments = []

    @controller.expose(aliases=['l'])
    def default(self):
        [print(unicode(i)) for i in self.app.session.query(WorkLog).all()]

class DiffController(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        stacked_on = 'WorkLog'
        label = 'diff'
        description = 'diff now() since last log'
        arguments = []

    @controller.expose(aliases=['d'])
    def default(self):
        wl = self.app.session.query(WorkLog).order_by(WorkLog.created_at.desc()).limit(1).one()
        print(unicode(wl))
        print("diff: %s" % (datetime.now() - wl.created_at))

export = [StartController, EndController, ResumeController, ListController, DiffController]
