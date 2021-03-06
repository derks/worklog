#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)

from cement.core import hook

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from sqlalchemy import Integer, Column, Enum, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.schema import Table

from datetime import datetime

Base = declarative_base()

class WorkLog(Base):
    __tablename__ = 'worklog'

    id = Column(Integer, primary_key=True)
    activity = Column(Enum('start', 'end', 'resume'))
    description = Column(String(256)) # in case of start activity, this will be the activity name
    created_at = Column(DateTime(), default=datetime.now)

    def __unicode__(self):
        return "%s %s %s" % (self.created_at, self.activity.ljust(6), self.description)

def init(app):
    app.log.debug(app.config.get('main', 'db'))
    e = create_engine(app.config.get('main', 'db'))
    app.session = scoped_session(sessionmaker(bind=e, autoflush=True))

    Base.metadata.bind = e
    Base.metadata.create_all()
