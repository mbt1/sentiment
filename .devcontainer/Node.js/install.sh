#!/bin/bash
curl -sL https://deb.nodesource.com/setup_14.x | bash -
apt-get install -y nodejs
apt-get install -y npm

node -v
npm -v
npx -v
