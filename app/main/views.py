# -*- coding:utf-8 -*-
from flask import abort, flash, current_app, render_template, request, url_for, redirect, make_response, g, jsonify
from flask_login import current_user, login_required

from .. import db
from ..decorators import admin_required, permission_required
from ..main import main
from ..main.forms import EditProfileForm, EditProfileAdminForm, PostForm, CommentForm
from ..models import User, Role, Permission, Post, Comment, Topic, Relate

import re


@main.route('/index', methods=['GET', 'POST'])
def index():
    postform = PostForm()
    page = request.args.get('page', 1, type=int)
    show_followed = False
    show_mine = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
        show_mine = bool(request.cookies.get('show_mine', ''))
    if show_mine:
        pagination = current_user.posts_related.order_by(Relate.timestamp.desc()).paginate(page,
                                                                                           per_page=current_app.config[
                                                                                               'BLOG_POSTS_PER_PAGE'],
                                                                                           error_out=False)
        posts = [item.post for item in pagination.items]
    else:
        if show_followed:
            query = current_user.followed_posts
        else:
            query = Post.query
        pagination = query.order_by(Post.timestamp.desc()).paginate(page,
                                                                    per_page=current_app.config['BLOG_POSTS_PER_PAGE'],
                                                                    error_out=False)
        posts = pagination.items
    hottopics = Topic.query.order_by(Topic.count.desc()).limit(5).all()
    if current_user.is_authenticated:
        followeds = User.query.filter(User.id.in_(
            [item.followed.id for item in current_user.followed if item.followed.id != current_user.id])).order_by(
            User.last_seen.desc()).limit(9).all()
        return render_template('index.html', postform=postform, posts=posts, pagination=pagination,
                               show_followed=show_followed, show_mine=show_mine, followeds=followeds,
                               hottopics=hottopics)
    return render_template('index.html', postform=postform, posts=posts, pagination=pagination,
                           show_followed=show_followed, show_mine=show_mine, hottopics=hottopics)


@main.route('/index/search', methods=['GET', 'POST'])
def search():
    keyword = request.args.get('keyword')
    show_search = True
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
        show_mine = bool(request.cookies.get('show_mine', ''))
    if show_mine:
        pagination = current_user.posts_related.order_by(
            Relate.timestamp.desc()).paginate(page,
                                              per_page=current_app.config['BLOG_POSTS_PER_PAGE'],
                                              error_out=False)
        posts = [item.post for item in pagination.items if keyword in item.post.body]
    else:
        if show_followed:
            query = current_user.followed_posts
        else:
            query = Post.query
        pagination = query.filter(Post.body.ilike('%' + keyword + '%')).order_by(Post.timestamp.desc()).paginate(page,
                                                                                                                 per_page=
                                                                                                                 current_app.config[
                                                                                                                     'BLOG_POSTS_PER_PAGE'],
                                                                                                                 error_out=False)
        posts = pagination.items
    hottopics = Topic.query.order_by(Topic.count.desc()).limit(5).all()
    if current_user.is_authenticated:
        followeds = User.query.filter(User.id.in_(
            [item.followed.id for item in current_user.followed if item.followed.id != current_user.id])).order_by(
            User.last_seen.desc()).limit(9).all()
        return render_template('index.html', posts=posts, pagination=pagination, followeds=followeds,
                               show_search=show_search, show_followed=show_followed, show_mine=show_mine,
                               keyword=keyword,
                               hottopics=hottopics)
    return render_template('index.html', pagination=pagination, posts=posts, show_search=show_search,
                           show_followed=show_followed, show_mine=show_mine, keyword=keyword, hottopics=hottopics)


@main.route('/index/topic', methods=['GET', 'POST'])
def topic():
    postform = PostForm()
    topic = request.args.get('topic')
    show_topic = True
    page = request.args.get('page', 1, type=int)
    show_followed = False
    post_id = list()
    t = Topic.query.filter_by(title=topic).first()
    t.pv += 1
    for p in t.posts:
        post_id.append(p.id)
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
        show_mine = bool(request.cookies.get('show_mine', ''))
    if show_mine:
        pagination = current_user.posts_related.filter(Relate.post_id.in_(post_id)).order_by(Relate.timestamp.desc()).paginate(page,
                                                                                           per_page=current_app.config[
                                                                                               'BLOG_POSTS_PER_PAGE'],
                                                                                           error_out=False)
        posts = [item.post for item in pagination.items]
    else:
        if show_followed:
            query = current_user.followed_posts
        else:
            query = Post.query
        pagination = query.filter(Post.id.in_(post_id)).order_by(Post.timestamp.desc()).paginate(page,
                                                                                                 per_page=
                                                                                                 current_app.config[
                                                                                                     'BLOG_POSTS_PER_PAGE'],
                                                                                                 error_out=False)
        posts = pagination.items
    hottopics = Topic.query.order_by(Topic.count.desc()).limit(5).all()
    if current_user.is_authenticated:
        followeds = User.query.filter(User.id.in_(
            [item.followed.id for item in current_user.followed if item.followed.id != current_user.id])).order_by(
            User.last_seen.desc()).limit(9).all()
        return render_template('index.html', posts=posts, pagination=pagination, followeds=followeds,
                               show_topic=show_topic, show_followed=show_followed, show_mine=show_mine, topic=t,
                               postform=postform,
                               hottopics=hottopics)
    return render_template('index.html', pagination=pagination, posts=posts, show_topic=show_topic,
                           show_followed=show_followed, show_mine=show_mine, topic=t, postform=postform,
                           hottopics=hottopics)


@main.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    page = request.args.get('page', 1, type=int)
    posts_all = user.posts.order_by(Post.timestamp.desc())
    pagination = posts_all.paginate(
        page, per_page=current_app.config['BLOG_POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items
    collects = user.posts_collected
    follows = user.followed
    followeds = [{'user': follow.followed, 'timestamp': follow.timestamp}
                 for follow in follows]
    follows = user.followers
    followers = [{'user': follow.follower, 'timestamp': follow.timestamp}
                 for follow in follows]
    topics = set()
    for post in posts_all.all():
        for topic in post.topics:
            topics.add(topic)
            if len(topics) > 4:
                break
        if len(topics) > 4:
            break
    return render_template('user.html', user=user, posts=posts, pagination=pagination, followeds=followeds,
                           followers=followers, collects=collects, topics=topics)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash(u'您的资料已更新')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash(u'用户资料已更新')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    commentform = CommentForm()
    if commentform.validate_on_submit():
        comment = Comment(body=commentform.body.data, post=post, author=current_user._get_current_object())
        db.session.add(comment)
        r = Relate.query.filter_by(post_id=id,username=post.author.username).first()
        if r is not None:
            r.update()
        else:
            r = Relate(post_id=id,username=post.author.username)
        db.session.add(r)
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) / current_app.config['BLOG_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(page, per_page=current_app.config[
        'BLOG_COMMENTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], commentform=commentform, comments=comments)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        post.body_html = form.body.data
        db.session.add(post)
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


# @main.route('/follow/<username>')
# @login_required
# @permission_required(Permission.FOLLOW)
# def follow(username):
#     user = User.query.filter_by(username=username).first()
#     if user is None:
#         flash(u'不存在的用户')
#         return redirect(url_for('.index'))
#     if current_user.is_following(user):
#         flash(u'你已经关注了TA')
#         return redirect(url_for('.user', username=username))
#     current_user.follow(user)
#     # flash(u'现在你关注了{username}'.format(username=username))
#     return redirect(url_for('.user', username=username))

@main.route('/follow')
@login_required
@permission_required(Permission.FOLLOW)
def follow():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'不存在的用户')
        return jsonify(result=False)
    if current_user.is_following(user):
        flash(u'你已经关注了该用户')
        return jsonify(result=False)
    current_user.follow(user)
    follows = user.followers
    followers = [{'user': follow.follower, 'timestamp': follow.timestamp}
                 for follow in follows]
    return jsonify(result=True, count=len(user.followers.all()) - 1)


# @main.route('/unfollow/<username>')
# @login_required
# @permission_required(Permission.FOLLOW)
# def unfollow(username):
#     user = User.query.filter_by(username=username).first()
#     if user is None:
#         flash(u'不存在的用户')
#         return redirect(url_for('.index'))
#     if not current_user.is_following(user):
#         flash(u'该用户不在你的关注列表中')
#         return redirect(url_for('.user', username=username))
#     current_user.unfollow(user)
#     # flash(u'你不再关注{username}'.format(username=username))
#     return redirect(url_for('.user', username=username))

@main.route('/unfollow')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'不存在的用户')
        return jsonify(result=False)
    if not current_user.is_following(user):
        flash(u'该用户不在你的关注列表中')
        return jsonify(result=False)
    current_user.unfollow(user)

    return jsonify(result=True, count=len(user.followers.all()) - 1)


@main.route('/followers/<username>', methods=['GET', 'POST'])
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'不存在的用户')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['BLOG_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title=u"的粉丝",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>', methods=['GET', 'POST'])
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'不存在的用户')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['BLOG_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title=u"的关注",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/all')
@login_required
def show_all():
    keyword = request.args.get('keyword')
    if keyword is not None:
        resp = make_response(redirect(url_for('.search', keyword=keyword)))
        resp.set_cookie('show_followed', '', max_age=30 * 24 * 60 * 60)
        resp.set_cookie('show_mine', '', max_age=30 * 24 * 60 * 60)
        return resp
    topic = request.args.get('topic')
    if topic is not None:
        resp = make_response(redirect(url_for('.topic', topic=topic)))
        resp.set_cookie('show_followed', '', max_age=30 * 24 * 60 * 60)
        resp.set_cookie('show_mine', '', max_age=30 * 24 * 60 * 60)
        return resp
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30 * 24 * 60 * 60)
    resp.set_cookie('show_mine', '', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    keyword = request.args.get('keyword')
    if keyword is not None:
        resp = make_response(redirect(url_for('.search', keyword=keyword)))
        resp.set_cookie('show_followed', '1', max_age=30 * 24 * 60 * 60)
        resp.set_cookie('show_mine', '', max_age=30 * 24 * 60 * 60)
        return resp
    topic = request.args.get('topic')
    if topic is not None:
        resp = make_response(redirect(url_for('.topic', topic=topic)))
        resp.set_cookie('show_followed', '1', max_age=30 * 24 * 60 * 60)
        resp.set_cookie('show_mine', '', max_age=30 * 24 * 60 * 60)
        return resp
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30 * 24 * 60 * 60)
    resp.set_cookie('show_mine', '', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/mine')
@login_required
def show_mine():
    keyword = request.args.get('keyword')
    if keyword is not None:
        resp = make_response(redirect(url_for('.search', keyword=keyword)))
        resp.set_cookie('show_followed', '', max_age=30 * 24 * 60 * 60)
        resp.set_cookie('show_mine', '1', max_age=30 * 24 * 60 * 60)
        return resp
    topic = request.args.get('topic')
    if topic is not None:
        resp = make_response(redirect(url_for('.topic', topic=topic)))
        resp.set_cookie('show_followed', '', max_age=30 * 24 * 60 * 60)
        resp.set_cookie('show_mine', '1', max_age=30 * 24 * 60 * 60)
        return resp
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30 * 24 * 60 * 60)
    resp.set_cookie('show_mine', '1', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(page, per_page=current_app.config[
        'BLOG_COMMENTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments, pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate', page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate', page=request.args.get('page', 1, type=int)))


@main.route('/like')
@login_required
def like():
    id = request.args.get('id', 0, type=int)
    post = Post.query.filter_by(id=id).first()
    if post is None:
        flash(u'不存在的微博')
        return jsonify(result=False)
    if current_user.is_liking(post):
        flash(u'你已经赞了这篇微博')
        return jsonify(result=False)
    current_user.posts_liked.append(post)
    counts = post.users_liked.count()
    return jsonify(result=True, counts=counts)


@main.route('/unlike')
@login_required
def unlike():
    id = request.args.get('id', 0, type=int)
    post = Post.query.filter_by(id=id).first()
    if post is None:
        flash(u'不存在的微博')
        return jsonify(result=False)
    if not current_user.is_liking(post):
        flash(u'你还没有赞这篇微博')
        return jsonify(result=False)
    current_user.posts_liked.remove(post)
    counts = post.users_liked.count()
    return jsonify(result=True, counts=counts)


@main.route('/collect')
@login_required
def collect():
    id = request.args.get('id', 0, type=int)
    post = Post.query.filter_by(id=id).first()
    if post is None:
        flash(u'不存在的微博')
        return jsonify(result=False)
    if current_user.is_collecting(post):
        flash(u'你已经收藏了这篇微博')
        return jsonify(result=False)
    current_user.posts_collected.append(post)
    return jsonify(result=True)


@main.route('/uncollect')
@login_required
def uncollect():
    id = request.args.get('id', 0, type=int)
    post = Post.query.filter_by(id=id).first()
    if post is None:
        flash(u'不存在的微博')
        return jsonify(result=False)
    if not current_user.is_collecting(post):
        flash(u'你还没有收藏这篇微博')
        return jsonify(result=False)
    current_user.posts_collected.remove(post)
    return jsonify(result=True)


@main.route('/submit')
@login_required
def submit():
    body = request.args.get('post')
    text = request.args.get('text')

    body = re.sub('<p>', '', body)
    body = re.sub('</p>', '<br>', body)
    while body[-4:] == '<br>':
        body = body[:-4]
    body = '<p>' + body + '</p>'
    if current_user.can(Permission.WRITE_ARTICLES) and body is not None:
        text = re.sub(chr(160), chr(32), text)  # 将HTML的160号空格替换为32号空格
        topics = re.findall('\#([^\#|.]+)\#', text)
        relates = re.findall('\@([^\@|.]+?)\s', text)  # 非贪婪匹配
        post = Post(body=text, body_html=body, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        for topic in set(topics):
            t = Topic.query.filter_by(title=topic).first()
            if t is not None:
                t.posts.append(post)
                t.count += 1
            else:
                t = Topic(title=topic)
                t.posts.append(post)
            db.session.add(t)
        for relate in set(relates):
            if User.query.filter_by(username=relate).first() is not None:
                r = Relate.query.filter_by(username=relate, post_id=post.id).first()
                if r is not None:
                    r.update()
                else:
                    r = Relate(username=relate, post_id=post.id)
                db.session.add(r)
        db.session.commit()
        return jsonify(result=True)
    return jsonify(result=False)


@main.route('/relate')
def relate():
    username = request.args.get('username')
    if username is not None:
        if User.query.filter_by(username=username).first() is not None:
            resp = make_response(redirect(url_for('.user', username=username)))
            return resp
        else:
            resp = make_response(redirect(url_for('.search', keyword=username)))
            return resp

@main.route('/share')
@login_required
def share():
    post_id = request.args.get('post_id')
    text = request.args.get('text')
    if post_id is None or text is None:
        return jsonify(result=False)
    username = Post.query.filter_by(id=post_id).first().auth.username
    post = Post(body=text, body_html=text, author=current_user._get_current_object(),forward_id=post_id)
    db.session.add(post)
    db.session.commit()
    relate = Relate(username=username,post_id=post.id)
    db.session.add(relate)
    return jsonify(result=True)
