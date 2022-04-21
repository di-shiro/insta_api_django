from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from . import serializers
from .models import Profile, Post, Comment


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)
'''
Userの新規作成は、まだUser登録していない利用者でも受け付けなければならないので、
permission_classesaを AllowAny としている。

また、このクラスは新規作成なので、 Profile.objects.all() で全てのオブジェクトを取得する必要がない
'''

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all() # これを書く必要があるらしい。
    serializer_class = serializers.ProfileSerializer # serializerの割当

    def perform_create(self, serializer):
        serializer.save(userProfile=self.request.user)
'''
ProfileViewSetは新規作成(CREATE)や更新(UPDATE)といった複数の機能が必要なので、
CRUDの４つ全てを扱える ModelViewSet を継承している。

perform_createは、新規作成をする時に呼ばれるメソッドで、予め作られている。今回はこれをOverrideしてカスタマイズしている。
現在ログインしているユーザ情報を使ってuserProfileを作成している。
UserSerializerクラスの extra_kwargsに指定した userProfile に現在のLoginUserをセットしている。z
'''


class MyProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        return self.queryset.filter(userProfile=self.request.user)
'''
ログインしているUserのProfile情報を返してくれるView
genericsの ListAPIViewを継承している。

get_querysetの
.queryset.filter(userProfile=self.request.user)
で、querysetの中にある複数のUserリストの内、現在ログインしているUserをfilterする。
'''


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        serializer.save(userPost=self.request.user)
'''
userPost=self.request.user で、userPostに現在ログインしているUserを設定している

'''

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.save(userComment=self.request.user)
'''
userComment=self.request.user によって、
コメントを作成する際に、
userCommentに ログインしているUserを自動で割り当てて
Commentオブジェクトを作成している。
'''





