from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from rest_framework.pagination import PageNumberPagination

from .models import Category, Banner, Slider, Profile, Tag, SendPost, SendVideo, About, Team, Information, ContactUs, SavedPost
from .serializer import CategorySerializer, BannerSerializer, SliderSerializer, ProfileSerializer, TagSerializer, SendPostSerializer, SendVideoSerializer, \
    AboutSerializer, TeamSerializer, InformationSerializer, ContactUsSerializer, SavedPostSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


@api_view(['GET'])
def category_view(request):
    profiles = Category.objects.all()
    ser = CategorySerializer(profiles, many=True).data
    return Response(ser)


@api_view(['GET'])
def single_category(request, pk):
    post = SendPost.objects.filter(category_id=pk)
    pagination_class = LargeResultsSetPagination
    paginator = pagination_class()
    result_page = paginator.paginate_queryset(post, request)
    ser_data = SendPostSerializer(result_page, many=True).data
    return paginator.get_paginated_response(ser_data)


@api_view(['GET'])
def profiles_view(request):
    profiles = Profile.objects.all()
    ser = ProfileSerializer(profiles, many=True).data
    return Response(ser)


@api_view(['PATCH'])
def profile_edit_view(request, pk):
    try:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        banner = request.FILES.get('banner')
        img = request.FILES.get('img')
        old_password = request.POST.get('old_password')
        explanation = request.POST.get('explanation')
        profile = Profile.objects.get(id=pk)
        if old_password == profile.password:
            if first_name:
                profile.first_name = first_name
            if last_name:
                profile.last_name = last_name
            if email:
                profile.email = email
            if username:
                profile.username = username
            if explanation:
                profile.explanation = explanation
            if banner:
                profile.banner = banner
            if img:
                profile.img = img
            if password:
                profile.password = password
            profile.save()
            data = {
                'success': True,
                'message': "UPDATED"
            }
        else:
            data = {
                'success': False,
                'message': "INVALID PASSWORD"
            }
    except Exception as e:
        data = {
            'success': False,
            'error': f'{e}'
        }
    return Response(data)


@api_view(['GET'])
def banner_view(request):
    banner = Banner.objects.all().order_by('-id')[:2]
    ser = BannerSerializer(banner, many=True).data
    return Response(ser)


@api_view(['GET'])
def slider_view(request):
    slider = Slider.objects.all().order_by('-id')[:2]
    ser = SliderSerializer(slider, many=True).data
    return Response(ser)


@api_view(['GET'])
def about_view(request):
    about = About.objects.last()
    ser = AboutSerializer(about).data
    return Response(ser)


@api_view(['GET'])
def information_view(request):
    information = Information.objects.last
    ser = InformationSerializer(information).data
    return Response(ser)


@api_view(['GET'])
def team_view(request):
    team = Team.objects.all().order_by('-id')[:6]
    ser = TeamSerializer(team, many=True).data
    return Response(ser)


@api_view(['GET'])
def tag_view(request):
    profiles = Tag.objects.all()
    ser = TagSerializer(profiles, many=True).data
    return Response(ser)


@api_view(['GET'])
def single_post(request, pk):
    post = SendPost.objects.get(id=pk)
    category_id = post.category.id
    category = SendPost.objects.filter(category_id=category_id)
    context = {
        'Post': SendPostSerializer(post).data,
        'Related posts': SendPostSerializer(category, many=True).data
    }
    return Response(context)


@api_view(['POST'])
def send_post(request):
    try:
        author = Profile.objects.get(id=request.POST.get('author_id'))
        tag = Tag.objects.get(id=request.POST.get('tag_id'))
        category = Category.objects.get(id=request.POST.get('category_id'))
        title = request.POST.get('title')
        text = request.POST.get('text')
        img = request.FILES.get('img')
        post = SendPost.objects.create(
            author=author,
            title=title,
            text=text,
            img=img,
            category=category,
        )
        post.tag.add(tag)
        data = {
            'success': True,
            'created': SendPostSerializer(post).data,
        }
    except Exception as e:
        data = {
            'success': False,
            'error': f'{e}'
        }
    return Response(data, status=HTTP_200_OK)


@api_view(['POST'])
def send_video(request):
    try:
        author = Profile.objects.get(id=request.POST.get('author_id'))
        tag = Tag.objects.get(id=request.POST.get('tag_id'))
        title = request.POST.get('title')
        text = request.POST.get('text')
        url = request.POST.get('url')
        post = SendVideo.objects.create(
            author=author,
            title=title,
            text=text,
            url=url,
        )
        post.tag.add(tag)
        data = {
            'success': True,
            'created': SendVideoSerializer(post).data,
        }
        status = HTTP_200_OK
    except Exception as e:
        data = {
            'success': False,
            'error': f'{e}'
        }
        status = HTTP_500_INTERNAL_SERVER_ERROR
    return Response(data, status)


@api_view(['POST'])
def saved_post(request):
    try:
        author = Profile.objects.get(id=request.POST.get('author_id'))
        post = SendPost.objects.get(id=request.POST.get('post_id'))
        saved_p = SavedPost.objects.create(author=author)
        saved_p.post.add(post)
        saved_p.save()
        data = {
            'success': True,
            'saved': SavedPostSerializer(saved_p).data
        }
        status = HTTP_200_OK
    except Exception as e:

        data = {
            'success': False,
            'error': f"{e}"
        }
        status = HTTP_500_INTERNAL_SERVER_ERROR
    return Response(data, status)


@api_view(['POST'])
def contactus_view(request):
    try:
        subject = request.POST.get('subject')
        name = request.POST.get('name')
        email = request.POST.get('email')
        explanation = request.POST.get('explanation')
        file = request.POST.get('file')
        contactus = ContactUs.objects.create(
            subject=subject,
            name=name,
            email=email,
            explanation=explanation,
            file=file,
        )
        data = {
            'success': True,
            'money': ContactUsSerializer(contactus).data,
        }
        status = HTTP_200_OK
    except Exception as e:
        data = {
            'success': False,
            'error': f'{e}'
        }
        status = HTTP_500_INTERNAL_SERVER_ERROR
    return Response(data, status)


@api_view(['GET'])
def top_post_view(request):
    top_post = SavedPost.objects.all()
    ser = SavedPostSerializer(top_post, many=True)
    status = HTTP_200_OK
    return Response(ser.data, status)


@api_view(['GET'])
def trend_post_view(request):
    top_post = SavedPost.objects.all()
    ser = SavedPostSerializer(top_post, many=True)
    status = HTTP_200_OK
    return Response(ser.data, status)


@api_view(['GET'])
def popular_post_view(request):
    popular_p = SendPost.objects.all().order_by('-viewed')
    ser = SendPostSerializer(popular_p, many=True).data
    return Response(ser)
