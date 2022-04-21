from django.urls import path, include
from . import view
from rest_framework.routers import DefaultRouter


'''
ここで、UrlパスとViewの紐付けをする。

ModelViewSetの場合 と、genericsの汎用Viewを使った場合とで、
UrlとViewの紐付けのやり方が異なる

ModelViewSetの場合は、ここでimportしたRouterというものを使う
genericsの汎用Viewの場合は、 urlpatterns = [] の中に登録する。
views.pyから作成したviewを呼び出して、.as_view() を付けてやる。

また、router = DefaultRouter() も、urlpatterns に登録する。
'''

app_name = 'user'

router = DefaultRouter()
router.register('profile', view.ProfileViewSet)
router.register('post', viewsPostViewSet)
router.register('comment', views.CommentViewSet)

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
    path('', include(router.urls)) # router を登録している。
]

