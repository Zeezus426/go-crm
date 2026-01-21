# Deployment Configuration for Go-CRM

## Environment Variables Required for Production

### Database Configuration
```bash
POSTGRES_NAME=your_database_name
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password
POSTGRES_HOST=your_database_host
POSTGRES_PORT=5432
```

### Security & Environment
```bash
SECRET_KEY=your_secret_key
DJANGO_SETTINGS_MODULE=core.settings.prod
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### CORS & CSRF
```bash
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Email Configuration (Mailgun)
```bash
MAILGUN_API_KEY=your_mailgun_api_key
MAILGUN_DOMAIN=your_mailgun_domain
EMAIL_HOST_USER=your_email_address
EMAIL_HOST_PASSWORD=your_mailgun_password
```

### SMS Configuration (Twilio)
```bash
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
```

### Redis & Celery
```bash
REDIS_HOST=redis://your_redis_host:6379/0
CELERY_TIMEZONE=Australia/Sydney
```

### External APIs
```bash
OPENAI_API_KEY=your_openai_api_key
NEO4J_URL=bolt://your_neo4j_host:7687
NEO4J_USERNAME=your_neo4j_username
NEO4J_PASSWORD=your_neo4j_password
FIRECRAWL_API_KEY=your_firecrawl_api_key
SERPER_API_KEY=your_serper_api_key
```

### Static & Media Files
```bash
STATIC_URL=/static/
MEDIA_URL=/media/
```

## Docker Build

```bash
# Build for production
docker build -t go-crm:latest .
```

## Docker Compose for Production

```bash
# Using the production compose
docker-compose -f docker-compose.prod.yml up -d
```

## Captain (CapRover) Deployment

1. Create a new app in CapRover dashboard
2. Set the environment variables listed above
3. Set the container port to `8000`
4. Upload the application or connect to your git repository
5. Deploy!

## Health Check Endpoint

The application includes a health check endpoint at `/health/` that returns 200 if the application is running correctly.

## Security Considerations

- **SSL/TLS**: Always use HTTPS in production
- **Secret Key**: Use a strong, random SECRET_KEY
- **Database**: Use strong database credentials
- **Allowed Hosts**: Configure ALLOWED_HOSTS properly
- **CORS**: Restrict CORS origins to your frontend domain only
- **Environment Variables**: Never commit `.env` files to version control

## Monitoring & Logging

- Django logs are written to `/app/logs/django.log`
- Health checks run every 30 seconds
- Application metrics should be integrated with your monitoring solution

## Production Database Setup

Before deploying, ensure your production database is properly set up:

```bash
# Run migrations
python manage.py migrate --settings=core.settings.prod

# Create superuser (optional)
python manage.py createsuperuser --settings=core.settings.prod

# Collect static files (automatically done in Dockerfile)
python manage.py collectstatic --noinput --settings=core.settings.prod
```