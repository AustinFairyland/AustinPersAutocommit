FROM ubuntu:22.04
LABEL authors="austin"
WORKDIR /application
ADD . /application
ENV TZ="Asia/Shanghai"
ENV DEBIAN_FRONTEND="noninteractive"
ENV GIT_USERNAME="AustinFairyland"
ENV GIT_EMAIL="fairylandhost@outlook.com"
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
    apt-get update && apt-get upgrade -y && apt-get install -y openssh-client wget git tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ >/etc/timezone && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    git config --global user.name $GIT_USERNAME && \
    git config --global user.email $GIT_EMAIL && \
    ssh-keygen -t ed25519 -C $GIT_EMAIL -f ~/.ssh/id_ed25519 -N "" && \
    eval "$(ssh-agent -s)" && \
    ssh-add ~/.ssh/id_ed25519 && \
#    ssh-keyscan github.com >> ~/.ssh/known_hosts && \
    ssh-keyscan ssh.github.com >> ~/.ssh/known_hosts && \
#    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    /bin/bash /tmp/miniconda.sh -b -p /opt/conda
ENV PATH /opt/conda/bin:$PATH
RUN conda create -n venv python=3.9.13 -y && echo "source activate venv" >> ~/.bashrc && \
    mkdir -p ~/.ssh/ && cp /application/conf/ssh-config/config ~/.ssh/config && \
    /bin/bash -c "source activate venv && pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple" && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    unset DEBIAN_FRONTEND && \
    cat ~/.ssh/id_ed25519.pub
CMD ["/bin/bash", "-c", "cat ~/.ssh/id_ed25519.pub && source activate venv && python main.py"]
