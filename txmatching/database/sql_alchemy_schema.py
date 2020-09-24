import dataclasses

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from txmatching.auth.data_types import UserRole
from txmatching.database.db import db
from txmatching.patients.patient import DonorType, RecipientRequirements
# pylint: disable=too-few-public-methods
# disable because sqlalchemy needs classes without public methods
from txmatching.utils.country import Country


class ConfigModel(db.Model):
    __tablename__ = 'config'
    __table_args__ = {'extend_existing': True}
    # Here and below I am using Integer instead of BigInt because it seems that there is a bug and BigInteger is not
    # transfered to BigSerial with autoincrement True, but to BigInt only.
    id = db.Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    txm_event_id = db.Column(db.Integer, ForeignKey('txm_event.id'), unique=False, nullable=False)
    parameters = db.Column(db.JSON, unique=False, nullable=False)
    created_by = db.Column(db.Integer, unique=False, nullable=False)
    # created at and updated at is not handled by triggers as then am not sure how tests would work, as triggers
    # seem to be specific as per db and I do not think its worth the effort as this simple approach works fine
    created_at = db.Column(db.DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    pairing_results = relationship('PairingResultModel', backref='config', cascade='all, delete')


class PairingResultModel(db.Model):
    __tablename__ = 'pairing_result'
    __table_args__ = {'extend_existing': True}

    id = db.Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    config_id = db.Column(db.Integer, ForeignKey('config.id'), unique=False, nullable=False)
    calculated_matchings = db.Column(db.JSON, unique=False, nullable=False)
    score_matrix = db.Column(db.JSON, unique=False, nullable=False)
    valid = db.Column(db.BOOLEAN, unique=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)


class TxmEventModel(db.Model):
    __tablename__ = 'txm_event'
    __table_args__ = {'extend_existing': True}

    id = db.Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.TEXT, unique=True, nullable=False)
    configs = relationship('ConfigModel', backref='txm_event', cascade='all, delete')
    donors = relationship('DonorModel', backref='txm_event', cascade='all, delete')
    recipients = relationship('RecipientModel', backref='txm_event', cascade='all, delete')
    created_at = db.Column(db.DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)


class RecipientModel(db.Model):
    __tablename__ = 'recipient'
    __table_args__ = {'extend_existing': True}

    id = db.Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    txm_event_id = db.Column(db.Integer, ForeignKey('txm_event.id'), unique=False, nullable=False)
    medical_id = db.Column(db.TEXT, unique=False, nullable=False)
    country = db.Column(db.Enum(Country), unique=False, nullable=False)
    blood = db.Column(db.TEXT, unique=False, nullable=False)
    hla_typing = db.Column(db.JSON, unique=False, nullable=False)
    active = db.Column(db.BOOLEAN, unique=False, nullable=False)
    recipient_requirements = db.Column(db.JSON, unique=False, nullable=False,
                                       default=dataclasses.asdict(RecipientRequirements()))
    created_at = db.Column(db.DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    acceptable_blood = relationship('RecipientAcceptableBloodModel', backref='recipient', cascade='all, delete')
    hla_antibodies = relationship('RecipientHLAAntibodyModel', backref='recipient', cascade='all, delete')
    UniqueConstraint('medical_id', 'txm_event_id')


class DonorModel(db.Model):
    __tablename__ = 'donor'
    __table_args__ = {'extend_existing': True}

    id = db.Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    txm_event_id = db.Column(db.Integer, ForeignKey('txm_event.id'), unique=False, nullable=False)
    medical_id = db.Column(db.TEXT, unique=False, nullable=False)
    country = db.Column(db.Enum(Country), unique=False, nullable=False)
    blood = db.Column(db.TEXT, unique=False, nullable=False)
    hla_typing = db.Column(db.JSON, unique=False, nullable=False)
    active = db.Column(db.BOOLEAN, unique=False, nullable=False)
    donor_type = db.Column(db.Enum(DonorType), unique=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    recipient_id = db.Column(db.Integer, ForeignKey('recipient.id'), unique=False, nullable=True)
    UniqueConstraint('medical_id', 'txm_event_id')


class RecipientAcceptableBloodModel(db.Model):
    __tablename__ = 'recipient_acceptable_blood'
    __table_args__ = {'extend_existing': True}

    id = db.Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    recipient_id = db.Column(db.Integer, ForeignKey('recipient.id'), unique=False, nullable=False)
    blood_type = db.Column(db.TEXT, unique=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)


class RecipientHLAAntibodyModel(db.Model):
    __tablename__ = 'recipient_hla_antibodies'
    __table_args__ = {'extend_existing': True}

    id = db.Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    recipient_id = db.Column(db.Integer, ForeignKey('recipient.id'), unique=False, nullable=False)
    hla_antibody = db.Column(db.TEXT, unique=False, nullable=False)
    mfi = db.Column(db.Integer, unique=False, nullable=False)
    cutoff = db.Column(db.Integer, unique=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)


class AppUserModel(db.Model):
    __tablename__ = 'app_user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = db.Column(db.TEXT, unique=True, nullable=False)
    pass_hash = db.Column(db.TEXT, unique=False, nullable=False)
    role = db.Column(db.Enum(UserRole), unique=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def __init__(self, email: str, pass_hash: str, role: UserRole):
        self.email = email
        self.pass_hash = pass_hash
        self.role = role
        self._is_authenticated = False

    @staticmethod
    def is_active():
        return True

    def is_authenticated(self):
        return self._is_authenticated

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.email

    def set_authenticated(self, authenticated: bool):
        self._is_authenticated = authenticated
