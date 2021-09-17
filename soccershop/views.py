import http

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Product, Size
from .form import ReviewForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request,
                  'soccershop/product/list.html',
                  {'page': page,
                   'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    quantity_options = [(i, str(i)) for i in range(1, 21)]
    size_options = Size.objects.filter(sizetype=product.syzetype)
    # Список активных комментариев для этой статьи.
    reviews = product.reviews.filter(active=True)
    new_review = None
    if request.user.is_authenticated:
        init_name = request.user.username
        init_email = request.user.email
    if request.method == 'POST':
        # Пользователь отправил комментарий.
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            # Создаем комментарий, но пока не сохраняем в базе данных.
            new_review = review_form.save(commit=False)
            # Привязываем комментарий к текущей статье.
            new_review.product = product
            # Сохраняем комментарий в базе данных.
            new_review.save()
            review_form = ReviewForm(initial={'name': init_name,
                                              'email': init_email})
    else:
        if request.user.is_authenticated:
            review_form = ReviewForm(initial={'name': init_name,
                                              'email': init_email})

        else:
            review_form = ReviewForm()
    return render(request,
                  'soccershop/product/details.html',
                  {'product': product,
                   'quantity_options': quantity_options,
                   'size_options': size_options,
                   'reviews': reviews,
                   'new_review': new_review,
                   'review_form': review_form})
