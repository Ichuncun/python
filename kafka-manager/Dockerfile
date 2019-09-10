FROM openjdk:8

# env ZK_HOSTS="localhost:2181" 
# env BASIC_AUTH_ENABLE="false"
# env BASIC_AUTH_USER="admin"
# env BASIC_AUTH_PASS="admin"
env JAVA_OPTS="-XX:+UnlockExperimentalVMOptions -XX:+UseCGroupMemoryLimitForHeap"
ADD *.tar.gz /
CMD ["/kafka-manager/bin/kafka-manager"]
