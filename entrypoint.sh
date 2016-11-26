#!/dumb-init /bin/bash

IAM_SYNC_INTERVAL=${IAM_SYNC_INTERVAL:-15m}

if [[ ! -d /var/run/sshd ]]; then
    mkdir -p /var/run/sshd
fi

# first sync is mandatory
/opt/iam/bin/sync_users || exit 1

# store IAM credentials if given via ENV
if [[ ! -z $AWS_ACCESS_KEY_ID ]]; then
    mkdir -p /root/.aws
    cat > /root/.aws/credentials << EOF
[default]
aws_access_key_id = ${AWS_ACCESS_KEY_ID}
aws_secret_access_key = ${AWS_SECRET_ACCESS_KEY}
EOF
fi

# run the sync every X minutes in the background
# (this is poor mans cron - yes)
while true; do
    sleep $IAM_SYNC_INTERVAL
    /opt/iam/bin/sync_users
done &

# run sshd in the foreground and output logs to stdout/stderr
exec /usr/sbin/sshd -D -e -f /etc/ssh/sshd_config
