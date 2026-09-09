import random
from datetime import timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.db import transaction
from django.utils import timezone

from apps.users.models import User, Address
from apps.categories.models import Category
from apps.menu.models import MenuItem
from apps.cart.models import Cart
from apps.orders.models import Order, OrderItem
from apps.reviews.models import Review
from apps.coupons.models import Coupon
from apps.payments.models import Payment
from apps.delivery.models import DeliveryPartner, DeliveryAssignment
from apps.core.constants import MANAGER_GROUP, DELIVERY_CREW_GROUP, KITCHEN_STAFF_GROUP


class Command(BaseCommand):
    help = "Seeds database with rich sample data (20-30 rows per entity) while strictly preserving User records."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting database cleanup and seeding process..."))

        with transaction.atomic():
            # 1. CLEANUP OPERATIONAL DATA ONLY (NEVER DELETE USERS!)
            self.stdout.write("Wiping operational data (Categories, Menu, Cart, Orders, Coupons, Payments, Delivery, Reviews)...")
            DeliveryAssignment.objects.all().delete()
            DeliveryPartner.objects.all().delete()
            Payment.objects.all().delete()
            OrderItem.objects.all().delete()
            Order.objects.all().delete()
            Cart.objects.all().delete()
            Review.objects.all().delete()
            MenuItem.objects.all().delete()
            Category.objects.all().delete()
            Coupon.objects.all().delete()

            # 2. SETUP GROUPS
            mgr_group, _ = Group.objects.get_or_create(name=MANAGER_GROUP)
            delivery_group, _ = Group.objects.get_or_create(name=DELIVERY_CREW_GROUP)
            kitchen_group, _ = Group.objects.get_or_create(name=KITCHEN_STAFF_GROUP)

            # Ensure existing manager user is in Manager group
            existing_manager = User.objects.filter(username="aman_gupta_manager").first()
            if existing_manager and not existing_manager.groups.filter(name=MANAGER_GROUP).exists():
                existing_manager.groups.add(mgr_group)

            # 3. ENSURE TEST USERS (Safe get_or_create, keeping existing users untouched)
            default_password = "Password123!"

            # Kitchen Staff
            kitchen_users = []
            for username, name, email, phone in [
                ("chef_mario", "Mario Rossi", "mario.chef@restaurant.com", "9811001101"),
                ("chef_gordon", "Gordon Ramsay", "gordon.chef@restaurant.com", "9811001102"),
                ("chef_vikram", "Vikram Khanna", "vikram.chef@restaurant.com", "9811001103"),
            ]:
                u, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        "first_name": name.split()[0],
                        "last_name": name.split()[-1],
                        "email": email,
                        "phone_number": phone,
                        "is_staff": True,
                    },
                )
                if created:
                    u.set_password(default_password)
                    u.save()
                u.groups.add(kitchen_group)
                kitchen_users.append(u)

            # Delivery Crew Users
            delivery_users = []
            delivery_profiles_data = [
                ("delivery_arjun", "Arjun Verma", "arjun.delivery@restaurant.com", "9822002201", "DL-01-AB-1234", "GOV-DL-88219"),
                ("delivery_deepak", "Deepak Sharma", "deepak.delivery@restaurant.com", "9822002202", "DL-04-CD-5678", "GOV-DL-77341"),
                ("delivery_rohit", "Rohit Kumar", "rohit.delivery@restaurant.com", "9822002203", "HR-26-EF-9012", "GOV-HR-44129"),
                ("delivery_kavita", "Kavita Singh", "kavita.delivery@restaurant.com", "9822002204", "UP-16-GH-3456", "GOV-UP-99382"),
            ]
            delivery_partners = []
            for username, name, email, phone, vehicle, gov_id in delivery_profiles_data:
                u, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        "first_name": name.split()[0],
                        "last_name": name.split()[-1],
                        "email": email,
                        "phone_number": phone,
                        "is_staff": False,
                    },
                )
                if created:
                    u.set_password(default_password)
                    u.save()
                u.groups.add(delivery_group)
                delivery_users.append(u)

                dp, _ = DeliveryPartner.objects.get_or_create(
                    user=u,
                    defaults={
                        "vehicle_number": vehicle,
                        "government_id": gov_id,
                        "status": DeliveryPartner.PartnerStatus.AVAILABLE,
                    },
                )
                delivery_partners.append(dp)

            # Customer Users
            customer_data = [
                ("customer_alice", "Alice", "Smith", "alice.smith@example.com", "9833003301"),
                ("customer_bob", "Bob", "Jones", "bob.jones@example.com", "9833003302"),
                ("customer_charlie", "Charlie", "Brown", "charlie.b@example.com", "9833003303"),
                ("customer_david", "David", "Miller", "david.m@example.com", "9833003304"),
                ("customer_emma", "Emma", "Watson", "emma.w@example.com", "9833003305"),
                ("customer_farhan", "Farhan", "Akhtar", "farhan.a@example.com", "9833003306"),
                ("customer_geeta", "Geeta", "Phogat", "geeta.p@example.com", "9833003307"),
                ("customer_harsh", "Harsh", "Beniwal", "harsh.b@example.com", "9833003308"),
                ("customer_ishaan", "Ishaan", "Khattar", "ishaan.k@example.com", "9833003309"),
                ("customer_jaya", "Jaya", "Bachhan", "jaya.b@example.com", "9833003310"),
                ("customer_kunal", "Kunal", "Kapoor", "kunal.k@example.com", "9833003311"),
                ("customer_lata", "Lata", "Mangeshkar", "lata.m@example.com", "9833003312"),
                ("customer_manish", "Manish", "Malhotra", "manish.m@example.com", "9833003313"),
                ("customer_nisha", "Nisha", "Rawal", "nisha.r@example.com", "9833003314"),
                ("customer_omkar", "Omkar", "Kapoor", "omkar.k@example.com", "9833003315"),
                ("customer_pooja", "Pooja", "Hegde", "pooja.h@example.com", "9833003316"),
            ]
            customer_users = []
            # Include existing user aman_gupta_user if present
            existing_user = User.objects.filter(username="aman_gupta_user").first()
            if existing_user:
                customer_users.append(existing_user)

            for username, fname, lname, email, phone in customer_data:
                u, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        "first_name": fname,
                        "last_name": lname,
                        "email": email,
                        "phone_number": phone,
                    },
                )
                if created:
                    u.set_password(default_password)
                    u.save()
                customer_users.append(u)

            # 4. ADDRESSES (Preserve existing, add new to reach 25+ addresses)
            cities = ["New Delhi", "Mumbai", "Bengaluru", "Pune", "Hyderabad", "Noida", "Gurugram"]
            for cust in customer_users:
                if cust.username == "aman_gupta_user" and cust.addresses.exists():
                    continue  # keep aman_gupta_user addresses untouched
                
                # Check if already has addresses
                if not cust.addresses.exists():
                    city = random.choice(cities)
                    Address.objects.create(
                        user=cust,
                        label="Home",
                        address=f"{random.randint(10, 999)}, Sunshine Apartments, Sector {random.randint(1, 62)}",
                        city=city,
                        state="State",
                        country="India",
                        postal_code=f"1100{random.randint(10, 99)}",
                        is_default=True,
                    )
                    # Add second address for some
                    if random.choice([True, False]):
                        Address.objects.create(
                            user=cust,
                            label="Office",
                            address=f"Tower {chr(random.randint(65, 70))}, Tech Business Park, Phase {random.randint(1, 5)}",
                            city=city,
                            state="State",
                            country="India",
                            postal_code=f"1100{random.randint(10, 99)}",
                            is_default=False,
                        )

            # 5. CATEGORIES (12 categories)
            categories_spec = [
                ("Starters & Appetizers", "Crispy, savory snacks and hot starters to kick off your dining experience."),
                ("Main Course (North Indian)", "Rich, aromatic curries and gravies cooked with traditional herbs and spices."),
                ("Biryani & Rice Bowls", "Slow-cooked dum biryanis and fragrant seasoned rice dishes."),
                ("Wood-Fired Pizzas", "Authentic hand-tossed thin crust pizzas baked to bubbly golden perfection."),
                ("Burgers & Wraps", "Juicy grilled patties, crispy fillings, fresh veggies, and toasted brioche buns."),
                ("Pastas & Italian", "Classic Italian pastas in creamy Alfredo, tangy Arrabbiata, and pesto sauces."),
                ("Asian & Wok Specialties", "Stir-fried noodles, aromatic fried rice, and sizzling oriental gravies."),
                ("Healthy Salads & Soups", "Wholesome bowls of fresh leafy greens, hearty broths, and soothing soups."),
                ("Desserts & Sweet Treats", "Decadent cakes, warm brownies, traditional sweets, and artisanal ice creams."),
                ("Beverages & Shakes", "Chilled mocktails, thick milkshakes, cold-brew coffees, and coolers."),
                ("South Indian Classics", "Crispy golden dosas, steamed idlis, and hot lentil sambar."),
                ("Breakfast Combos", "Wholesome morning combos, pancakes, waffles, and energy bowls."),
            ]
            category_objs = []
            for title, desc in categories_spec:
                cat = Category.objects.create(title=title, description=desc, is_active=True)
                category_objs.append(cat)

            # 6. MENU ITEMS (30 items)
            cat_map = {c.title: c for c in category_objs}
            menu_specs = [
                # Starters
                ("Paneer Tikka", "Cottage cheese marinated in spices, hung curd, and grilled in a clay oven.", Decimal("289.00"), "Starters & Appetizers", True, 20, 360),
                ("Crispy Corn Chaat", "Sweet corn kernels tossed with spices, lemon juice, and crispy cilantro.", Decimal("199.00"), "Starters & Appetizers", True, 15, 240),
                ("Chicken Malai Tikka", "Succulent chicken skewers marinated in cream, cashew paste, and mild spices.", Decimal("349.00"), "Starters & Appetizers", True, 25, 420),
                ("Veggie Spring Rolls", "Crispy golden rolls packed with julienned vegetables served with sweet chilli dip.", Decimal("219.00"), "Starters & Appetizers", True, 15, 290),

                # Main Course
                ("Butter Chicken", "Tender chicken simmered in a silky tomato, cashew nut, and butter gravy.", Decimal("399.00"), "Main Course (North Indian)", True, 30, 580),
                ("Dal Makhani", "Black lentils slow-cooked overnight with creamy butter and subtle aromatic spices.", Decimal("299.00"), "Main Course (North Indian)", True, 25, 450),
                ("Paneer Butter Masala", "Soft paneer cubes tossed in rich tomato gravy finished with fenugreek leaves.", Decimal("329.00"), "Main Course (North Indian)", True, 20, 510),
                ("Kadhai Chicken", "Chicken chunks cooked with crunchy bell peppers, onions, and freshly ground spices.", Decimal("379.00"), "Main Course (North Indian)", True, 25, 490),

                # Biryani
                ("Hyderabadi Chicken Biryani", "Layered basmati rice with spiced chicken, mint, saffron, served with salan and raita.", Decimal("369.00"), "Biryani & Rice Bowls", True, 30, 680),
                ("Lucknowi Veg Dum Biryani", "Fragrant basmati rice gently cooked with marinated seasonal garden vegetables.", Decimal("289.00"), "Biryani & Rice Bowls", True, 25, 520),
                ("Mutton Dum Biryani", "Prime cuts of tender lamb slow-cooked with basmati rice and royal spices.", Decimal("469.00"), "Biryani & Rice Bowls", True, 35, 750),

                # Pizzas
                ("Classic Margherita Pizza", "San Marzano tomato sauce, fresh mozzarella, and aromatic basil leaves.", Decimal("349.00"), "Wood-Fired Pizzas", True, 20, 620),
                ("Farmhouse Veggie Pizza", "Loaded with bell peppers, red onions, mushrooms, sweet corn, and black olives.", Decimal("429.00"), "Wood-Fired Pizzas", True, 25, 690),
                ("BBQ Chicken & Jalapeno Pizza", "Smoky grilled chicken pieces, spicy jalapenos, BBQ glaze, and mozzarella.", Decimal("499.00"), "Wood-Fired Pizzas", True, 25, 760),

                # Burgers
                ("Classic Cheeseburger", "Juicy grilled beef/chicken patty with melted cheddar, lettuce, tomatoes, and gherkins.", Decimal("259.00"), "Burgers & Wraps", True, 15, 540),
                ("Crispy Spicy Paneer Burger", "Crumb-coated spiced paneer patty with spicy sriracha mayo and crunchy lettuce.", Decimal("229.00"), "Burgers & Wraps", True, 15, 510),
                ("Falafel Hummus Wrap", "Crispy spiced chickpea falafels with house hummus, pickled veggies, and tahini.", Decimal("219.00"), "Burgers & Wraps", True, 15, 440),

                # Pastas
                ("Penne Creamy Alfredo", "Penne tossed in a velvety garlic parmesan cream sauce with sautéed mushrooms.", Decimal("339.00"), "Pastas & Italian", True, 20, 610),
                ("Spicy Arrabbiata Pasta", "Al dente penne in a fiery tomato basil sauce infused with garlic and red chillies.", Decimal("319.00"), "Pastas & Italian", True, 20, 480),

                # Asian
                ("Veg Hakka Noodles", "Wok-tossed noodles with shredded cabbage, carrots, bell peppers, and scallions.", Decimal("239.00"), "Asian & Wok Specialties", True, 15, 380),
                ("Chilli Chicken Gravy", "Crispy chicken cubes tossed in spicy soy-garlic sauce with peppers and onions.", Decimal("349.00"), "Asian & Wok Specialties", True, 20, 490),
                ("Vegetable Fried Rice", "Fluffy wok-tossed jasmine rice with diced veggies and toasted sesame oil.", Decimal("229.00"), "Asian & Wok Specialties", True, 15, 370),

                # Salads & Soups
                ("Classic Caesar Salad", "Crisp romaine lettuce, herb garlic croutons, parmesan shavings, and Caesar dressing.", Decimal("249.00"), "Healthy Salads & Soups", True, 12, 280),
                ("Creamy Roasted Tomato Soup", "Slow-roasted plum tomatoes blended with cream and served with crispy croutons.", Decimal("179.00"), "Healthy Salads & Soups", True, 15, 180),

                # Desserts
                ("Hot Gulab Jamun (2 Pcs)", "Soft golden milk dumplings soaked in warm fragrant cardamom sugar syrup.", Decimal("129.00"), "Desserts & Sweet Treats", True, 10, 310),
                ("Sizzling Chocolate Brownie", "Warm fudgy walnut brownie served on a hot skillet with vanilla bean ice cream.", Decimal("249.00"), "Desserts & Sweet Treats", True, 12, 520),
                ("Classic New York Cheesecake", "Creamy baked vanilla cheesecake on a graham cracker crust with berry compote.", Decimal("279.00"), "Desserts & Sweet Treats", True, 10, 460),

                # Beverages
                ("Fresh Mango Lassi", "Creamy chilled yogurt blended with sweet Alphonso mango pulp and saffron.", Decimal("149.00"), "Beverages & Shakes", True, 5, 260),
                ("Cold Brew Hazelnut Coffee", "Smooth 18-hour cold brewed artisan coffee with a hint of roasted hazelnut.", Decimal("189.00"), "Beverages & Shakes", True, 5, 140),

                # Breakfast & South Indian (one unavailable item for testing filters!)
                ("Masala Dosa with Sambar", "Crispy fermented crepe filled with spiced potatoes, served with coconut chutney.", Decimal("169.00"), "South Indian Classics", False, 15, 340),
            ]

            menu_item_objs = []
            for title, desc, price, cat_title, avail, prep_min, cals in menu_specs:
                item = MenuItem.objects.create(
                    title=title,
                    description=desc,
                    price=price,
                    category=cat_map[cat_title],
                    available=avail,
                    preparation_time=timedelta(minutes=prep_min),
                    calories=cals,
                )
                menu_item_objs.append(item)

            # 7. COUPONS (20 coupons: 10 Percentage, 10 Flat)
            now = timezone.now()
            coupon_specs = [
                # Percentage Coupons (Active)
                ("WELCOME50", Coupon.DiscountType.PERCENTAGE, Decimal("50.00"), Decimal("150.00"), Decimal("299.00"), now - timedelta(days=10), now + timedelta(days=60), True),
                ("FEAST20", Coupon.DiscountType.PERCENTAGE, Decimal("20.00"), Decimal("100.00"), Decimal("499.00"), now - timedelta(days=5), now + timedelta(days=45), True),
                ("SAVER15", Coupon.DiscountType.PERCENTAGE, Decimal("15.00"), Decimal("75.00"), Decimal("350.00"), now - timedelta(days=3), now + timedelta(days=30), True),
                ("MEGA30", Coupon.DiscountType.PERCENTAGE, Decimal("30.00"), Decimal("200.00"), Decimal("799.00"), now - timedelta(days=2), now + timedelta(days=20), True),
                ("WEEKEND25", Coupon.DiscountType.PERCENTAGE, Decimal("25.00"), Decimal("125.00"), Decimal("599.00"), now - timedelta(days=1), now + timedelta(days=14), True),
                ("PARTY40", Coupon.DiscountType.PERCENTAGE, Decimal("40.00"), Decimal("300.00"), Decimal("1199.00"), now - timedelta(days=1), now + timedelta(days=30), True),
                ("LUNCH10", Coupon.DiscountType.PERCENTAGE, Decimal("10.00"), Decimal("50.00"), Decimal("199.00"), now - timedelta(days=5), now + timedelta(days=60), True),
                ("DINNER15", Coupon.DiscountType.PERCENTAGE, Decimal("15.00"), Decimal("80.00"), Decimal("399.00"), now - timedelta(days=5), now + timedelta(days=60), True),
                # Percentage Coupons (Expired / Inactive for API edge-case testing)
                ("EXPIRED20", Coupon.DiscountType.PERCENTAGE, Decimal("20.00"), Decimal("100.00"), Decimal("299.00"), now - timedelta(days=60), now - timedelta(days=10), True),
                ("INACTIVE30", Coupon.DiscountType.PERCENTAGE, Decimal("30.00"), Decimal("150.00"), Decimal("399.00"), now - timedelta(days=5), now + timedelta(days=30), False),

                # Flat Coupons (Active)
                ("FLAT50", Coupon.DiscountType.FLAT, Decimal("50.00"), None, Decimal("250.00"), now - timedelta(days=10), now + timedelta(days=60), True),
                ("FLAT100", Coupon.DiscountType.FLAT, Decimal("100.00"), None, Decimal("499.00"), now - timedelta(days=10), now + timedelta(days=60), True),
                ("FLAT150", Coupon.DiscountType.FLAT, Decimal("150.00"), None, Decimal("699.00"), now - timedelta(days=10), now + timedelta(days=60), True),
                ("FLAT200", Coupon.DiscountType.FLAT, Decimal("200.00"), None, Decimal("999.00"), now - timedelta(days=10), now + timedelta(days=60), True),
                ("QUICK30", Coupon.DiscountType.FLAT, Decimal("30.00"), None, Decimal("150.00"), now - timedelta(days=10), now + timedelta(days=60), True),
                ("TREAT75", Coupon.DiscountType.FLAT, Decimal("75.00"), None, Decimal("399.00"), now - timedelta(days=10), now + timedelta(days=60), True),
                ("SUPER250", Coupon.DiscountType.FLAT, Decimal("250.00"), None, Decimal("1200.00"), now - timedelta(days=10), now + timedelta(days=60), True),
                ("MIDNIGHT60", Coupon.DiscountType.FLAT, Decimal("60.00"), None, Decimal("300.00"), now - timedelta(days=10), now + timedelta(days=60), True),
                # Flat Coupons (Expired / Inactive)
                ("EXPIREDFLAT", Coupon.DiscountType.FLAT, Decimal("100.00"), None, Decimal("400.00"), now - timedelta(days=90), now - timedelta(days=5), True),
                ("INACTIVEFLAT", Coupon.DiscountType.FLAT, Decimal("80.00"), None, Decimal("350.00"), now - timedelta(days=5), now + timedelta(days=30), False),
            ]

            coupon_objs = []
            for code, dtype, val, max_d, min_o, vf, vu, active in coupon_specs:
                cp = Coupon.objects.create(
                    code=code,
                    discount_type=dtype,
                    discount_value=val,
                    max_discount_amount=max_d,
                    min_order_amount=min_o,
                    valid_from=vf,
                    valid_until=vu,
                    is_active=active,
                )
                coupon_objs.append(cp)

            # 8. CART ITEMS (25 items for testing /api/cart/)
            cart_count = 0
            # Populate cart for customers
            for cust in customer_users[:8]:
                sample_items = random.sample(menu_item_objs[:25], 3)
                for item in sample_items:
                    Cart.objects.create(
                        user=cust,
                        menu_item=item,
                        quantity=random.randint(1, 3),
                        unit_price=item.price,
                        price=item.price,
                    )
                    cart_count += 1

            # 9. ORDERS & ORDER ITEMS (28 orders covering all statuses)
            order_statuses = [
                Order.StatusChoices.PENDING_PAYMENT,
                Order.StatusChoices.PENDING_PAYMENT,
                Order.StatusChoices.PENDING_PAYMENT,
                Order.StatusChoices.PENDING_PAYMENT,
                Order.StatusChoices.CONFIRMED,
                Order.StatusChoices.CONFIRMED,
                Order.StatusChoices.CONFIRMED,
                Order.StatusChoices.CONFIRMED,
                Order.StatusChoices.PREPARING,
                Order.StatusChoices.PREPARING,
                Order.StatusChoices.PREPARING,
                Order.StatusChoices.PREPARING,
                Order.StatusChoices.READY_FOR_PICKUP,
                Order.StatusChoices.READY_FOR_PICKUP,
                Order.StatusChoices.READY_FOR_PICKUP,
                Order.StatusChoices.READY_FOR_PICKUP,
                Order.StatusChoices.OUT_FOR_DELIVERY,
                Order.StatusChoices.OUT_FOR_DELIVERY,
                Order.StatusChoices.OUT_FOR_DELIVERY,
                Order.StatusChoices.OUT_FOR_DELIVERY,
                Order.StatusChoices.DELIVERED,
                Order.StatusChoices.DELIVERED,
                Order.StatusChoices.DELIVERED,
                Order.StatusChoices.DELIVERED,
                Order.StatusChoices.DELIVERED,
                Order.StatusChoices.DELIVERED,
                Order.StatusChoices.CANCELLED,
                Order.StatusChoices.CANCELLED,
            ]

            active_coupons = [c for c in coupon_objs if c.is_valid]
            created_orders = []

            for idx, status in enumerate(order_statuses):
                cust = customer_users[idx % len(customer_users)]
                
                # Assign delivery crew if out for delivery or delivered
                assigned_crew = None
                if status in [Order.StatusChoices.OUT_FOR_DELIVERY, Order.StatusChoices.DELIVERED, Order.StatusChoices.READY_FOR_PICKUP]:
                    assigned_crew = delivery_users[idx % len(delivery_users)]

                # Optional coupon
                applied_coupon = None
                if idx % 3 == 0 and active_coupons:
                    applied_coupon = active_coupons[idx % len(active_coupons)]

                order = Order.objects.create(
                    user=cust,
                    delivery_crew=assigned_crew,
                    status=status,
                    coupon=applied_coupon,
                    discount_amount=Decimal("0.00"),
                    total=Decimal("0.00"),
                )

                # Order Items (2-3 items per order)
                order_items_selection = random.sample(menu_item_objs, random.randint(2, 3))
                subtotal = Decimal("0.00")
                for m_item in order_items_selection:
                    qty = random.randint(1, 2)
                    oi = OrderItem.objects.create(
                        order=order,
                        menu_item=m_item,
                        quantity=qty,
                        unit_price=m_item.price,
                        price=m_item.price * qty,
                    )
                    subtotal += oi.price

                # Calculate discount
                discount = Decimal("0.00")
                if applied_coupon:
                    discount = Decimal(str(round(applied_coupon.calculate_discount(subtotal), 2)))

                final_total = max(subtotal - discount, Decimal("0.00"))
                order.discount_amount = discount
                order.total = final_total
                order.save()
                created_orders.append(order)

            # 10. PAYMENTS (25 payments for created orders)
            payment_methods = [
                Payment.PaymentMethod.UPI,
                Payment.PaymentMethod.CARD,
                Payment.PaymentMethod.NET_BANKING,
                Payment.PaymentMethod.COD,
                Payment.PaymentMethod.RAZORPAY,
                Payment.PaymentMethod.STRIPE,
            ]
            for order in created_orders:
                if order.status == Order.StatusChoices.PENDING_PAYMENT:
                    pay_status = Payment.PaymentStatus.PENDING
                elif order.status == Order.StatusChoices.CANCELLED:
                    pay_status = random.choice([Payment.PaymentStatus.FAILED, Payment.PaymentStatus.REFUNDED])
                else:
                    pay_status = Payment.PaymentStatus.COMPLETED

                Payment.objects.create(
                    order=order,
                    amount=order.total,
                    status=pay_status,
                    payment_method=random.choice(payment_methods),
                )

            # 11. DELIVERY ASSIGNMENTS (20 assignments)
            partner_map = {dp.user.id: dp for dp in delivery_partners}
            for order in created_orders:
                if order.delivery_crew and order.delivery_crew.id in partner_map:
                    partner = partner_map[order.delivery_crew.id]
                    if order.status == Order.StatusChoices.DELIVERED:
                        da_status = DeliveryAssignment.AssignmentStatus.DELIVERED
                    elif order.status == Order.StatusChoices.OUT_FOR_DELIVERY:
                        da_status = DeliveryAssignment.AssignmentStatus.PICKED_UP
                    elif order.status == Order.StatusChoices.READY_FOR_PICKUP:
                        da_status = DeliveryAssignment.AssignmentStatus.ASSIGNED
                    elif order.status == Order.StatusChoices.CANCELLED:
                        da_status = DeliveryAssignment.AssignmentStatus.CANCELLED
                    else:
                        continue

                    DeliveryAssignment.objects.create(
                        order=order,
                        partner=partner,
                        status=da_status,
                    )

            # 12. REVIEWS (30 reviews)
            review_comments = [
                (5, "Absolutely exquisite flavors! Arrived hot and perfectly seasoned."),
                (5, "One of the best dishes I've had in a long time. Highly recommend!"),
                (4, "Delicious food, well packaged, portion size was good."),
                (4, "Very tasty and fresh ingredients. Will definitely order again."),
                (5, "Top quality, authentic taste and great presentation."),
                (3, "Decent food, could use a bit more spice, but overall enjoyable."),
                (4, "Crispy and flavorful, reached quickly."),
                (5, "Loved the rich creamy texture. A must-try!"),
                (3, "Good taste, though slightly on the oily side."),
                (2, "A bit too salty for my liking, but the texture was nice."),
                (5, "Hands down the best item on the menu! 10/10."),
                (4, "Perfect companion for an evening meal with friends."),
            ]

            review_pairs = set()
            reviews_count = 0
            while reviews_count < 30:
                cust = random.choice(customer_users)
                m_item = random.choice(menu_item_objs)
                pair = (cust.id, m_item.id)
                if pair in review_pairs:
                    continue
                review_pairs.add(pair)
                rating, comment = random.choice(review_comments)
                Review.objects.create(
                    user=cust,
                    menu_item=m_item,
                    rating=rating,
                    comment=comment,
                )
                reviews_count += 1

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
