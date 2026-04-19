# Deployment Readiness Checklist

## Backend
- [ ] All unit tests passing (`pytest tests/ -v`)
- [ ] All API endpoints returning correct status codes
- [ ] Error handling working (400, 404, 500 responses)
- [ ] CORS configured correctly
- [ ] Environment variables set (no secrets in code)
- [ ] Database migrations runnable (`alembic upgrade head`)
- [ ] Logging implemented

## Frontend
- [ ] No console errors on any page
- [ ] All pages load without crashing
- [ ] Loading states showing on async calls
- [ ] Error messages displayed on API failures
- [ ] Mobile responsive (tested at 480px, 768px, 1024px)
- [ ] Build succeeds: `npm run build`
- [ ] `NEXT_PUBLIC_API_URL` set for production

## Security
- [ ] HTTPS enforced in production
- [ ] CORS origins restricted to known domains
- [ ] SQL injection prevention (ORM used throughout)
- [ ] No sensitive data in frontend code
- [ ] `.env` files not committed to git

## Performance
- [ ] Dashboard loads in <3 seconds
- [ ] API responses <200ms for list endpoints
- [ ] Images optimised

## Monitoring
- [ ] Error logging configured
- [ ] Uptime monitoring enabled
- [ ] Database backups scheduled
