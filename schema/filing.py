# Copyright 2017 Charity Navigator.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sqlalchemy as db
import sqlalchemy.dialects.mysql as m
from sqlalchemy.orm import relationship
from base import Base

class Filing(Base):
    __tablename__ = "filing"
    
    id               = db.Column(db.Integer, primary_key=True)
    EIN              = db.Column(m.CHAR(9))
    DLN              = db.Column(m.CHAR(14))
    ObjectId         = db.Column(m.CHAR(18))
    FormType         = db.Column(db.String(20))
    URL              = db.Column(db.String(100))
    OrganizationName = db.Column(db.String(120))
    SubmittedOn      = db.Column(db.Date)
    LastUpdated      = db.Column(db.DateTime)
    TaxPeriod        = db.Column(db.Date)
    IsElectronic     = db.Column(m.BIT)
    IsAvailable      = db.Column(m.BIT)

    raw = relationship("RawXML", back_populates="filing")

class RawXML(Base):
    __tablename__ = "xml"

    id = db.Column(db.Integer, primary_key=True)
    FilingId = db.Column(db.Integer, db.ForeignKey('filing.id', ondelete="CASCADE", onupdate="CASCADE"), unique=True)
    XML = db.Column(m.LONGTEXT)
    Version = db.Column(db.String(20))
    FormType = db.Column(db.String(5))

    filing = relationship("Filing", back_populates="raw")

    def __init__(self, xmlStr, filing, version = None, formType = None):
        self.filing = filing
        self.XML    = xmlStr
        self.Version = version
        self.FormType = formType
