# Wedding API Gateway

API Gateway menggunakan KrakenD untuk menjembatani tiga microservices dengan arsitektur **production-ready**:
- **Auth API** - Authentication & Authorization Service (Nginx + PHP-FPM)
- **Generic API** - General Purpose Service (Nginx + PHP-FPM)
- **Transaction API** - Transaction Management Service (Nginx + PHP-FPM)

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Network `backend-network` harus sudah dibuat terlebih dahulu

### Membuat Network (jika belum ada)
```bash
docker network create backend-network
```

### Menjalankan API Gateway

1. **Build dan jalankan semua services:**
```bash
# Jalankan Auth API (Nginx + PHP-FPM)
cd ../auth
docker-compose up -d --build

# Jalankan Generic API (Nginx + PHP-FPM)
cd ../generic
docker-compose up -d --build

# Jalankan Transaction API (Nginx + PHP-FPM)
cd ../transaction
docker-compose up -d --build

# Jalankan API Gateway
cd ../api-gateway
docker-compose up -d --build
```

2. **Atau build ulang:**
```bash
docker-compose up -d --build
```

3. **Cek logs:**
```bash
docker-compose logs -f
```

4. **Stop services:**
```bash
docker-compose down
```

## 📡 API Endpoints

API Gateway berjalan di `http://localhost:8080`

### Health Check
- `GET /health` - Gateway health status

### Auth Service (`/auth/*`)
- `POST /auth/register` - Register user baru
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user
- `GET /auth/user` - Get current user
- `GET /auth/users` - Get all users
- `GET /auth/users/{id}` - Get user by ID
- `POST /auth/users` - Create new user
- `PUT /auth/users/{id}` - Update user
- `DELETE /auth/users/{id}` - Delete user
- `GET /auth/roles` - Get all roles
- `GET /auth/permissions` - Get all permissions

### Generic Service (`/generic/*`)
- `GET /generic/menus` - Get all menus
- `GET /generic/menus/{id}` - Get menu by ID
- `POST /generic/menus` - Create new menu
- `PUT /generic/menus/{id}` - Update menu
- `DELETE /generic/menus/{id}` - Delete menu
- `GET /generic/{resource}` - Get all resources (dynamic)
- `GET /generic/{resource}/{id}` - Get resource by ID
- `POST /generic/{resource}` - Create resource
- `PUT /generic/{resource}/{id}` - Update resource
- `DELETE /generic/{resource}/{id}` - Delete resource

### Transaction Service (`/transaction/*`)
- `GET /transaction/transactions` - Get all transactions
- `GET /transaction/transactions/{id}` - Get transaction by ID
- `POST /transaction/transactions` - Create new transaction
- `PUT /transaction/transactions/{id}` - Update transaction
- `DELETE /transaction/transactions/{id}` - Delete transaction
- `GET /transaction/{resource}` - Get all resources (dynamic)
- `GET /transaction/{resource}/{id}` - Get resource by ID
- `POST /transaction/{resource}` - Create resource
- `PUT /transaction/{resource}/{id}` - Update resource
- `DELETE /transaction/{resource}/{id}` - Delete resource

## 🔧 Configuration

### Port Mapping
- **API Gateway**: `8080` (external) → `8080` (internal)
- **Auth Service (Nginx)**: `8000` (external) → `80` (nginx) → `9000` (php-fpm)
- **Generic Service (Nginx)**: `8001` (external) → `80` (nginx) → `9000` (php-fpm)
- **Transaction Service (Nginx)**: `8002` (external) → `80` (nginx) → `9000` (php-fpm)

### Backend Services
Konfigurasi backend services ada di `config/krakend.json`:
- `nginx-auth` - Auth Service (Internal Nginx container)
- `nginx-generic` - Generic Service (Internal Nginx container)
- `nginx-transaction` - Transaction Service (Internal Nginx container)

### Architecture per Service
Setiap service menggunakan arsitektur 2-tier:
1. **Nginx** - Web server & reverse proxy (port 80 internal)
2. **PHP-FPM** - PHP FastCGI Process Manager (port 9000 internal)

### CORS Configuration
Gateway mengizinkan:
- All origins (`*`)
- Methods: GET, POST, PUT, DELETE, PATCH, OPTIONS
- Headers: Origin, Content-Type, Authorization, Accept, X-Requested-With
- Max Age: 12 hours

## 📝 Example Usage

### Register User
```bash
curl -X POST http://localhost:8080/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Get Menus (with Auth)
```bash
curl -X GET http://localhost:8080/generic/menus \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Create Transaction
```bash
curl -X POST http://localhost:8080/transaction/transactions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "amount": 1000000,
    "description": "Wedding Package Payment"
  }'
```

## 🐳 Docker Architecture

```
┌─────────────────────────────────────────────────────┐
│          API Gateway (KrakenD)                      │
│                Port: 8080                           │
└───────────────────┬─────────────────────────────────┘
                    │
        ┌───────────┼───────────┬──────────────────┐
        │           │           │                  │
┌───────▼────┐ ┌───▼───────┐ ┌─▼──────────────┐   │
│ nginx-auth │ │nginx-      │ │nginx-          │   │
│   :8000    │ │generic     │ │transaction     │   │
│            │ │  :8001     │ │    :8002       │   │
└─────┬──────┘ └──────┬─────┘ └────────┬───────┘   │
      │               │                 │           │
      │ fastcgi       │ fastcgi         │ fastcgi   │
      │ :9000         │ :9000           │ :9000     │
      │               │                 │           │
┌─────▼──────┐ ┌──────▼─────┐ ┌────────▼───────┐   │
│ api-auth   │ │api-generic │ │api-transaction │   │
│ (PHP-FPM)  │ │ (PHP-FPM)  │ │   (PHP-FPM)    │   │
└────────────┘ └────────────┘ └────────────────┘   │
                                                    │
         All connected via backend-network ─────────┘
```

## 🔐 Security Features

### API Gateway (KrakenD)
- CORS enabled dengan konfigurasi flexible
- Request timeout: 30 seconds
- Cache TTL: 5 minutes (300s)
- Logging level: INFO
- JSON output encoding

### Nginx Layer (Production)
- **Security Headers**: X-Frame-Options, X-Content-Type-Options, X-XSS-Protection
- **Gzip Compression**: Menghemat bandwidth untuk JSON & assets
- **Static File Caching**: Cache 1 tahun untuk images, CSS, JS
- **FastCGI Optimization**: Timeout 60s untuk PHP processing
- **Hide PHP Version**: Security best practice
- **Hidden Files Protection**: Blokir akses ke `.env`, `.git`, dll

## 🛠️ Troubleshooting

### Gateway tidak bisa akses backend services
1. Pastikan semua services berjalan:
```bash
docker ps
```

2. Cek network:
```bash
docker network inspect backend-network
```

3. Cek logs gateway:
```bash
docker-compose logs -f api-gateway
```

### Rebuild configuration
Jika mengubah `krakend.json`:
```bash
docker-compose down
docker-compose up -d --build
```

### Test connectivity
```bash
# Masuk ke container gateway
docker exec -it api-gateway sh

# Test akses ke Nginx backends
wget -O- http://nginx-auth/api/health
wget -O- http://nginx-generic/api/health
wget -O- http://nginx-transaction/api/health

# Test dari host machine
curl http://localhost:8000/api/health  # Auth via Nginx
curl http://localhost:8001/api/health  # Generic via Nginx
curl http://localhost:8002/api/health  # Transaction via Nginx
curl http://localhost:8080/health      # Gateway health
```

### Cek status containers
```bash
# Lihat semua containers
docker ps

# Expected output:
# - api-gateway
# - nginx-auth, api-auth
# - nginx-generic, api-generic
# - nginx-transaction, api-transaction
```

### Akses Nginx logs
```bash
# Auth service
docker exec nginx-auth tail -f /var/log/nginx/access.log
docker exec nginx-auth tail -f /var/log/nginx/error.log

# Generic service
docker exec nginx-generic tail -f /var/log/nginx/access.log

# Transaction service
docker exec nginx-transaction tail -f /var/log/nginx/access.log
```

## 📚 Additional Resources

- [KrakenD Documentation](https://www.krakend.io/docs/)
- [KrakenD Configuration](https://www.krakend.io/docs/configuration/structure/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [PHP-FPM Configuration](https://www.php.net/manual/en/install.fpm.php)

## 🎯 Production Features

### Why Nginx + PHP-FPM?
1. **Performance**: Multi-process handling untuk concurrent requests
2. **Stability**: Production-tested & reliable
3. **Scalability**: Easy horizontal scaling
4. **Security**: Industry-standard security practices
5. **Caching**: Static file optimization & Gzip compression

### Benefits dengan API Gateway
- ✅ Centralized routing via KrakenD
- ✅ Production-ready backend services
- ✅ Load balancing & rate limiting di Gateway layer
- ✅ SSL/TLS termination bisa di Gateway
- ✅ Monitoring & logging terpusat

## 📄 License

This project is part of Wedding Backend System.
