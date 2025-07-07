#!/bin/bash

echo "🟢 Staging all changes..."
git add .

echo "📝 Enter your commit message: "
read commit_msg

if [ -z "$commit_msg" ]; then
  echo "❌ Commit message cannot be empty."
  exit 1
fi

echo "🔄 Committing changes..."
git commit -m "$commit_msg"

echo "🚀 Pushing to GitHub..."
git push origin main

echo "✅ All done!"
