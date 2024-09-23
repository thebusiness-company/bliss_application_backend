from .views.auth_views import *
from .views.file_views import *
from .views.product_views import *
from .views.cart_views import *
from .views.order_views import *
# from .views.payment_views import *
from django.urls import path

urlpatterns = [
    #customer api
    path('create_token',CreateToken.as_view()),   
    path('add_customer',AddCustomer.as_view()),    
    path('update_customer',UpdateCustomer.as_view()),
    path('get_customer',GetCustomer.as_view()), 
    path('get_user_id',GetUserId.as_view()), 
    path('list_customer',ListCustomer.as_view()),
    path('add_collection_query',AddCollectionQuery.as_view()), 
    path('add_role',AddRole.as_view()), 
    path('add_admin',AddAdmin.as_view()),
    path('get_user_role',Get_User_Role.as_view()),
    path('contact_api',Contact_Submission.as_view()),
    path('signinwith_google',SignInWith_Google.as_view()),
    path('reset_password',Reset_Password.as_view()),
    path('change_password',Change_Password.as_view()),
    #product api
    path('add_product',AddProduct.as_view()), 
    path('list_product',ListProduct.as_view()), 
    path('get_product',GetProduct.as_view()),
    path('update_product',UpdateProduct.as_view()),
    path('delete_product',DeleteProduct.as_view()),
    #cart api
    path('add_to_cart',AddCart.as_view()), 
    path('get_cart',GetCart.as_view()),
    path('list_cart',ListCartItems.as_view()), 
    path('update_cart',UpdateCartItems.as_view()), 
    path('delete_cart',DeleteCartItems.as_view()),
    path('delete_all_cart',DeleteAllItems.as_view()), 
    
    #order api
    path('create_order',AddOrder.as_view()), 
    path('cancel_order',CancelOrder.as_view()),
    path('update_order',UpdateOrder.as_view()),
    path('get_order',GetOrderData.as_view()),
    path('list_order_by_userfilter',ListOrdersByUser.as_view()),
    path('list_orders',ListAllOrders.as_view()),
    
    path('upload_file', UploadFile.as_view()),
    path('get_file',GetFile.as_view()),
    
    #payment
    # path('razorpay_order', PaymentView.as_view(), name='razorpay_order'),
    # path('razorpay_callback', CallbackView.as_view(), name='razorpay_callback'),
]
