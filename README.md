# SCU Robomaster 门禁系统

国际惯例，先膜黄神 :)
# build
```bash
$ pip3 install git+https://github.com/scientificRat/easy_py_server.git
```

安装`evdev`
```bash
$ apt-get install python-dev python-pip gcc
$ apt-get install linux-headers-$(uname -r)
$ pip install evdev 
```


# run
```bash
python main.py
```

# autorun
supervisord


# login
用户名及密码：
```
admin admin
```
只允许内网访问

# changelog
2018-9-8: 使用sqlite, 尝试部署在树莓派

# refer
- https://python-evdev.readthedocs.io/en/latest/install.html

Les1ie
2018-9-8 00:14:28