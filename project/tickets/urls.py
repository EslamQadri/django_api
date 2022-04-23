from django.urls import include, path
from .views import test, no_rest_no_model, no_rest_with_model, FBV_LIST as rest_post_and_get_methods, FBV_BK as rest_delete_put_and_get_methods
from .views import CBV_LIST as rest_post_and_get_methods_cbv, CBV_BK as rest_delete_put_and_get_methods_cbv
from .views import mixins_list, mixins_pk, Generic_list, Generic_pk
from tickets import views 
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token 
router = DefaultRouter()
router.register('guests',views.Viewset_Guest)
router.register('movie',views.Viewset_movie)
router.register('Reservation',views.Viewset_Reservation)

app_name = 'tickets'
urlpatterns = [

    path("", test, name='test'),
    path('no_rest_no_model', no_rest_no_model, name='no_rest_no_model'),
    path('no_rest_with_model', no_rest_with_model, name='no_rest_with_model'),
    # rest fbv
    path('rest_post_and_get_methods', rest_post_and_get_methods,
         name='rest_post_and_get_methods'),
    path('rest_delete_put_and_get_methods/<int:Pk>/',
         rest_delete_put_and_get_methods, name='rest_delete_put_and_get_methods'),
    # rest cbv
    path('rest_post_and_get_methods_cbv', rest_post_and_get_methods_cbv.as_view(
    ), name='rest_post_and_get_methods_cbv'),
    path('rest_delete_put_and_get_methods_cbv/<int:PK>/',
         rest_delete_put_and_get_methods_cbv.as_view()),
    # rest mixins cbv
    path('mixins_list', mixins_list, name='mixins_list'),
    path('mixins_pk/<int:pk>/', mixins_pk, name='mixins_pk'),
    # generics cbv
    path('Generic_list/', Generic_list.as_view()),
    path('Generic_pk/<int:pk>', Generic_pk.as_view()),
    # viwe set
    path('rest/viewsets/', include(router.urls)),
    #find movie
    path('fbv/findmovie/',views.find_movie),
    #new new_Reservation
    path ('fbv/new_Reservation/',views.new_Reservation),
    
    #rest auth url
    path('api-auth',include('rest_framework.urls')),

    #tokens
    #------------------------------------------------------------------
    path('api-auth-token',obtain_auth_token,name='api-auth-token'),

    #---------------------------------------------------------
    #permissions 
    path('post/<int:pk>',views.Post_pk.as_view()),

]
