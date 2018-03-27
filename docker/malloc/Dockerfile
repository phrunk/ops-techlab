FROM centos:7

ADD malloc.c /tmp
RUN yum -y update && \
    yum -y install gcc && \
    gcc -o /usr/local/bin/malloc /tmp/malloc.c && \
    yum -y history undo last

EXPOSE 8000

CMD ["/usr/local/bin/malloc"]
