import dataclasses
from typing import List

from flask_sqlalchemy import Model
from sqlalchemy import (BOOLEAN, JSON, TEXT, BigInteger, Column, DateTime,
                        Enum, Float, ForeignKey, Integer, LargeBinary,
                        UniqueConstraint)
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql import func

from txmatching.auth.data_types import UserRole
from txmatching.patients.patient import DonorType, RecipientRequirements
from txmatching.utils.country_enum import Country
# pylint: disable=too-few-public-methods,too-many-arguments
# disable because sqlalchemy needs classes without public methods
from txmatching.utils.enums import Sex
from txmatching.utils.hla_system.hla_code_processing_result_detail import \
    HlaCodeProcessingResultDetail


class ConfigModel(Model):
    __tablename__ = 'config'
    __table_args__ = {'extend_existing': True}
    # Here and below I am using Integer instead of BigInt because it seems that there is a bug and BigInteger is not
    # transferred to BigSerial with autoincrement True, but to BigInt only.
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    txm_event_id = Column(Integer, ForeignKey('txm_event.id', ondelete='CASCADE'), unique=False, nullable=False)
    parameters = Column(JSON, unique=False, nullable=False)
    patients_hash = Column(BigInteger, unique=False, nullable=False)
    created_by = Column(Integer, unique=False, nullable=False)
    # created at and updated at is not handled by triggers as then am not sure how tests would work, as triggers
    # seem to be specific as per db and I do not think its worth the effort as this simple approach works fine
    created_at = Column(DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    pairing_results = relationship('PairingResultModel', backref='config', passive_deletes=True)
    UniqueConstraint('txm_event_id')


class PairingResultModel(Model):
    __tablename__ = 'pairing_result'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    config_id = Column(Integer, ForeignKey('config.id', ondelete='CASCADE'), unique=False, nullable=False)
    calculated_matchings = Column(JSON, unique=False, nullable=False)
    score_matrix = Column(JSON, unique=False, nullable=False)
    valid = Column(BOOLEAN, unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    UniqueConstraint('config_id')


class TxmEventModel(Model):
    __tablename__ = 'txm_event'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(TEXT, unique=True, nullable=False)
    configs = relationship('ConfigModel', backref='txm_event', passive_deletes=True)  # type: List[ConfigModel]
    donors = relationship('DonorModel', backref='txm_event', passive_deletes=True)  # type: List[DonorModel]
    created_at = Column(DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)


class RecipientModel(Model):
    __tablename__ = 'recipient'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    txm_event_id = Column(Integer, ForeignKey('txm_event.id', ondelete='CASCADE'), unique=False, nullable=False)
    medical_id = Column(TEXT, unique=False, nullable=False)
    country = Column(Enum(Country), unique=False, nullable=False)
    blood = Column(TEXT, unique=False, nullable=False)
    hla_typing_raw = Column(JSON, unique=False, nullable=False)
    hla_typing = Column(JSON, unique=False, nullable=False)  # HLATyping is model of the JSON
    recipient_requirements = Column(JSON, unique=False, nullable=False,
                                    default=dataclasses.asdict(RecipientRequirements()))
    recipient_cutoff = Column(Integer, unique=False, nullable=False)
    sex = Column(Enum(Sex), unique=False, nullable=True)
    height = Column(Integer, unique=False, nullable=True)
    weight = Column(Float, unique=False, nullable=True)
    yob = Column(Integer, unique=False, nullable=True)
    waiting_since = Column(DateTime(timezone=True), unique=False, nullable=True)
    previous_transplants = Column(Integer, unique=False, nullable=True)
    created_at = Column(DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    acceptable_blood = relationship('RecipientAcceptableBloodModel', backref='recipient', passive_deletes=True,
                                       lazy='joined')  # type: List[RecipientAcceptableBloodModel]
    hla_antibodies = Column(JSON, unique=False, nullable=False)
    hla_antibodies_raw = relationship('HLAAntibodyRawModel', backref='recipient', passive_deletes=True,
                                         lazy='joined')  # type: List[HLAAntibodyRawModel]
    UniqueConstraint('medical_id', 'txm_event_id')

    def __repr__(self):
        return f'<RecipientModel {self.id} (medical_id={self.medical_id})>'


class DonorModel(Model):
    __tablename__ = 'donor'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    txm_event_id = Column(Integer, ForeignKey('txm_event.id', ondelete='CASCADE'), unique=False, nullable=False)
    medical_id = Column(TEXT, unique=False, nullable=False)
    country = Column(Enum(Country), unique=False, nullable=False)
    blood = Column(TEXT, unique=False, nullable=False)
    hla_typing_raw = Column(JSON, unique=False, nullable=False)
    hla_typing = Column(JSON, unique=False, nullable=False)
    active = Column(BOOLEAN, unique=False, nullable=False)
    donor_type = Column(Enum(DonorType), unique=False, nullable=False)
    sex = Column(Enum(Sex), unique=False, nullable=True)
    height = Column(Integer, unique=False, nullable=True)
    weight = Column(Float, unique=False, nullable=True)
    yob = Column(Integer, unique=False, nullable=True)
    created_at = Column(DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    recipient_id = Column(Integer, ForeignKey('recipient.id'), unique=False, nullable=True)
    recipient = relationship('RecipientModel', backref=backref('donor', uselist=False),
                                passive_deletes=True,
                                lazy='joined')
    UniqueConstraint('medical_id', 'txm_event_id')

    def __repr__(self):
        return f'<DonorModel {self.id} (medical_id={self.medical_id})>'


class RecipientAcceptableBloodModel(Model):
    __tablename__ = 'recipient_acceptable_blood'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    recipient_id = Column(Integer, ForeignKey('recipient.id', ondelete='CASCADE'), unique=False, nullable=False)
    blood_type = Column(TEXT, unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)


class HLAAntibodyRawModel(Model):
    __tablename__ = 'hla_antibody_raw'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    recipient_id = Column(Integer, ForeignKey('recipient.id', ondelete='CASCADE'), unique=False, nullable=False)
    raw_code = Column(TEXT, unique=False, nullable=False)
    mfi = Column(Integer, unique=False, nullable=False)
    cutoff = Column(Integer, unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f'<HLAAntibodyRawModel {self.id} ' \
               f'(raw_code={self.raw_code}, mfi={self.mfi}, cutoff={self.cutoff})>'


class AppUserModel(Model):
    __tablename__ = 'app_user'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(TEXT, unique=True, nullable=False)
    pass_hash = Column(TEXT, unique=False, nullable=False)
    role = Column(Enum(UserRole), unique=False, nullable=False)
    default_txm_event_id = Column(Integer, unique=False, nullable=True)
    # Whitelisted IP address if role is SERVICE
    # Seed for TOTP in all other cases
    second_factor_material = Column(TEXT, unique=False, nullable=False)
    phone_number = Column(TEXT, unique=False, nullable=True, default=None)
    require_2fa = Column(BOOLEAN, unique=False, nullable=False, default=True)
    allowed_edit_countries = Column(JSON, unique=False, nullable=False, default=lambda: [])

    created_at = Column(DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)


class UserToAllowedEvent(Model):
    __tablename__ = 'user_to_allowed_event'
    __table_args__ = {'extend_existing': True}

    user_id = Column(
        Integer,
        ForeignKey('app_user.id', ondelete='CASCADE'),
        unique=False, nullable=False, primary_key=True, index=True
    )
    txm_event_id = Column(
        Integer,
        ForeignKey('txm_event.id', ondelete='CASCADE'),
        unique=False, nullable=False, primary_key=True, index=True
    )


class UploadedDataModel(Model):
    __tablename__ = 'uploaded_data'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    txm_event_id = Column(Integer, ForeignKey('txm_event.id', ondelete='CASCADE'), unique=False, nullable=False)
    user_id = Column(Integer, ForeignKey('app_user.id'), unique=False, nullable=False)
    uploaded_data = Column(JSON, unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), unique=False, nullable=False, server_default=func.now(),
                        onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)


class ParsingErrorModel(Model):
    __tablename__ = 'parsing_error'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    hla_code = Column(TEXT, unique=False, nullable=False)
    hla_code_processing_result_detail = Column(Enum(HlaCodeProcessingResultDetail), unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        unique=False,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
    deleted_at = Column(DateTime(timezone=True), nullable=True)


class UploadedFileModel(Model):
    __tablename__ = 'uploaded_file'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    file_name = Column(TEXT, unique=False, nullable=False)
    file = Column(LargeBinary, unique=False, nullable=False)
    txm_event_id = Column(Integer, ForeignKey('txm_event.id', ondelete='CASCADE'), unique=False, nullable=False)
    user_id = Column(Integer, ForeignKey('app_user.id', ondelete='CASCADE'), unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), unique=False, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        unique=False,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
    deleted_at = Column(DateTime(timezone=True), nullable=True)
