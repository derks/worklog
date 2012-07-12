#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
from cement.core import foundation, controller, handler
from .model import WorkLog
from datetime import datetime, timedelta

log = logging.getLogger(__name__)

class WorkLogController(controller.CementBaseController):
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
        label = 'start'
        description = 'start an activity'
        arguments = [(['args'], dict(metavar='activity', type=str, nargs='+'))]

    @controller.expose(aliases=['s'])
    def default(self):
        self._activity()

class EndController(ActivityWriter):
    class Meta:
        interface = controller.IController
        label = 'end'
        description = 'end last activity'
        arguments = [(['args'], dict(type=str, nargs='*', metavar='description'))]

    @controller.expose(aliases=['e'])
    def default(self):
        self._activity()


class ResumeController(ActivityWriter):
    class Meta:
        interface = controller.IController
        label = 'resume'
        description = 'resume last activity'
        arguments = [(['args'], dict(type=str, nargs='*', metavar='description'))]

    @controller.expose(aliases=['r'])
    def default(self):
        self._activity()

def display(items):
    [print(unicode(i)) for i in items]

def display_diff(items, diff):
    display(items)
    print("diff: %s" % diff)

class ListController(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'list'
        description = 'list log'
        arguments = []

    @controller.expose(aliases=['l'])
    def default(self):
        display(self.app.session.query(WorkLog).all())

class DiffController(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'diff'
        description = 'diff now() since last log'
        arguments = [(['-f', '--full'], dict(action='store_true'))]

    @controller.expose(aliases=['d'])
    def default(self):
        self.log.debug(self.pargs)
        if self.pargs.full:
            items, state = get_activity(self.app.session, self.log)
            # FIXME: fix get_activity for this use-case so if the first record isnt END state, create it from now()
            diff = state[2]
        else:
            wl = self.app.session.query(WorkLog).order_by(WorkLog.created_at.desc()).limit(1).one()
            diff = datetime.now() - wl.created_at
            items = [wl]

        display_diff(items, diff)

def get_activity(session, log):
    q = session.query(WorkLog).order_by(WorkLog.created_at.desc()).all()

    ALG_START=0
    START='start'
    END='end'
    RESUME='resume'
    states = {
        # CURSTATE: NEXT_STATES, NEW_DIFFSUM_FN(cur diff sum, prev item, cur item)
        ALG_START: ([END], lambda _, _1, _2: timedelta(0)),
        END: ([START, RESUME], lambda s, p, i: s + (p.created_at - i.created_at)),
        RESUME: ([END], lambda s, _, _1: s),
    }

    state = (ALG_START, None, None)
    #       current state, prev item, diff sum
    items = []
    while not state[0] == START:
        item = q.pop(0)
        if item.activity not in states[state[0]][0]:
            raise RuntimeError("invalid state")

        state = (item.activity, item, states[state[0]][1](state[2], state[1], item))
        log.debug("new state: (%s, %s, %s)" % state)
        items.insert(0, item)
    return items, state

class PopController(controller.CementBaseController):
    class Meta:
        interface = controller.IController
        label = 'pop'
        description = 'diff now() since last log'
        arguments = []

    @controller.expose(aliases=['p'])
    def default(self):
        items, state = get_activity(self.app.session, log)
        display_diff(items, state[2])
        [self.app.session.delete(i) for i in items]
        self.app.session.commit()

export = [StartController, EndController, ResumeController, ListController, DiffController, PopController]
