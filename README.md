# gitlab 集成 omniauth-qq-connect

gitlab 默认集成了`github,google,twitter,facebook`等三方认证登录，但如果需要集成国内的`QQ,weibo`等，必须[Using Custom Omniauth Providers.](https://github.com/gitlabhq/gitlabhq/blob/master/doc/integration/omniauth.md)

**注意:** 系统环境：Ubuntu 14.04 gitlab版本：8.2.0 建议整个安装和集成过程都修改ruby官方源为[阿里云ruby源.](http://mirrors.aliyun.com/help/rubygems)

## gitlab 安装与集成 omniauth-qq-connect
参照gitlab[源码安装文档](https://github.com/gitlabhq/gitlabhq/blob/master/doc/install/installation.md)，安装进行在**第七步**`Install Gems`之前，可以集成[omniauth-qq-connect](https://github.com/kaichen/omniauth-qq-connect)，GFW墙内用户必须修改ruby官方源为[阿里云ruby源.](http://mirrors.aliyun.com/help/rubygems)

修改gitlab应用Gemfile文件，修改ruby官方源为阿里云ruby源，集成[omniauth-qq-connect:](https://github.com/kaichen/omniauth-qq-connect)

```
source 'http://mirrors.aliyun.com/rubygems/'
gem 'omniauth-qq-connect'
``` 

继续**第七步**`Install Gems`处安装：

```
# For PostgreSQL (note, the option says "without ... mysql")
sudo -u git -H bundle install --deployment --without development test mysql aws kerberos

# Or if you use MySQL (note, the option says "without ... postgres")
sudo -u git -H bundle install --deployment --without development test postgres aws kerberos
```

修改gitlab应用`config/gitlab.yml`文件，修改`OmniAuth settings:`

```
providers:
       - { name: 'qq_connect',
           app_id: 'xxxx',
           app_secret: 'xxxx' }
```

## 单独集成 omniauth-qq-connect
修改gitlab应用Gemfile文件，修改ruby官方源为阿里云ruby源，集成[omniauth-qq-connect:](https://github.com/kaichen/omniauth-qq-connect)

```
source 'http://mirrors.aliyun.com/rubygems/'
gem 'omniauth-qq-connect'

# bundle install
bundle install --without development test mysql --path vendor/bundle --no-deployment
``` 

## QQ登录回调报错：

```
Sign-in failed because email is invalid,notification_email is invalid.
```

这是因为默认gitlab注册会校验邮件地址格式合法性。gitlab qq登录默认会根据qq昵称生成对应的email。所以在校验email的时候就会失败，登录也就随之失败了。

解决方法：修改email生成器`lib/gitlab/o_auth/auth_hash.rb:`

```
def generate_temporarily_email()
        "temp-email-for-oauth-#{Time.now.to_i}@gitlab.localhost"
      end
```

写在最后，打docker,docker启动参数如下：

```
docker run --detach \
    --hostname gitlab.test.com \
    --publish 2222:22 --publish 8043:443 \
    --name gitlab \
    --restart always \
    --volume /data/gitlab/postgres:/var/lib/postgresql/9.3/main \
    --volume /data/gitlab/repositories:/home/git/repositories \
    gitlab /boot.sh
```
