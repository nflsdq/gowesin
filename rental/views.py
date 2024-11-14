from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
from .models import Sepeda, Peminjaman, Stasiun, Pelanggan, Pembayaran
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login berhasil!')
            return redirect('home')
        else:
            messages.error(request, 'Username atau password salah!')
    
    return render(request, 'login.html')

def daftar_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        no_telp = request.POST.get('no_telp')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Konfirmasi password tidak cocok.')
            return redirect('daftar')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan.')
            return redirect('daftar')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah digunakan.')
            return redirect('daftar')

        user = User.objects.create_user(first_name=nama, username=username, email=email, password=password)
        pelanggan = Pelanggan.objects.create(
            user=user,
            nama=nama,
            username=username,
            email=email,
            no_telp=no_telp
        )

        messages.success(request, 'Pendaftaran berhasil. Silahkan login.')
        return redirect('login')

    return render(request, 'daftar.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout berhasil!')
    return redirect('home')  

def home(request):
    sepeda_tersedia = Sepeda.objects.filter(status_sepeda='T')[:6]
    stasiun_list = Stasiun.objects.annotate(jumlah_sepeda=Count('sepeda')).all()
    return render(request, 'home.html', {'sepeda_tersedia': sepeda_tersedia, 'stasiun_list': stasiun_list})

def daftar_sepeda(request):
    sepeda_list = Sepeda.objects.all()

    jenis_sepeda = request.GET.get('jenis_sepeda')
    stasiun = request.GET.get('stasiun')

    if jenis_sepeda:
        sepeda_list = sepeda_list.filter(jenis_sepeda=jenis_sepeda)
    if stasiun:
        sepeda_list = sepeda_list.filter(stasiun__id_stasiun=stasiun)

    return render(request, 'daftar_sepeda.html', {'sepeda_list': sepeda_list})

def detail_sepeda(request, id_sepeda):
    sepeda = get_object_or_404(Sepeda, id_sepeda=id_sepeda)
    if request.method == 'POST':
        pelanggan = request.user.pelanggan
        peminjaman = Peminjaman.objects.create(
            pelanggan=pelanggan,
            sepeda=sepeda,
            stasiun_pengambilan=sepeda.stasiun,
            waktu_pengambilan=timezone.now()
        )
        sepeda.status_sepeda = 'D'
        sepeda.save()
        messages.success(request, 'Sepeda berhasil disewa!')
        return redirect('riwayat_peminjaman')
        
    return render(request, 'detail_sepeda.html', {'sepeda': sepeda})

def daftar_stasiun(request):
    stasiun_list = Stasiun.objects.annotate(jumlah_sepeda=Count('sepeda')).all()
    return render(request, 'daftar_stasiun.html', {'stasiun_list': stasiun_list})

@login_required
def kembalikan_sepeda(request, id_peminjaman):
    peminjaman = get_object_or_404(Peminjaman, id_peminjaman=id_peminjaman)
    if request.method == 'POST':
        stasiun_id = request.POST.get('stasiun_id')
        stasiun_pengembalian = get_object_or_404(Stasiun, id_stasiun=stasiun_id)
        
        sepeda = peminjaman.sepeda

        peminjaman.waktu_pengembalian = timezone.now()
        peminjaman.stasiun_pengembalian = stasiun_pengembalian
        peminjaman.sepeda.status_sepeda = 'T'
        peminjaman.sepeda.stasiun = stasiun_pengembalian
        
        # Hitung biaya
        durasi = peminjaman.waktu_pengembalian - peminjaman.waktu_pengambilan
        jam = durasi.total_seconds() / 3600
        tarif_per_jam = sepeda.biaya_sepeda()
        peminjaman.total_biaya = jam * tarif_per_jam
        
        peminjaman.save()
        peminjaman.sepeda.save()
        
        messages.success(request, 'Sepeda berhasil dikembalikan!')
        return redirect('pembayaran', id_peminjaman=peminjaman.id_peminjaman)
    
    stasiun_list = Stasiun.objects.all()
    return render(request, 'kembalikan_sepeda.html', {'peminjaman': peminjaman, 'stasiun_list': stasiun_list})

@login_required
def pembayaran(request, id_peminjaman):
    peminjaman = get_object_or_404(Peminjaman, id_peminjaman=id_peminjaman)
    if request.method == 'POST':
        metode_pembayaran = request.POST.get('metode_pembayaran')
        Pembayaran.objects.create(
            peminjaman=peminjaman,
            metode_pembayaran=metode_pembayaran,
            jumlah_pembayaran=peminjaman.total_biaya
        )
        peminjaman.status_pembayaran = 'Lunas'
        peminjaman.save()
        messages.success(request, 'Pembayaran berhasil!')
        return redirect('riwayat_peminjaman')
    return render(request, 'pembayaran.html', {'peminjaman': peminjaman})

@login_required
def riwayat_peminjaman(request):
    peminjaman_list = Peminjaman.objects.filter(pelanggan=request.user.pelanggan).order_by('-waktu_pengambilan')
    return render(request, 'riwayat_peminjaman.html', {'peminjaman_list': peminjaman_list})

@login_required
def detail_peminjaman(request, id_peminjaman):
    peminjaman = get_object_or_404(Peminjaman, id_peminjaman=id_peminjaman)
    return render(request, 'detail_peminjaman.html', {'peminjaman': peminjaman})
