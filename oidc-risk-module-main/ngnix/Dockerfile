# instructions from: https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Docker-Nginx-reverse-proxy-setup-example

# sudo docker build -t nginx-reverse-proxy .
# docker run --rm --name nginx-reverse-proxy -p 8080:8080 -it nginx-reverse-proxy

#sudo iptables -A INPUT  -p tcp --dport 5001 --src moodle.oidc-prince.dei.uc.pt,172.17.0.0/16,10.10.0.0/8 -j ACCEPT

#sudo iptables -A INPUT  -p tcp --dport 8000 --src moodle.oidc-prince.dei.uc.pt,172.17.0.0/8,10.10.0.0/8 -j ACCEPT

FROM nginx:latest
COPY default.conf /etc/nginx/conf.d/default.conf
COPY moodle.oidc-prince.dei.uc.pt.crt /usr/ngnix/moodle.oidc-prince.dei.uc.pt.crt
COPY moodle.oidc-prince.dei.uc.pt.key /usr/ngnix/moodle.oidc-prince.dei.uc.pt.key

