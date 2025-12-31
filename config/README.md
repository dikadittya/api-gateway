# KrakenD Flexible Configuration

Struktur ini menggunakan **KrakenD Flexible Configuration** untuk memisahkan endpoints berdasarkan service/host.

## Struktur File

```
config/
├── krakend.tmpl.json          # Main config dengan Go templates
├── krakend.json               # Generated config (jangan edit manual)
├── settings/
│   └── hosts.json             # Definisi host untuk setiap service
└── partials/
    ├── endpoints_auth.tmpl    # Endpoints untuk Auth Service (nginx-auth)
    ├── endpoints_generic.tmpl # Endpoints untuk Generic Service (nginx-generic)
    └── endpoints_transaction.tmpl # Endpoints untuk Transaction Service (nginx-transaction)
```

## Cara Kerja

1. **Edit template files** (`krakend.tmpl.json` dan `partials/*.tmpl`) untuk perubahan konfigurasi
2. **Generate krakend.json** dari templates menggunakan KrakenD CLI
3. **Restart gateway** untuk apply perubahan

## Commands

### 1. Build Configuration (Tanpa KrakenD CLI)

```bash
# Windows PowerShell
cd c:\laragon\www\WeddingBE\api-gateway\config
.\build-config.ps1

# Atau langsung dengan Python
python build-config.py
```

### 2. Validate Generated Config (Optional, jika ada KrakenD CLI)

```bash
krakend check -c krakend.json
```

### 3. Restart Gateway

```bash
cd c:\laragon\www\WeddingBE\api-gateway
docker-compose restart
```

## Menambah Endpoint Baru

### Auth Service Endpoints
Edit: `partials/endpoints_auth.tmpl`

```json
,{
  "endpoint": "/new-endpoint",
  "method": "GET",
  "input_headers": ["Authorization"],
  "output_encoding": "no-op",
  "backend": [
    {
      "url_pattern": "/api/new-endpoint",
      "encoding": "json",
      "method": "GET",
      "host": ["{{ .hosts.auth }}"],
      "extra_config": {
        "backend/http": {
          "return_error_code": true
        }
      }
    }
  ]
}
```

### Generic Service Endpoints
Edit: `partials/endpoints_generic.tmpl`

### Transaction Service Endpoints
Edit: `partials/endpoints_transaction.tmpl`

## Mengganti Host

Edit: `settings/hosts.json`

```json
{
  "hosts": {
    "auth": "http://nginx-auth",
    "generic": "http://nginx-generic",
    "transaction": "http://nginx-transaction",
    "gateway": "http://api-gateway:8080"
  }
}
```

## Backup Config Lama

Config single-file yang lama sudah di-backup ke `krakend.json.backup`

## Troubleshooting

### Template Errors
```bash
krakend check -t -c krakend.tmpl.json -d
```

### JSON Syntax Errors
- Pastikan setiap endpoint dipisah dengan koma
- Endpoint terakhir dalam file template TIDAK boleh ada koma trailing

### Host Not Found
- Check `settings/hosts.json`
- Pastikan template menggunakan `{{ .hosts.service_name }}`

## Best Practices

1. ✅ Selalu test dengan `krakend check` sebelum restart
2. ✅ Edit file `.tmpl` bukan `krakend.json` directly
3. ✅ Commit kedua `.tmpl` dan generated `krakend.json`
4. ✅ Gunakan versioning untuk track changes
5. ✅ Backup config sebelum major changes
