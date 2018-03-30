#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from app import create_app
from app import db
from flask_script import Manager
from flask_script import Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)


def make_shell_context():
    return dict(app=app)

manager.add_command("shell", Shell(make_context=make_shell_context))


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    manager.run()


