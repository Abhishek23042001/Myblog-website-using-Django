from django.shortcuts import render,HttpResponse,redirect
from .models import Post,BlogComment
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from blog.templatetags import extras
 

# Create your views here.
#@login_required(login_url='/')
def blogHome(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        allpost= Post.objects.all()
        context= {'allpost': allpost}
        return render(request,'blog/blogHome.html',context)

@login_required(login_url='/')
def blogPost(request,sno):
    post= Post.objects.filter(sno=sno).first()
    comments= BlogComment.objects.filter(post= post,parent=None)
    replies= BlogComment.objects.filter(post= post).exclude(parent=None) # exclude all comments where parent is none
    repDict={}
    for reply in replies:
        if reply.parent.sno not in repDict.keys():
            repDict[reply.parent.sno] = [reply]
        else:
            repDict[reply.parent.sno].append(reply)
    

    context= {'post':post,'comments': comments,'repDict':repDict}
    return render(request,'blog/blogPost.html',context)

def postComment(request):
    if request.method == 'POST': 
        replysno= request.POST.get("")  
        comment = request.POST.get("comment")
        user= request.user
    
        postsno= request.POST.get("postsno")
        post= Post.objects.get(sno= postsno)
        parentsno = request.POST.get("parentsno")
        if parentsno == "":
          comment= BlogComment(comment=comment,user=user,post=post)
          comment.save()
          messages.success(request,"Your Comment has been Posted Successfully")
        else:
          parent= BlogComment.objects.get(sno=parentsno)
          comment= BlogComment(comment=comment,user=user,post=post,parent=parent)
          comment.save()
          messages.success(request,"Your Reply has been Posted Successfully")
          
    return redirect(f"/blog/{post.sno}")
        





