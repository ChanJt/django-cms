# -*- coding: utf-8 -*-
from cms.signals.apphook import debug_server_restart
from cms.signals.page import pre_save_page, post_save_page, pre_delete_page, post_delete_page, post_moved_page
from cms.signals.permissions import post_save_user, post_save_user_group, pre_save_user, pre_delete_user, pre_save_group, pre_delete_group, pre_save_pagepermission, pre_delete_pagepermission, pre_save_globalpagepermission, pre_delete_globalpagepermission
from cms.signals.placeholder import pre_delete_placeholder_ref, post_delete_placeholder_ref
from cms.signals.plugins import post_delete_plugins, pre_save_plugins, pre_delete_plugins
from cms.signals.reversion_signals import post_revision
from cms.signals.title import pre_save_title, post_save_title, pre_delete_title, post_delete_title
from cms.utils.compat.dj import is_installed
from cms.utils.conf import get_cms_setting
from django.db.models import signals
from django.dispatch import Signal

from cms.models import Page, Title, CMSPlugin, PagePermission, GlobalPagePermission, PageUser, PageUserGroup, PlaceholderReference
from django.conf import settings
from django.contrib.auth.models import User, Group

#################### Our own signals ###################

# fired after page location is changed - is moved from one node to other
page_moved = Signal(providing_args=["instance"])

# fired after page gets published - copied to public model - there may be more
# than one instances published before this signal gets called
post_publish = Signal(providing_args=["instance", "language"])
post_unpublish = Signal(providing_args=["instance", "language"])

# fired if a public page with an apphook is added or changed
urls_need_reloading = Signal(providing_args=[])

if settings.DEBUG:
    urls_need_reloading.connect(debug_server_restart)

######################### plugins #######################

signals.pre_delete.connect(pre_delete_plugins, sender=CMSPlugin, dispatch_uid='cms_pre_delete_plugin')
signals.post_delete.connect(post_delete_plugins, sender=CMSPlugin, dispatch_uid='cms_post_delete_plugin')
signals.pre_save.connect(pre_save_plugins, sender=CMSPlugin, dispatch_uid='cms_pre_save_plugin')

########################## page #########################

signals.pre_save.connect(pre_save_page, sender=Page, dispatch_uid='cms_pre_save_page')
signals.post_save.connect(post_save_page, sender=Page, dispatch_uid='cms_post_save_page')
signals.pre_delete.connect(pre_delete_page, sender=Page, dispatch_uid='cms_pre_delete_page')
signals.post_delete.connect(post_delete_page, sender=Page, dispatch_uid='cms_post_delete_page')
page_moved.connect(post_moved_page, sender=Page, dispatch_uid='cms_post_move_page')

######################### title #########################

signals.pre_save.connect(pre_save_title, sender=Title, dispatch_uid='cms_pre_save_page')
signals.post_save.connect(post_save_title, sender=Title, dispatch_uid='cms_post_save_page')
signals.pre_delete.connect(pre_delete_title, sender=Title, dispatch_uid='cms_pre_delete_page')
signals.post_delete.connect(post_delete_title, sender=Title, dispatch_uid='cms_post_delete_page')

###################### placeholder #######################

signals.pre_delete.connect(pre_delete_placeholder_ref, sender=PlaceholderReference,
                           dispatch_uid='cms_pre_delete_placeholder_ref')
signals.post_delete.connect(post_delete_placeholder_ref, sender=PlaceholderReference,
                            dispatch_uid='cms_post_delete_placeholder_ref')

###################### permissions #######################

if get_cms_setting('PERMISSION'):
    # only if permissions are in use
    signals.pre_save.connect(pre_save_user, sender=User, dispatch_uid='cms_pre_save_user')
    signals.post_save.connect(post_save_user, sender=User, dispatch_uid='cms_post_save_user')
    signals.pre_delete.connect(pre_delete_user, sender=User, dispatch_uid='cms_pre_delete_user')

    signals.pre_save.connect(pre_save_user, sender=PageUser, dispatch_uid='cms_pre_save_pageuser')
    signals.pre_delete.connect(pre_delete_user, sender=PageUser, dispatch_uid='cms_pre_delete_pageuser')

    signals.pre_save.connect(pre_save_group, sender=Group, dispatch_uid='cms_pre_save_group')
    signals.post_save.connect(post_save_user_group, sender=Group, dispatch_uid='cms_post_save_group')
    signals.pre_delete.connect(pre_delete_group, sender=Group, dispatch_uid='cms_post_save_group')

    signals.pre_save.connect(pre_save_group, sender=PageUserGroup, dispatch_uid='cms_pre_save_pageusergroup')
    signals.pre_delete.connect(pre_delete_group, sender=PageUserGroup, dispatch_uid='cms_pre_delete_pageusergroup')

    signals.pre_save.connect(pre_save_pagepermission, sender=PagePermission, dispatch_uid='cms_pre_save_pagepermission')
    signals.pre_delete.connect(pre_delete_pagepermission, sender=PagePermission,
                               dispatch_uid='cms_pre_delete_pagepermission')

    signals.pre_save.connect(pre_save_globalpagepermission, sender=GlobalPagePermission,
                             dispatch_uid='cms_pre_save_globalpagepermission')
    signals.pre_delete.connect(pre_delete_globalpagepermission, sender=GlobalPagePermission,
                               dispatch_uid='cms_pre_delete_globalpagepermission')

###################### reversion #########################

if is_installed('reversion'):
    from reversion.models import post_revision_commit

    post_revision_commit.connect(post_revision, dispatch_uid='cms_post_revision')

