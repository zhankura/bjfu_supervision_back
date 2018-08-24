#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/7 2:54 PM
# @Author  : suchang
# @File    : run.py
# -*- coding=utf-8 -*-

from flask_script import Manager, Shell
from app.core.models.fake import insert_user
from flask import jsonify
from app import app, db
from flask_migrate import Migrate, MigrateCommand
import pymysql
import os
from flask_pymongo import PyMongo

manager = Manager(app)
migrate = Migrate(app, db)

mongo = PyMongo(app)


def create_all():
    db.drop_all()
    db.create_all()
    insert_user()


def make_shell_context():
    return dict(app=app, mongo=mongo, db=db, create_all=create_all)


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
