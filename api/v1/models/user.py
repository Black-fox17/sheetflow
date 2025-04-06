""" User data model
"""

from sqlalchemy import Column, String, text, Boolean, Index
# from sqlalchemy.orm import relationship
# from api.v1.models.associations import user_organisation_association
# from api.v1.models.permissions.user_org_role import user_organisation_roles
from api.v1.models.base_model import BaseTableModel


class User(BaseTableModel):
    __tablename__ = "users"
    
    def to_dict(self):
        obj_dict = super().to_dict()
        obj_dict.pop("password")
        return obj_dict

    def __str__(self):
        return self.email
