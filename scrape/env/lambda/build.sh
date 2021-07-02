docker build \
  -t kagemeka/adam-pixiv-lambda \
  -f Dockerfile \
  ../../

aws ecr get-login-password --region ap-northeast-1 | \
docker login --username AWS --password-stdin 867493361193.dkr.ecr.ap-northeast-1.amazonaws.com

docker tag kagemeka/adam-pixiv-lambda 867493361193.dkr.ecr.ap-northeast-1.amazonaws.com/adam-pixiv-lambda:latest

docker push 867493361193.dkr.ecr.ap-northeast-1.amazonaws.com/adam-pixiv-lambda:latest