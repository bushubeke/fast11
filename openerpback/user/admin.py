from sqladmin import ModelView
from user.models import *

class UserAdmin(ModelView, model=User):
    column_list =['id','first_name','last_name','password','date_registerd','roles']
    column_searchable_list=['first_name','last_name']
    column_default_sort='id'
    column_sortable_list=['id','first_name','last_name']
    can_create=True
    form_excluded_columns=[User.date_registerd]


class RoleAdmin(ModelView,model=Role):
    column_list=['id','name','description'] 
    column_sortable_list=['id']
    column_default_sort='id'

class ContentTypesAdmin(ModelView,model=ContentTypes):
    column_list=[ContentTypes.id,ContentTypes.app_label,ContentTypes.model_name,ContentTypes.read_roles,ContentTypes.write_roles]
    column_sortable_list=['id']
    column_default_sort='id'
    can_view_details=True
