#!/bin/bash
set -e

# Pre-deployment tasks
echo "Running pre-deployment tasks..."

# Install Python dependencies
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo "Pre-deployment tasks completed successfully!"
