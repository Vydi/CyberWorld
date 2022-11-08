# CyberWorld

Функционал блога: 

- [Главная страница](#index) 
- [Вывод постов](#category)
- [Детальный вид поста](#details)
- [Поиск по заголовку поста](#title)
- [Вывод популярных постов](#popular)
- [Добавление комментариев к посту](#comments)
- [Регистрация](#reg)
- [Личный кабинет](#cab)
- [Создать пост](#createpost)


## <a name="index">Главная страница</a>
Главная страница
![image](https://user-images.githubusercontent.com/11966417/200554151-272bb895-31f0-46a0-9a69-75a529f20877.png)



## <a name="category">Вывод постов</a> 
Слайдер хранит в себе <a name="popular">5 популярных постов,</a>  кторые определяются кол-вом просмотров 
![image](https://user-images.githubusercontent.com/11966417/200554736-586d677c-3232-44e6-bd77-67b6d52bc449.png)

```python 
class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='url', unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    photo = models.ImageField(upload_to='posts/photos/%Y/%m/%d', blank=True, verbose_name='Фото')
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name='Тег')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.title, 'ru', reversed=True))
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('details', kwargs={"slug": self.slug})  # построение ссылки

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья(ю)'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']
        
```



```python
@register.inclusion_tag('popular_post_tpl.html')
def get_popular_post(cnt=5):
    post_pop = Post.objects.order_by('-views')[:cnt]
    print({'posts': post_pop})
    return {'posts': post_pop}

```

Все посты и <a name="title">поиск по заголовку. </a> 

![image](https://user-images.githubusercontent.com/11966417/200555275-1a7021dc-fce8-466e-9ba8-ddaa9252781f.png)

```python
class Search(ListView):
    template_name = 'blog.html'
    context_object_name = 'posts_search'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s = {self.request.GET.get('s')} &"
        return context

```
## <a name="details">Детальный вид поста</a>
![image](https://user-images.githubusercontent.com/11966417/200555406-9e08383f-1d73-41bd-aa0d-bc94178495de.png)
На этой странице пристутствует: 

### <a name="comments">Добавление комментариев к посту</a> 
Могут комментировать только зарегестрированные пользователи.
![image](https://user-images.githubusercontent.com/11966417/200555512-ed992ce0-cf25-46ec-96a7-671abc8b31aa.png)

Если авторизироваться. 

![image](https://user-images.githubusercontent.com/11966417/200555725-9b5322d6-c525-491c-b597-6d9798895f37.png)
![image](https://user-images.githubusercontent.com/11966417/200555785-fc4ce6be-e080-4b45-980e-c21d9fac3272.png)

```python
class ViewPosts(FormMixin, DetailView):
    model = Post
    context_object_name = 'posts_item'
    template_name = 'details.html'
    form_class = CommentForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()

        return context

    def post(self, request, *args, **kwargs):

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):

        post = Post.objects.get(slug=self.kwargs['slug'])

        comment = Comment(
            body=form.cleaned_data["body"],
            post=post
        )

        comment.author = self.request.user

        comment.save()
        return HttpResponseRedirect(self.request.path_info)
```

## <a name="reg">Форма регистрации</a>

![image](https://user-images.githubusercontent.com/11966417/200556381-e225348f-c5b7-4bdc-9208-d338d49bc539.png)
## <a name="cab">Личный кабинет</a>
Есть возможность редактировать имя, фамилию, ставить фото пользователя, почту, дату рождения.
![image](https://user-images.githubusercontent.com/11966417/200556446-a8bb7c5c-6b27-48ad-9362-61c9cafe8424.png)
![image](https://user-images.githubusercontent.com/11966417/200557788-23250821-767e-45ed-9c47-5ba0418d0cc1.png)


## <a name="createpost">Форма создания поста</a>
![image](https://user-images.githubusercontent.com/11966417/200557067-438ef559-736b-443b-b2aa-762cc9eb58e3.png)

