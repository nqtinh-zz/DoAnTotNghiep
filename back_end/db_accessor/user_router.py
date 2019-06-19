#  @Project FCloudConsole
#  @Homepage https://fsmartstore.com
#  @Copyright (c) 2018 Fujinet Systems JSC. All Rights Reserved.
#  @License All resources of the source code are owned by 'Fujinet Systems JSC'.
#  Intentionally infringing, stealing, exchanging, or trading in all of the
#  resources below without our consent, is a violation of intellectual property
#  rights. So, if you accidentally receive this source code, please send an email
#  to rd-support@fujinet.net, so we can find the best solution for this problem.


class UserRouter:
    """
    A router to control all database operations on models in the
    auth application.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read web_admin models go to fusers.
        """
        if model._meta.app_label == 'web_admin':
            return 'fusers'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write web_admin models go to fusers.
        """
        if model._meta.app_label == 'web_admin':
            return 'fusers'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the web_admin app is involved.
        """
        if obj1._meta.app_label == 'web_admin' or \
                obj2._meta.app_label == 'web_admin':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the web_admin app only appears in the 'fusers'
        database.
        """
        if app_label == 'web_admin':
            return db == 'fusers'
            # this will prevent other apps to create their tables in 'second_db'
        if db == 'fusers':
            return False
        return None
