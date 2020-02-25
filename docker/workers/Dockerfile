FROM statice:latest

# Configure and run supervisord.
USER root
RUN apt-get update && apt-get install -y supervisor
COPY docker/workers/supervisord.conf /etc/supervisord.conf
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisord.conf"]