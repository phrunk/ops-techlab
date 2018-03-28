FROM centos:7

RUN yum -y update && \
    yum -y install python-flask && \
    yum clean all
ADD malloc.py /usr/local/bin

EXPOSE 8000

CMD ["/usr/local/bin/malloc.py"]
