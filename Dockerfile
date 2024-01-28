FROM ubuntu:22.04
LABEL authors="austin"
ENV TZ=Asia/Shanghai
ENV GIT_USERNAME="AustinFairyland"
ENV GIT_EMAIL="fairylandhost@outlook.com"
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
sed -i 's/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
RUN apt-get update && apt-get upgrade -y && apt-get install -y openssh-client wget git
RUN #apt-get install -y tzdata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ >/etc/timezone && \
git config --global user.name $GIT_USERNAME && \
git config --global user.email $GIT_EMAIL && \
#wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
/bin/bash /tmp/miniconda.sh -b -p /opt/conda
ENV PATH /opt/conda/bin:$PATH
RUN conda create -n myenv python=3.9.13 && echo "source activate myenv" >> ~/.bashrc
WORKDIR /application
ADD . /application
RUN mkdir -p ~/.ssh/ && cp /application/conf/ssh-config/config ~/.ssh/config
RUN ssh-keygen -t ed25519 -C $GIT_EMAIL -f ~/.ssh/id_ed25519 -N "" && \
eval "$(ssh-agent -s)" && \
ssh-add ~/.ssh/id_ed25519 && \
#ssh-keyscan github.com >> ~/.ssh/known_hosts && \
ssh-keyscan ssh.github.com >> ~/.ssh/known_hosts
RUN /bin/bash -c "source activate myenv && pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple"
CMD ["/bin/bash", "-c", "cat ~/.ssh/id_ed25519.pub && source activate myenv && python main.py"]
