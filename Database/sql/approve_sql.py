"""
MIT License

Copyright (c) 2022 Aʙɪsʜɴᴏɪ

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import threading
from sqlalchemy import BigInteger, Column, String
from sqlalchemy.exc import SQLAlchemyError
from Database.sql import BASE, SESSION


class Approvals(BASE):
    __tablename__ = "approval"
    chat_id = Column(String(14), primary_key=True)
    user_id = Column(BigInteger, primary_key=True)  # Use BigInteger for large IDs

    def __init__(self, chat_id, user_id):
        self.chat_id = str(chat_id)  # Ensure string
        self.user_id = user_id

    def __repr__(self):
        return "<Approval %s>" % self.user_id


# Ensure table is created
Approvals.__table__.create(checkfirst=True)

APPROVE_INSERTION_LOCK = threading.RLock()


def approve(chat_id, user_id):
    with APPROVE_INSERTION_LOCK:
        try:
            approve_user = Approvals(str(chat_id), user_id)
            SESSION.add(approve_user)
            SESSION.commit()
        except SQLAlchemyError as e:
            SESSION.rollback()  # Rollback on error
            print(f"Error approving user: {e}")
        finally:
            SESSION.close()  # Ensure session is closed


def is_approved(chat_id, user_id):
    try:
        return SESSION.query(Approvals).get((str(chat_id), user_id))
    except SQLAlchemyError as e:
        print(f"Error checking approval: {e}")
        return None
    finally:
        SESSION.close()  # Ensure session is closed


def disapprove(chat_id, user_id):
    with APPROVE_INSERTION_LOCK:
        try:
            disapprove_user = SESSION.query(Approvals).get((str(chat_id), user_id))
            if disapprove_user:
                SESSION.delete(disapprove_user)
                SESSION.commit()
                return True
            return False
        except SQLAlchemyError as e:
            SESSION.rollback()  # Rollback on error
            print(f"Error disapproving user: {e}")
            return False
        finally:
            SESSION.close()  # Ensure session is closed


def list_approved(chat_id):
    try:
        return (
            SESSION.query(Approvals)
            .filter(Approvals.chat_id == str(chat_id))
            .order_by(Approvals.user_id.asc())
            .all()
        )
    except SQLAlchemyError as e:
        print(f"Error listing approved users: {e}")
        return []
    finally:
        SESSION.close()  # Ensure session is closed
