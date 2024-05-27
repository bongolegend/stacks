from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, func, text, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


Base = declarative_base()

class CommonBase(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

followers = Table(
    'followers', Base.metadata,
    Column('follower_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('leader_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
)

class User(CommonBase):
    __tablename__ = 'users'

    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

    tasks = relationship('Task', back_populates='user', cascade="all, delete", passive_deletes=True)
    goals = relationship('Goal', back_populates='user', cascade="all, delete", passive_deletes=True)
    is_following = relationship(
        'User',
        secondary=followers,
        primaryjoin="users.c.id == followers.c.follower_id",
        secondaryjoin="users.c.id == followers.c.leader_id",
        backref="followers"
    )

    def __repr__(self):
        return f"<{self.username}, {self.id}>"


class Task(CommonBase):
    __tablename__ = 'tasks'

    description = Column(Text, nullable=False)
    is_completed = Column(Boolean, default=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    goal_id = Column(UUID(as_uuid=True), ForeignKey('goals.id'), nullable=True)

    user = relationship('User', back_populates='tasks')
    goal = relationship('Goal', back_populates='tasks')

class Goal(CommonBase):
    __tablename__ = 'goals'

    description = Column(Text, nullable=False)
    is_completed = Column(Boolean, default=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    user = relationship('User', back_populates='goals')
    tasks = relationship('Task', back_populates='goal')