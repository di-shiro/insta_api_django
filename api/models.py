from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUsermanager, PermissionsMixin
from django.conf import settings

'''
# Profileクラスで使う関数
引数:
    instance: この関数を利用するProfileのインスタンスを受け取る
    filename: フロント側のブラウザで選んだ画像のファイル名を設定
    画像はavatarsフォルダに纏めて保存する。ファイルを保存するURLを作成して returnしている。
'''
def upload_avatar_path(instance, filename):
    ext = filename.split('.')[-1] # 拡張子を取得
    return '/'.join(['avatars', str(instance.userProfile.id)+str(instance.nickName)+str(".")+str(ext)])


def upload_post_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['posts', str(instance.userPost.id)+str(instance.title)+str(".")+str(ext)])



    # このクラスは、Djangoに標準で用意されている。
class UserManager(BaseUserManager):
    # これをOverRideして機能を拡張する。
    # 下のcreate_user関数は、初期状態(default)では第２引数がusernameでpasswordが必須だが、
    # 今回はusernameをemailに変更している。
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('email is must')

        # ユーザが入力したemailを小文字にしてからuserインスタンスを作成している
        user = self.model(email=self.normalize_email(email))
        # 作成したuserに対してユーザが入力したパスワードを設定している
        # その際、元のパスワードをハッシュ化してuserに設定している
        user.set_password(password)
        # userをDBに保存している
        user.save(using=self._db)

        return user

    # admin user を作成する設定もoverrideしている
    # デフォルトではusernameだが、emailに変えている。
    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=_self._db)

        return user


# このクラスも、予めDjangoにデフォルトで（標準で）用意されているクラス。
class User(AbstractBaseUser, PermissionsMixin):
    # emailは重複できない設定にする。
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)   # Adminにログインする権限はない。

    objects = UserManager()

    # 通常、以下の設定値はusernameだが、今回は、emailでOverRideしている。
    USERNAME_FIELD = 'email'


    # 以下の __str__()によって、例えば、この Userクラス を
    # Print( User )のようにした際に、emailを文字列で返してくれる。
    def __str__(self):
        return self.email


class Profile(models.Model):
    nickName = models.CharField(max_length=20)
    userProfile = models.OneToOneField(
        # DjangoのUserモデルとProfileとを One to One で紐付ける設定
        settings.AUTH_USER_MODEL, related_name='userProfile',
        # カスケードデリートでUserが削除された時にProfileも連鎖的に削除される設定
        on_delete=models.CASCADE
    )
    # このProfileのインスタンスが作られる時の日時

    created_on = models.DateTimeField(auto_now_add=True)
    # アバター画像の
    # blank と null を Trueにすることで、アバター画像を登録しないこともできる。
    # upload_toにアバター画像の保存先のパスを設定。
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)

    def __str__(self):
        return self.nickName


class Post(models.Model):
    title = models.CharField(max_length=100)
    '''
    ユーザの投稿記事には複数のコメントをつけることができ、DBでは One to Many の関係を作る。
    これをDjangoで表現するには 以下の models.ForeignKey を用いる
    '''
    userPost = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userPost',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_post_path)
    '''
    liked はPostに「いいね!」をつける機能で、
    あるユーザが投稿したPost記事に対して、別のユーザが liked を付けることができる。
    これをDBで表現すると、「User と liked」が 「多対多 Many to Many 」の関係で結びついていると表せる。
    下の models.ManyToManyField でこれを設定している。
    '''
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked', blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=100)
    # 誰が入力したコメントなのかを記録するために、models.ForeignKey を使って
    # DjangoのUserモデルと紐付けている。
    userComment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="userComment",
        on_delete=models.CASCADE
    )
    # どのPostに対するコメントなのかを設定している。
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
