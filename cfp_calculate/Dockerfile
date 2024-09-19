FROM ubuntu:20.04
WORKDIR /root
RUN apt-get update && DEBIAN_FRONTEND=noninteractive TZ="Asia/Taipei" apt-get install -y locales build-essential libpoppler-cpp-dev pkg-config python3-dev python3-pil python3-pip && pip3 install pdftotext && sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG=en_US.UTF-8  
ENV LANGUAGE=en_US:en  
ENV LC_ALL=en_US.UTF-8
CMD ["bash"]
