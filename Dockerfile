FROM fedora:latest
COPY ./test_groupkt_api.py /root/
RUN dnf install -y python3-pytest python3-requests
CMD ["pytest-3", "/root/test_groupkt_api.py"]
