from decimal import Decimal
from django.conf import settings
from soccershop.models import Product


class Cart(object):

    def __init__(self, request):
        """Инициализация объекта корзины."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем в сессии пустую корзину.
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """Проходим по товарам корзины и получаем соответствующие объекты"""
        product_ids = self.cart.keys()
        # Получаем объекты модели Product и передаем их в корзину.
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for item_key in cart.keys():
            cart[item_key]['product'] = products.get(id=item_key[0])
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            for size_item in item['size_items'].values():
                size_item['total_price'] = \
                    item['price'] * size_item['quantity']
            yield item

    def __len__(self):
        """Возвращает общее количество товаров в корзине."""
        count = 0
        for item in self.cart.values():
            for size_item in item['size_items'].values():
                count += size_item['quantity']

        return count

    def add(self, product, quantity=1, size=None):
        """Добавление товара в корзину."""
        product_id = str(product.id)
        product_was_never_added = True
        for key in self.cart.keys():
            if key == product_id:
                product_was_never_added = False
                break

        if product_was_never_added:
            self.cart[product_id] = {'size_items': {},
                                     'price': str(product.price)}

        size_never_added = True
        for size_item in self.cart[product_id]['size_items'].keys():
            if size_item == size:
                size_never_added = False

        if size_never_added:
            self.cart[product_id]['size_items'][size] = {'quantity': quantity}
        else:
            self.cart[product_id]['size_items'][size]['quantity'] += quantity

        self.save()

    def save(self):
        """Помечаем сессию как измененную."""
        self.session.modified = True

    def remove(self, product, size):
        """Удаление товара из корзины."""
        product_id = str(product.id)
        if product_id in self.cart:
            if size in self.cart[product_id]['size_items']:
                del self.cart[product_id]['size_items'][size]
            self.save()

    def get_total_price(self):
        """Вычисление общей стоимости товаров в корзине."""
        total = 0
        for item in self.cart.values():
            for size_item in item['size_items'].values():
                total += Decimal(item['price']) * size_item['quantity']

        return total

    def clear(self):
        """Очистка корзины."""
        del self.session[settings.CART_SESSION_ID]
        self.save()
