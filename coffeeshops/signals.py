from django.core.mail import send_mail


from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from coffeeshops.models import  CafeOwner, CoffeeShop, CoffeeShopAddress, Drink
from utils import create_slug
@receiver(post_save, sender=CafeOwner)
def send_new_owner_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'New Cafe Owner',
            'A new cafe owner has joined named'+ instance.full_name,
            'send@test.com',
            ['reciver@test.com'],
            fail_silently=False,
        )
@receiver(pre_save, sender=CoffeeShop)
def slugify_coffee_shop(sender, instance, **kwargs):

    print(instance.slug)
    if not instance.slug:
        print(instance.slug)
        instance.slug = create_slug(instance=instance,slugify_field="name")
@receiver(post_save, sender=CoffeeShop)
def add_default_address(sender, created, instance, **kwargs):
    if created and not instance.location:
        defaultLocation = CoffeeShopAddress.objects.create(coffee_shop=instance)
        instance.location = defaultLocation
        instance.save()
@receiver(post_delete, sender=CoffeeShopAddress)
def restore_default_address(sender, instance, **kwargs):
    coffee_shop = instance.coffee_shop

    newAddress = CoffeeShopAddress.objects.create(coffee_shop= instance)
    coffee_shop.location = newAddress
    coffee_shop.save()


@receiver(pre_save, sender=Drink)
def slugify_coffee_shop(sender, instance, **kwargs):
    if instance.stock_count > 0:
        instance.is_out_of_stock = False
    else:
        instance.is_out_of_stock = True

