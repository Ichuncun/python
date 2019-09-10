FROM tomcat:8-alpine

# env dubbo.registry.address=zookeeper://192.168.1.104:2181
env JAVA_OPTS="-XX:+UnlockExperimentalVMOptions -XX:+UseCGroupMemoryLimitForHeap"
RUN rm -rf webapps/* 
ADD *.tar.gz webapps/
