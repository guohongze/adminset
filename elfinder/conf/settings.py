from os.path import join
from django.conf import settings
from elfinder.utils.accesscontrol import fs_standard_access
from elfinder.volumes.filesystem import ElfinderVolumeLocalFileSystem
from elfinder.volumes.storage import ElfinderVolumeStorage
ELFINDER_JS_URLS = {
    'a_jquery' : '%splugins/jQuery/jquery-2.2.3.min.js' % settings.STATIC_URL,
    'b_jqueryui' : '%splugins/jquery-ui-1.12/jquery-ui.js' % settings.STATIC_URL,
    'c_elfinder' : '%selfinder/js/elfinder.full.js' % settings.STATIC_URL,
}
#allow to override any key in the project settings file   
ELFINDER_JS_URLS.update(getattr(settings, 'ELFINDER_JS_URLS', {}))

ELFINDER_CSS_URLS = {
    'a_jqueryui' : '%splugins/jquery-ui-1.12/jquery-ui.css' % settings.STATIC_URL,
    'b_elfinder' : '%selfinder/css/elfinder.min.css' % settings.STATIC_URL
}
#allow to override any key in the project settings file   
ELFINDER_CSS_URLS.update(getattr(settings, 'ELFINDER_CSS_URLS', {}))

# 这些文件在本地不存在，注释掉或设置为空字符串
# ELFINDER_WIDGET_JS_URL = '%sjs/jquery.elfinder-widget.full.js' % settings.STATIC_URL
# ELFINDER_WIDGET_CSS_URL = '%scss/jquery.elfinder-widget.full.css' % settings.STATIC_URL
ELFINDER_WIDGET_JS_URL = ''
ELFINDER_WIDGET_CSS_URL = ''

ELFINDER_LANGUAGES_ROOT_URL = getattr(settings, 'ELFINDER_LANGUAGES_ROOT_URL', '%selfinder/js/i18n/' % settings.STATIC_URL)

#The available language codes. A corresponding ELFINDER_LANGUAGES_ROOT_URL/elfinder.{ext}.js url must be available  
ELFINDER_LANGUAGES = getattr(settings, 'ELFINDER_LANGUAGES', ['ar', 'bg', 'ca', 'cs', 'de', 'el', 'es', 'fa', 'fr', 'hu', 'it', 'jp', 'ko', 'nl', 'no', 'pl', 'pt_BR', 'ru', 'tr', 'zh_CN'])

ELFINDER_CONNECTOR_OPTION_SETS = {
    #the default keywords demonstrates all possible configuration options
    #it allowes all file types, except from hidden files
    'default' : {
        'debug' : True, #optionally set debug to True for additional debug messages
        'roots' : [ 
            {
                'id' : 'lff',
                'driver' : ElfinderVolumeLocalFileSystem,
                'path' : settings.MEDIA_ROOT,  # 使用settings中的MEDIA_ROOT
                'alias' : '系统文件',
                'URL' : settings.MEDIA_URL,  # 使用settings中的MEDIA_URL
                'uploadAllow' : ['all'],
                'uploadDeny' : [],
                'uploadOrder' : ['allow', 'deny'],
                'accessControl' : fs_standard_access,
                'attributes' : [
                    {
                        'pattern' : r'\.tmb$',
                        'read' : True,
                        'write': True,
                        'hidden' : True,
                        'locked' : True
                    },
                ],
            }
        ]
    },
    
    # 添加与URL匹配的mfile选项集，使用与default相同的配置
    'mfile' : {
        'debug' : True,
        'roots' : [ 
            {
                'id' : 'lff',
                'driver' : ElfinderVolumeLocalFileSystem,
                'path' : settings.MEDIA_ROOT,
                'alias' : '系统文件',
                'URL' : settings.MEDIA_URL,
                'uploadAllow' : ['all'],
                'uploadDeny' : [],
                'uploadOrder' : ['allow', 'deny'],
                'accessControl' : fs_standard_access,
                'attributes' : [
                    {
                        'pattern' : r'\.tmb$',
                        'read' : True,
                        'write': True,
                        'hidden' : True,
                        'locked' : True
                    },
                ],
            }
        ]
    },
    
    #option set to only allow image files
    # 'image' : {
    #     'debug' : True,
    #     'roots' : [
    #         {
    #             'id' : 'imageid',
    #             'driver' : ElfinderVolumeLocalFileSystem,
    #             'path' : join(settings.MEDIA_ROOT, u'images'),
    #             'alias' : 'Elfinder images',
    #             'URL' : '%simages/' % settings.MEDIA_URL,
    #             'onlyMimes' : ['image',],
    #             'uploadAllow' : ['image',],
    #             'uploadDeny' : ['all',],
    #             'uploadMaxSize' : '128m',
    #             'disabled' : ['mkfile', 'archive'],
    #             'accessControl' : fs_standard_access,
    #             'attributes' : [
    #                 {
    #                     'pattern' : r'\.tmb$',
    #                     'read' : True,
    #                     'write': True,
    #                     'hidden' : True,
    #                     'locked' : True
    #                 },
    #             ],
    #         }
    #     ]
    # },
    # 'pdf':{
    #     'debug':True,
    #     'roots':[
    #         {
    #             'id' : 'pdf',
    #             'driver' : ElfinderVolumeLocalFileSystem,
    #             'path' : join(settings.MEDIA_ROOT, u'pdf'),
    #             'alias' : 'pdf',
    #             'URL' : '%spdf/' % settings.MEDIA_URL,
    #             'onlyMimes' : ['application/pdf',],
    #             'uploadAllow' : ['application/pdf',],
    #             'uploadDeny' : ['all',],
    #             'uploadMaxSize' : '128m',
    #             'disabled' : ['mkfile', 'archive'],
    #             'accessControl' : fs_standard_access,
    #             'attributes' : [
    #                 {
    #                     'pattern' : r'\.tmb$',
    #                     'read' : True,
    #                     'write': True,
    #                     'hidden' : True,
    #                     'locked' : True
    #                 },
    #             ],
    #         }
    #     ]
    #     },
    # sftp选项集已删除    
}

ELFINDER_CONNECTOR_OPTION_SETS.update(getattr(settings, 'ELFINDER_CONNECTOR_OPTION_SETS', {}))
