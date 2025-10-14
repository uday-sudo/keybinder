#!/usr/bin/env bash
set -euo pipefail

# =====================================================
# Configuration
# =====================================================

CONTAINER_NAME="keybinder-test"
VERSION="0.1.0"
REGISTRY="git.homebox.com/uday-sudo/keybinder"
IMAGE_TAG="${REGISTRY}/${CONTAINER_NAME}:${VERSION}"

# =====================================================
# Build & Push
# =====================================================

echo "🔨 Building container image: ${IMAGE_TAG}"
cp ../flake.nix .
cp ../flake.lock .
podman build -t "${IMAGE_TAG}" -f Containerfile .
rm flake.nix
rm flake.lock

echo "✅ Build complete."

# Make sure you’re logged in before pushing:
# podman login git.homebox.com

echo "📤 Pushing image to ${REGISTRY}..."
podman push "${IMAGE_TAG}"

echo "🚀 Done. Image pushed:"
