from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from account.models import User
from board.models import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def board(request, p_type=None):
    current_type = None
    p_types = PostType.objects.all()
    postlist = Post.objects.all()

    page = request.GET.get('page', '1')
    if p_type:
        current_type = get_object_or_404(PostType, p_type=p_type)
        postlist = postlist.filter(p_type=current_type)

    paginator = Paginator(postlist, 16)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    comment_count = Comment.objects.all()

    return render(request, 'board/board.html', {'current_type':current_type, 'p_types': p_types, 'postlist': page_obj, 'comment_count': comment_count,})


def board_write(request):
    p_types = PostType.objects.all()
    authuser = request.session.get('authUser')
    i = User.objects.get(member_id=authuser['member_id'])
    return render(request, 'board/board_write.html', {'p_types': p_types, 'i': i,})


def board_write_post(request):
    p_types = PostType.objects.all()
    response_data = {}
    post = Post()
    authuser = request.session.get('authUser')
    i = User.objects.get(member_id=authuser['member_id'])
    post.member_id = i
    if request.POST.get('pn') == "":
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')+'?result=t_fail')
    elif request.POST.get('c') == "":
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')+'?result=c_fail')

    else:
        post.contents = request.POST.get('c')
        post.postname = request.POST.get('pn')
        t = PostType.objects.get(p_type=request.POST.get('category'))
        post.p_type = t
        post.save()
        return redirect('detail/' + str(post.id))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')+'?result=fail')


def board_delete(request, p_id):
    p = Post.objects.get(id=p_id)
    p.delete()
    return redirect('/board')


def board_edit(request, p_id):
    post = get_object_or_404(Post, id=p_id)
    authuser = request.session.get('authUser')
    i = User.objects.get(member_id=authuser['member_id'])
    p_types = PostType.objects.all()
    if request.method == 'POST':
        post.postname = request.POST.get('pn')
        post.contents = request.POST.get('c')
        if request.POST.get('category') is None:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')+'?result=type_fail')
        else:
            t = PostType.objects.get(p_type=request.POST.get('category'))
            post.p_type = t
            post.save()
        return redirect('/board/detail/' + str(post.id))
    else:
        return render(request, 'board/board_edit.html', {'post': post, 'user': i, 'p_types': p_types})


def board_detail(request, id):
    post = get_object_or_404(Post, id=id)
    authuser = request.session.get('authUser')
    i = User.objects.get(member_id=authuser['member_id'])
    p_types = PostType.objects.all()
    comment_list = Comment.objects.filter(post_id=id)
    return render(request, 'board/board_detail.html', {'post': post, 'user': i, 'p_types': p_types, 'comment_list': comment_list})


@csrf_exempt
def comment_write(request, p_id):
    authuser = request.session.get('authUser')
    i = User.objects.get(member_id=authuser['member_id'])

    if request.POST.get('comment'):
        comment = Comment()
        p = Post.objects.get(id=p_id)
        comment.post_id = p
        comment.member_id = i
        comment.comment_content = request.POST.get('comment')
        comment.save()
    return redirect('/board/detail/' + str(p_id))


def comment_delete(request, c_id):
    comment = Comment.objects.get(id=c_id)
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))