
初探django-charade在centos7下部署并演示使用virtualenv（可选）
====================
2016/1/15

#一、演示如何使用virtualenv（如果不需要，请跳到第二节）

prepare
-------
1. pip+virtualenv+django ::

        [root@tvm001 ~]# yum install python-pip
        [root@tvm001 ~]# pip install virtualenvwrapper
        [root@tvm001 ~]# mkdir /opt/.virtualenvs /opt/.pyprojects
        [root@tvm001 ~]# echo 'export WORKON_HOME=/opt/.virtualenvs' >>~/.bashrc
        [root@tvm001 ~]# echo 'export PROJECT_HOME=/opt/.pyprojects' >>~/.bashrc
        [root@tvm001 ~]# echo 'source /usr/bin/virtualenvwrapper.sh' >>~/.bashrc
    
        [root@tvm001 ~]# source ~/.bashrc
        [root@tvm001 ~]# mkproject django_web
        (django_web)[root@tvm001 django_web]# pip install django


2. 调整 project setting ::

        (django_web)[root@tvm001 django_web]# django-admin startproject www
        (django_web)[root@tvm001 django_web]# cd www
        (django_web)[root@tvm001 www]# vim www/settings.py
        增加app，调整语言和时区，配置文件最后增加static目录的路径 
            INSTALLED_APPS = [
                (omitted)
                'charade',
                'polls',
            ]
            LANGUAGE_CODE = 'zh-cn'
            TIME_ZONE = 'Asia/Shanghai' 

3. 拷贝上述2个app的代码到project目录下 ::

    (omitted)

4. 调整 project urls ::

        (django_web)[root@tvm001 www]# vim www/urls.py
            from django.conf.urls import url, include
            from django.contrib import admin
            from charade import views
    
            urlpatterns = [
                url(r'^$', views.index, name='index'),
                url(r'^charade/', include('charade.urls', namespace='charade')),
                url(r'^polls/', include('polls.urls', namespace='polls')),
                url(r'^admin/', include(admin.site.urls)),

5. 生成数据库 ::

        (django_web)[root@tvm001 www]# python manage.py migrate
        (django_web)[root@tvm001 www]# python manage.py makemigrations charade
        (django_web)[root@tvm001 www]# python manage.py sqlmigrate charade 0001
        (django_web)[root@tvm001 www]# python manage.py makemigrations polls
        (django_web)[root@tvm001 www]# python manage.py sqlmigrate polls 0001
        (django_web)[root@tvm001 www]# python manage.py migrate

6. 试着运行一下 ::

        (django_web)[root@tvm001 www]# python manage.py runserver 0.0.0.0:80
    测试基本功能，例如，我们用到了：pytz，需要安装，否则会报错：
    
        Exception Type:	ImproperlyConfigured
        Exception Value:	
        This query requires pytz, but it isn't installed.
        (django_web)[root@tvm001 www]# pip install pytz     
    
    确认后台的数据读写无异常后，停止运行，后续将使用uwsgi来管理。


7. admin后台 ::

        (django_web)[root@tvm001 www]# python manage.py createsuperuser
        http://0.0.0.0/admin/


8. debug ::

        DEBUG=False，则django不处理静态文件，此时应该配置nginx或apache来处理静态文件。


uwsgi+supervisord+nginx
----------------------
1. 安装 ::

        [root@tvm001 ~]# yum install nginx python-devel
        [root@tvm001 ~]# yum groupinstall "development tools"
        [root@tvm001 ~]# pip install supervisor
        [root@tvm001 ~]# whereis supervisord
        supervisord: /usr/bin/supervisord /etc/supervisord.conf
        
        (django_web)[root@tvm001 www]# pip install uwsgi
        (django_web)[root@tvm001 www]# whereis uwsgi
        uwsgi: /opt/.virtualenvs/django_web/bin/uwsgi    

2. 配置 ::

    1) 关闭django项目的 DEBUG 选项，并设置 ALLOWED_HOSTS 和 STATIC_ROOT ：
    
        (django_web)[root@tvm001 www]# vim www/settings.py
        DEBUG = False
        
        ALLOWED_HOSTS = ['*']
        
        STATIC_ROOT = os.path.join(BASE_DIR,'static')
    
    2) 收集django项目的static文件：
    
        (django_web)[root@tvm001 www]# python manage.py collectstatic
    
    3) 使用supervisor来管理uwsgi服务，用uwsgi来运行django：
    
        [root@tvm001 ~]# # echo_supervisord_conf > /etc/supervisord.conf \
        && mkdir /etc/supervisor.d \
        && echo -e '[include]\nfiles=/etc/supervisor.d/*.ini' >>/etc/supervisord.conf \
        && grep ^[^\;] /etc/supervisord.conf
        
        [root@tvm001 ~]# whereis supervisord
    
    4) 启动 supervisord 服务：
    
        [root@tvm001 ~]# /usr/bin/supervisord -c /etc/supervisord.conf
        [root@tvm001 ~]# echo '/usr/bin/supervisord -c /etc/supervisord.conf' >>/etc/rc.local
    
    5) 配置uwsgi服务：
    
        [root@tvm001 ~]# cat /etc/supervisor.d/uwsgi.ini 
        [program:uwsgi]
        command=/opt/.virtualenvs/django_web/bin/uwsgi --socket 127.0.0.1:8090 --chdir /opt/.pyprojects/django_web/www --module www.wsgi
        
    6）启动 uwsgi 服务：
    
        [root@tvm001 ~]# supervisorctl reload
        Restarted supervisord
        [root@tvm001 ~]# supervisorctl status
        uwsgi                            RUNNING   pid 22023, uptime 0:00:05
    
        说明：
        uwsgi 使用 --socket 方式，表示：通过socket来访问，因此后续可以用 nginx uwsgi 模块来访问。
        uwsgi 使用 --http 方式，表示：可以直接通过 http访问，因此后续可以用 nginx proxy 来访问。
    
    
    7) 使用nginx来处理静态文件和转发请求到后端的uwsgi服务
    
        a）nginx uwsgi
        [root@tvm001 ~]# cat /etc/nginx/conf.d/www.conf 
        server {
            listen 80 default;
            server_name www.test.com;
            charset utf-8;
        
            location /static {
                alias /opt/.pyprojects/django_web/www/static;
            }
        
            location / {
                uwsgi_pass 127.0.0.1:8090;
                include uwsgi_params;
            }
        }
        
        b）nginx proxy
        [root@tvm001 ~]# cat /etc/nginx/conf.d/www.conf 
        upstream backend {
            server 127.0.0.1:8090;
        }
        
        server {
            listen 80 default;
            server_name www.test.com;
            charset utf-8;
            
            location /static {
                alias /opt/.pyprojects/django_web/www/static;
            }
        
            location / {
                proxy_pass http://backend;
            }
        }
        
        (centos7)
        [root@tvm001 ~]# systemctl start nginx.service
        [root@tvm001 ~]# systemctl enable nginx.service

        
#二、演示直接部署
------------------------------------------------------------------------------

prepare
-------
1. pip+django ::

        [root@tvm001 ~]# yum install python-pip
        [root@tvm001 ~]# pip install django


2. 调整 project setting ::

        [root@tvm001 ~]# cd /opt
        [root@tvm001 opt]# django-admin startproject www
        [root@tvm001 opt]# cd www
        [root@tvm001 www]# vim www/settings.py
        增加app，调整语言和时区，配置文件最后增加static目录的路径 
            INSTALLED_APPS = [
                (omitted)
                'charade',
                'polls',
            ]
            LANGUAGE_CODE = 'zh-cn'
            TIME_ZONE = 'Asia/Shanghai' 

3. 拷贝上述2个app的代码到project目录下 ::

    (omitted)

4. 调整 project urls ::

        [root@tvm001 www]# vim www/urls.py
            from django.conf.urls import url, include
            from django.contrib import admin
            from charade import views
    
            urlpatterns = [
                url(r'^$', views.index, name='index'),
                url(r'^charade/', include('charade.urls', namespace='charade')),
                url(r'^polls/', include('polls.urls', namespace='polls')),
                url(r'^admin/', include(admin.site.urls)),

5. 生成数据库 ::

        [root@tvm001 www]# python manage.py migrate
        [root@tvm001 www]# python manage.py makemigrations charade
        [root@tvm001 www]# python manage.py sqlmigrate charade 0001
        [root@tvm001 www]# python manage.py makemigrations polls
        [root@tvm001 www]# python manage.py sqlmigrate polls 0001
        [root@tvm001 www]# python manage.py migrate

6. 试着运行一下 ::

        [root@tvm001 www]# python manage.py runserver 0.0.0.0:80
    测试基本功能，例如，我们用到了：pytz，需要安装，否则会报错：
    
        Exception Type:	ImproperlyConfigured
        Exception Value:	
        This query requires pytz, but it isn't installed.
        [root@tvm001 www]# pip install pytz     
    
    确认后台的数据读写无异常后，停止运行，后续将使用uwsgi来管理。


7. admin后台 ::

        [root@tvm001 www]# python manage.py createsuperuser
        http://0.0.0.0/admin/


8. debug ::

        DEBUG=False，则django不处理静态文件，此时应该配置nginx或apache来处理静态文件。


uwsgi+supervisord+nginx
----------------------
1. 安装 ::

        [root@tvm001 www]# yum install nginx python-devel
        [root@tvm001 www]# yum groupinstall "development tools"
        [root@tvm001 www]# pip install supervisor
        [root@tvm001 www]# whereis supervisord
        supervisord: /usr/bin/supervisord /etc/supervisord.conf
        
        [root@tvm001 www]# pip install uwsgi
        [root@tvm001 www]# whereis uwsgi
        uwsgi: /usr/bin/uwsgi    

2. 配置 ::

    1) 关闭django项目的 DEBUG 选项，并设置 ALLOWED_HOSTS 和 STATIC_ROOT ：
    
        [root@tvm001 www]# vim www/settings.py
        DEBUG = False
        
        ALLOWED_HOSTS = ['*']
        
        STATIC_ROOT = os.path.join(BASE_DIR,'static')
    
    2) 收集django项目的static文件：
    
        [root@tvm001 www]# python manage.py collectstatic
    
    3) 使用supervisor来管理uwsgi服务，用uwsgi来运行django：
    
        [root@tvm001 www]# # echo_supervisord_conf > /etc/supervisord.conf \
        && mkdir /etc/supervisor.d \
        && echo -e '[include]\nfiles=/etc/supervisor.d/*.ini' >>/etc/supervisord.conf \
        && grep ^[^\;] /etc/supervisord.conf
        
        [root@tvm001 www]# whereis supervisord
    
    4) 启动 supervisord 服务：
    
        [root@tvm001 www]# /usr/bin/supervisord -c /etc/supervisord.conf
        [root@tvm001 www]# echo '/usr/bin/supervisord -c /etc/supervisord.conf' >>/etc/rc.local
    
    5) 配置uwsgi服务：
    
        [root@tvm001 www]# cat /etc/supervisor.d/uwsgi.ini 
        [program:uwsgi]
        command=/usr/bin/uwsgi --socket 127.0.0.1:8090 --chdir /opt/www --module www.wsgi
        
    6）启动 uwsgi 服务：
    
        [root@tvm001 www]# supervisorctl reload
        Restarted supervisord
        [root@tvm001 www]# supervisorctl status
        uwsgi                            RUNNING   pid 22133, uptime 0:00:05
    
        说明：
        uwsgi 使用 --socket 方式，表示：通过socket来访问，因此后续可以用 nginx uwsgi 模块来访问。
        uwsgi 使用 --http 方式，表示：可以直接通过 http访问，因此后续可以用 nginx proxy 来访问。
    
    
    7) 使用nginx来处理静态文件和转发请求到后端的uwsgi服务
    
        a）nginx uwsgi
        [root@tvm001 www]# cat /etc/nginx/conf.d/www.conf 
        server {
            listen 80 default;
            server_name www.test.com;
            charset utf-8;
        
            location /static {
                alias /opt/www/static;
            }
        
            location / {
                uwsgi_pass 127.0.0.1:8090;
                include uwsgi_params;
            }
        }
        
        b）nginx proxy
        [root@tvm001 www]# cat /etc/nginx/conf.d/www.conf 
        upstream backend {
            server 127.0.0.1:8090;
        }
        
        server {
            listen 80 default;
            server_name www.test.com;
            charset utf-8;
            
            location /static {
                alias /opt/www/static;
            }
        
            location / {
                proxy_pass http://backend;
            }
        }
        
        (centos7)
        [root@tvm001 www]# systemctl start nginx.service
        [root@tvm001 www]# systemctl enable nginx.service
