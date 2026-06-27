# ============================================
# STAGE 1: Build frontend assets with Node.js
# ============================================
FROM node:20-alpine AS node-build

WORKDIR /build

COPY package.json ./
RUN npm install

COPY postcss.config.js tailwind.config.js vite.config.js ./
COPY resources/ resources/
RUN npm run build

# ============================================
# STAGE 2: PHP + Composer + Laravel runtime
# ============================================
FROM php:8.2-cli

# Install system dependencies & PHP extensions
RUN apt-get update && apt-get install -y \
    git \
    unzip \
    libzip-dev \
    libsqlite3-dev \
    libonig-dev \
    libxml2-dev \
    curl \
    && docker-php-ext-install \
    pdo \
    pdo_sqlite \
    mbstring \
    xml \
    bcmath \
    zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Composer
COPY --from=composer:2.8 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

# Copy application files
COPY composer.json composer.lock ./
COPY artisan ./
COPY bootstrap/ bootstrap/
COPY config/ config/
COPY database/ database/
COPY public/ public/
COPY routes/ routes/
COPY app/ app/
COPY resources/ resources/
COPY storage/ storage/
COPY .env.example .env

# Ensure required directories exist (gitignored dirs may not be in git)
RUN mkdir -p storage/framework/{cache,sessions,views,testing} \
    && mkdir -p storage/logs \
    && mkdir -p storage/app \
    && mkdir -p bootstrap/cache

# Copy built frontend assets from node-build stage
COPY --from=node-build /build/public/build/ public/build/

# Install PHP dependencies
RUN composer install --no-interaction --optimize-autoloader --no-dev

# Generate app key & create sqlite database
# MUFTI_API_URL ditambahkan ke .env karena php artisan serve
# tidak mewariskan semua environment variable dari Docker
RUN echo "MUFTI_API_URL=http://python-api:8001" >> .env \
    && php artisan key:generate --force \
    && touch database/database.sqlite \
    && php artisan migrate --force

# Set permissions
RUN chown -R www-data:www-data storage bootstrap/cache \
    && chmod -R 775 storage bootstrap/cache

EXPOSE 8000

# Run Laravel development server
CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=8000"]
