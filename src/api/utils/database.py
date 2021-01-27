"""
sqlalchemy init object
"""
# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseMixin:
    """
    abstract class for model
    """

    def save(self):
        """
        save data to database
        """
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """
        delete data on database
        """
        db.session.delete(self)
        db.session.commit()
