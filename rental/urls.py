from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('daftar/', views.daftar_view, name='daftar'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('sepeda/', views.daftar_sepeda, name='daftar_sepeda'),
    path('sepeda/<int:id_sepeda>/', views.detail_sepeda, name='detail_sepeda'),
    path('stasiun/', views.daftar_stasiun, name='daftar_stasiun'),
    path('peminjaman/<int:id_peminjaman>/kembalikan/', views.kembalikan_sepeda, name='kembalikan_sepeda'),
    path('peminjaman/<int:id_peminjaman>/pembayaran/', views.pembayaran, name='pembayaran'),
    path('riwayat-peminjaman/', views.riwayat_peminjaman, name='riwayat_peminjaman'),
    path('peminjaman/<int:id_peminjaman>/', views.detail_peminjaman, name='detail_peminjaman'),
]