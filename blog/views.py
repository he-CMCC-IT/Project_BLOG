from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm
from taggit.models import Tag
from django.db.models import Count


# Create your views here.
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # 每页显示3篇文章
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page参数不是一个整数就返回第一页
        posts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出总页数就返回最后一页
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status="published",
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    post.explored += 1
    post.save(update_fields=['explored', ])

    # 列出文章对应的所有活动的评论
    object_list = post.comments.filter(active=True)
    total_comments = object_list
    paginator = Paginator(object_list, 5)  # 每页显示5篇评论
    page = request.GET.get('page')
    # 获取用于正确展示分页评论序号的偏移量
    if not page:
        page = 1  # 用于控制直接GET方式访问详情页，page为NoneType的情况
    page_offset = (int(page) - 1) * 5
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # 如果page参数不是一个整数就返回第一页
        comments = paginator.page(1)
    except EmptyPage:
        # 如果页数超出总页数就返回最后一页
        comments = paginator.page(paginator.num_pages)

    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # 通过表单直接创建新数据对象，但是不要保存到数据库中
            new_comment = comment_form.save(commit=False)
            # 设置外键为当前文章
            new_comment.post = post
            # 将评论数据对象写入数据库
            new_comment.save()
    else:
        comment_form = CommentForm()

    # 显示相近Tag的文章列表
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_tags = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_tags.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:3]
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'total_comments': total_comments,
                                                     'comments': comments,
                                                     'page_offset': page_offset,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts})


