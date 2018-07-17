from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserInfo(AbstractUser):
    #通常我们都是继承自models模块的Model类,
    #而这里AbstractUser往上追溯,其也是继承自models模块的Model类,
    """
    用户信息
    """
    nid = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.FileField(upload_to='avatars/', default="avatars/default.png")
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    # 如何理解verbose_name?
    #官网解释A human-readable name for the field.

    blog = models.OneToOneField(to='Blog', to_field='nid', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Blog(models.Model):
    """
    博客信息
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site_name = models.CharField(verbose_name='站点名称', max_length=64)
    theme = models.CharField(verbose_name='博客主题', max_length=32)

    def __str__(self):
        return self.title


class Category(models.Model):
    """
    博主个人文章分类表
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid', on_delete=models.CASCADE)
    #how to 快速理解ForeignKey,
    #即定义外键的表为多,关联的表为一,
    #因为一被写了多次,所以单独写成表后,就只需要写一次,

    def __str__(self):
        return self.title


class Article(models.Model):

    nid = models.AutoField(primary_key=True)
    # 你不自己建个主键,django也会建,不如自己建个,更清楚结构
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章描述')
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    # auto_now_add,这个选择值得注意下
    content = models.TextField()

    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)


    user = models.ForeignKey(verbose_name='作者', to='UserInfo', to_field='nid', on_delete=models.CASCADE)
    category = models.ForeignKey(to='Category', to_field='nid', null=True, on_delete=models.CASCADE)
    # 上面两个外键,在添加article的时候,django自带的admin就会提示我们添加对应的数据,
    #但是下面这个自定义表的多对多关系,admin就不提示我们了,需要我们自己显示的添加.
    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
    )


    def __str__(self):
        return self.title


class Article2Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid', on_delete=models.CASCADE)
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid', on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]

    def __str__(self):
        v = self.article.title + "---" + self.tag.title
        return v


class ArticleUpDown(models.Model):
    """
    点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInfo', null=True, on_delete=models.CASCADE)
    article = models.ForeignKey("Article", null=True, on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True)



class Comment(models.Model):
    """
    评论表
    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid', on_delete=models.CASCADE)
    # 一篇文章可能有多个评论
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid', on_delete=models.CASCADE)
    #是用户发布评论,同时一个用户发布多个评论,
    content = models.CharField(verbose_name='评论内容', max_length=255)
    #评论会限制字数,大概和它有关,
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    parent_comment = models.ForeignKey('Comment', null=True, on_delete=models.CASCADE,blank=True)
    #这里是追评,
    #这里的写法,省略了to关键字,

    def __str__(self):
        return self.content


