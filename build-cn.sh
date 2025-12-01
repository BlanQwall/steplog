#!/bin/bash

# Clean previous deployment directory
rm -rf deploy-cn
mkdir deploy-cn

# Rsync everything except excluded paths
rsync -av \
  --exclude='.git/' \
  --exclude='.github/' \
  --exclude='archive/' \
  --exclude='deploy-cn/' \
  --exclude='*.sh' \
  --exclude='.gitignore' \
  ./ deploy-cn/

echo "Build-cn completed. deploy-cn/ is ready."
