from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship

from app.api.bootstrap import api
from app.api.helpers.db import safe_query
from app.api.helpers.permissions import jwt_required
from app.api.schema.email_notifications import EmailNotificationSchema
from app.models import db
from app.models.email_notification import EmailNotification
from app.models.user import User


class EmailNotificationListAdmin(ResourceList):
    """
    List and create email notifications
    """
    methods = ['GET', ]
    schema = EmailNotificationSchema
    decorators = (api.has_permission('is_admin'),)
    data_layer = {'session': db.session,
                  'model': EmailNotification}


class EmailNotificationList(ResourceList):
    """
    List all the email notification
    """

    def query(self, view_kwargs):
        """
        query method for Notifications list
        :param view_kwargs:
        :return:
        """
        query_ = self.session.query(EmailNotification)
        if view_kwargs.get('id'):
            user = safe_query(self, User, 'id', view_kwargs['id'], 'id')
            query_ = query_.join(User).filter(User.id == user.id)
        return query_

    view_kwargs = True
    methods = ['GET', ]
    decorators = (api.has_permission('is_user_itself', fetch="id", fetch_as="id"),)
    schema = EmailNotificationSchema
    data_layer = {'session': db.session,
                  'model': EmailNotification,
                  'methods': {
                      'query': query
                  }}


class EmailNotificationDetail(ResourceDetail):
    """
    Email notification detail by ID
    """
    decorators = (api.has_permission('is_user_itself', fetch="user_id", fetch_as="id",
                  model=EmailNotification),)
    schema = EmailNotificationSchema
    data_layer = {'session': db.session,
                  'model': EmailNotification}


class EmailNotificationRelationshipRequired(ResourceRelationship):
    """
    Email notification Relationship (Required)
    """
    decorators = (jwt_required,)
    methods = ['GET', 'PATCH']
    schema = EmailNotificationSchema
    data_layer = {'session': db.session,
                  'model': EmailNotification}


class EmailNotificationRelationshipOptional(ResourceRelationship):
    """
    Email notification Relationship (Optional)
    """
    decorators = (api.has_permission('is_user_itself', fetch="user_id", fetch_as="id",
                                     model=EmailNotification),)
    schema = EmailNotificationSchema
    data_layer = {'session': db.session,
                  'model': EmailNotification}
