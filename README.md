# blog

You need to add an environment variable file in root directory named .env.In general,it should contain following items.

#!/bin/sh

SECRET_KEY = 'difficult to guess secrect'

BLOG_ADMIN = 'example@email.com'

BLOG_MAIL_SENDER = 'BLOG manager example@email.com'

MAIL_USERNAME = 'example@email.com'

MAIL_PASSWORD = 'yourpassword'

DEV_SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@IP:port/dev_blog?charset=utf8'

TEST_SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@IP:port/test_blog?charset=utf8'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@IP:port/blog?charset=utf8'
