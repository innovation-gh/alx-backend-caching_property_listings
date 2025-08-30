# alx-backend-caching_property_listings
# ALX Backend Caching - Property Listings

A Django-based property listing application demonstrating multi-level caching strategies using Redis.

## Features

- **Multi-level Caching**: View-level and low-level queryset caching
- **Redis Backend**: High-performance in-memory caching
- **Cache Invalidation**: Automatic cache invalidation using Django signals
- **Cache Metrics**: Real-time Redis performance monitoring
- **Dockerized Services**: PostgreSQL and Redis containers

## Project Structure

```
alx-backend-caching_property_listings/
├── alx_backend_caching_property_listings/
│   ├── settings.py              # Django settings with Redis configuration
│   ├── urls.py                  # Main URL configuration
│   └── ...
├── properties/
│   ├── models.py               # Property model
│   ├── views.py                # Cached views
│   ├── utils.py                # Caching utilities and metrics
│   ├── signals.py              # Cache invalidation signals
│   ├── apps.py                 # App configuration
│