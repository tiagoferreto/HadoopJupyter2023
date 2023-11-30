# Use Ubuntu 20.04 as the base image
FROM ubuntu:20.04

# Set environment variables to configure timezone without user interaction
ENV DEBIAN_FRONTEND=noninteractive

# Update apt repositories and install required packages
RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    apt-get install -y openjdk-8-jdk ssh pdsh vim wget apt-utils python3 python3-pip ipython3 less unzip sudo net-tools iputils-ping && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Enable read, write, and execution access to /opt folder for all users
RUN chmod -R 777 /opt

# Create a new user 'hadoop', set bash as the shell, add to sudo group
RUN useradd -m -s /bin/bash hadoop && \
    usermod -aG sudo hadoop && \
    sed -i "\$ahadoop  ALL=(ALL) NOPASSWD:ALL" /etc/sudoers

# Update SSH configuration to disable host key checking
RUN echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config && \
    echo "UserKnownHostsFile /dev/null" >> /etc/ssh/ssh_config

# Switch to hadoop user
USER hadoop

# Generate SSH key without passphrase
# Copy generated public key to authorized_keys
RUN mkdir -p /home/hadoop/.ssh && \
    ssh-keygen -t rsa -f /home/hadoop/.ssh/id_rsa -q -N "" && \
    cat /home/hadoop/.ssh/id_rsa.pub >> /home/hadoop/.ssh/authorized_keys && \
    chmod 600 /home/hadoop/.ssh/authorized_keys
# && \
#    chown -R hadoop:hadoop /home/hadoop/.ssh

# Set working directory to /opt
WORKDIR /opt

# Download and unpack Hadoop
RUN wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz && \
    tar -xzvf hadoop-3.3.6.tar.gz && \
    rm hadoop-3.3.6.tar.gz && \
    ln -s /opt/hadoop-3.3.6 /opt/hadoop

# Append JAVA_HOME to hadoop-env.sh
RUN echo "export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-arm64" >> /opt/hadoop/etc/hadoop/hadoop-env.sh

# Copy configuration files to Hadoop etc folder
COPY core-site.xml /opt/hadoop/etc/hadoop/core-site.xml
COPY hdfs-site.xml /opt/hadoop/etc/hadoop/hdfs-site.xml
COPY yarn-site.xml /opt/hadoop/etc/hadoop/yarn-site.xml
COPY mapred-site.xml /opt/hadoop/etc/hadoop/mapred-site.xml

# Copy workers file
COPY workers /opt/hadoop/etc/hadoop/workers

# Install JupyterLab
# RUN pip3 install jupyterlab

# Set environment variables
# ENV JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64 \

# ENV JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-arm64 \
#     PDSH_RCMD_TYPE=ssh \
#     HADOOP_HOME=/opt/hadoop \
#     HADOOP_VERSION=3.3.6 \
#     HADOOP_COMMON_HOME=/opt/hadoop \
#     HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop \
#     HADOOP_HDFS_HOME=/opt/hadoop \
#     HADOOP_MAPRED_HOME=/opt/hadoop \
#     HADOOP_YARN_HOME=/opt/hadoop \
#     PATH=${PATH}:/opt/hadoop/bin:/opt/hadoop/sbin

RUN cat <<EOF > /opt/envvars.sh
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-arm64
export PDSH_RCMD_TYPE=ssh
export HADOOP_HOME=/opt/hadoop
export HADOOP_VERSION=3.3.6
export HADOOP_COMMON_HOME=\${HADOOP_HOME}
export HADOOP_CONF_DIR=\${HADOOP_HOME}/etc/hadoop
export HADOOP_HDFS_HOME=\${HADOOP_HOME}
export HADOOP_MAPRED_HOME=\${HADOOP_HOME}
export HADOOP_YARN_HOME=\${HADOOP_HOME}
export PATH=\${PATH}:\${HADOOP_HOME}/bin:\${HADOOP_HOME}/sbin
EOF

USER root

RUN mkdir /var/run/sshd

# Expose SSH port
EXPOSE 22

# Set the entrypoint script to start the SSH server
CMD ["/usr/sbin/sshd", "-D"]

# RUN echo "#ENTRYPOINT" > /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# CMD [ "/bin/bash" ]

# ENTRYPOINT [ "/bin/bash" ]

# ENTRYPOINT ["/bin/bash","/entrypoint.sh"]

# ... (remaining instructions)

# Start a shell by default when the container is run
# CMD ["/bin/bash"]
