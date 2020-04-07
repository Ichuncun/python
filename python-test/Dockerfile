FROM python:3-alpine

RUN apk add --no-cache --virtual .build-deps alpine-sdk tzdata \
&& cp -rf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

COPY . /

CMD [ "python3", "test.py" ]

kubectl create secret generic kube-registry --from-file=.dockerconfigjson=/root/.docker/config.json --type=kubernetes.io/dockerconfigjson
for i in $(kubectl get deploy --no-headers -n zhonggu|cut -d' ' -f1); do kubectl scale deploy $i --replicas 1 -n zhonggu;done

WARPATH=$(find ${WORKSPACE} -name *.war) && WAR=${WARPATH##*/}
cd ${WARPATH%/*} && cp /opt/Dockerfile . && cp /opt/aliyun.yaml .

docker build -t registry.cn-hangzhou.aliyuncs.com/daianla-prod/sd-${WAR%.*}:${GIT_COMMIT} .
docker push registry.cn-hangzhou.aliyuncs.com/daianla-prod/sd-${WAR%.*}:${GIT_COMMIT}
sed -i "s/dubbo-admin/${WAR%.*}/g" aliyun.yaml && kubectl apply -f aliyun.yaml -n zhonggu --kubeconfig=/root/.kube/conf
kubectl -n zhonggu set image deployment/${WAR%.*} ${WAR%.*}=registry.cn-hangzhou.aliyuncs.com/daianla-prod/sd-${WAR%.*}:${GIT_COMMIT} --kubeconfig=/root/.kube/conf