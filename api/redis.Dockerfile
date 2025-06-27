FROM redis:alpine
CMD ["sh", "-c", "if [ -n \"$REDIS_PASSWORD\" ]; then redis-server --requirepass \"$REDIS_PASSWORD\"; else redis-server; fi"]