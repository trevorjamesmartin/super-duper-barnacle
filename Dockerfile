FROM debian:buster-slim

RUN apt-get update \
 && apt-get install -y unzip curl python3 python3-pip \
 && apt-get install -y wget iproute2 net-tools iputils-ping expect \
 && apt-get install -y --no-install-recommends expect

ENV TUNER_IP="${TUNER_IP}"
ADD entrypoint.sh /entrypoint.sh

EXPOSE 5000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/bin/bash"]