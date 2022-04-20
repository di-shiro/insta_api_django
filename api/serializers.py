from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Post, Comment

'''
serializerの書き方としては、
「class Meta:」のところに色々とオプションを書いていく
'''


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

''' 説明
)get_user_model :
はDjangoの標準の関数で、現在アクティブなUserModelを取得できる。
今回は、models.pyの中でカスタマイズしたUserモデルを取得することになる。

)fields :
このuserSerializerで取り扱いたいパラメータの一覧

)extra_kwargs :
fieldsに設定したパラメータの内、読み・書きなどの属性を指定できる
(write_onry, read_only, etc...)
こうすることで、例えば、下のuserSerializerの場合、
write_onlyを指定しているので、ブラウザ側からGETメソッドでアクセスしてきても、
passwordをブラウザ側に返さないことになる。

) def create :
validationを通過したデータを元に、Userオブジェクトを作成している。
createメソッドをOverrideしている。
get_user_modelはmodels.pyの中で定義したUserクラスのこと.
これに連なっている  .objects.create_user()  により、新規Userを作成してDBに追加している。
.objects は、Userモデル の中で  objects = UserManager()  として紐付けられている。
そのため、具体的には、新規Userをさくせいするために、
models.py のUserクラスからUserManagerクラスのcreate_userメソッドを呼び出して処理していることになる。

)validated_data:
例えば、「fields」に指定した email, password をブラウザ側で入力してDjango側で受け取ると、
まずValidationでチェックされる。
それを通過するとvalidated_dataにdictionary型{} で格納される。
'''

class ProfileSerializer(serializers.ModelSerializer):

    # Profileの作成日時を人が読めるフォーマットにしている。
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Profile  # Profileモデルを使う
        fields = ('id', 'nickName', 'userProfile', 'created_on', 'updated_on', 'img')
        extra_kwargs = {'userProfile': {'read_only': True}}
'''
# userProfileには、現在ログインしているUserがはいる
このLoginUserは、フロント側で指定することもできるが、煩雑になるため、Django側で指定している。

'''


class PostSerializer(serializers.ModelSerializer):
    created_on = serializers.DatetimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'title', 'userPost', 'created_on', 'img', 'liked')
        extra_kwargs = {'userPost': {'read_only': True}}
'''
extra_kwargsの userPost にはloginUser が格納される。
これについては、別に処理を作成する。
'''


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'userComment', 'post')
        extra_kwargs = {'userComment': {read_only: True}}

