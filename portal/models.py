from django.db import models


class NavMenu(models.Model):
    menu_id = models.IntegerField(db_column='MenuId', primary_key=True, null=False)
    menu_name = models.CharField(db_column='MenuName', max_length=100, null=False)
    caption = models.CharField(db_column='Caption', max_length=100, null=False)
    parent_menu_id = models.IntegerField(db_column='ParentMenuId', null=True)
    is_enable = models.BooleanField(db_column='IsEnable', null=False)
    is_visible = models.BooleanField(db_column='IsVisible', null=False)
    sort_index = models.IntegerField(db_column='SortIndex', null=False)
    is_admin_only = models.BooleanField(db_column='IsAdminOnly', null=False)
    link_type = models.CharField(db_column='LinkType', max_length=20, null=True)
    page_path = models.CharField(db_column='PagePath', max_length=100, null=True)
    report_id = models.CharField(db_column='ReportId', max_length=50, null=True)
    report_option = models.CharField(db_column='ReportOption', max_length=500, null=True)
    filter_table = models.CharField(db_column='filterTable', max_length=100, null=True)
    filter_column = models.CharField(db_column='filterColumn', max_length=100, null=True)

    class Meta:
        db_table = 'NavMenu'


