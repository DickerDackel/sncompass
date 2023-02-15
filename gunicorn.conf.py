wsgi_app                          = 'sncompass.server:create_app()'
bind                              = ['0.0.0.0:8080']
workers                           = 4
reload                            = True

accesslog                         = '-'
errorlog                          = '-'
