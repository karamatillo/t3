from django.urls import path
from .views import profiles_view, banner_view, slider_view, about_view, information_view, team_view, category_view, tag_view, single_post, \
    send_post, send_video, saved_post, contactus_view, single_category, profile_edit_view, top_post_view, trend_post_view, popular_post_view

urlpatterns = [
    path('get-profiles/', profiles_view),
    path('edit-profile/<int:pk>/', profile_edit_view),
    path('get-banner/', banner_view),
    path('get-slider/', slider_view),
    path('get-about/', about_view),
    path('get-info/', information_view),
    path('get-team/', team_view),
    path('get-category/', category_view),
    path('single-category/<int:pk>/', single_category),
    path('get-tag/', tag_view),
    path('singlepost/<int:pk>/', single_post),
    path('send-post/', send_post),
    path('send-video/', send_video),
    path('saved-post/', saved_post),
    path('create-contact/', contactus_view),
    path('top-post/', top_post_view),
    path('trend-post/', trend_post_view),
    path('get-popular-post/', popular_post_view)
]

