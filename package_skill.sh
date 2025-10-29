#!/bin/bash
# Package Postman Skill for Claude Desktop
# This script creates a clean zip file suitable for loading into Claude Desktop

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
OUTPUT_DIR="${SCRIPT_DIR}/.."
ZIP_NAME="postman-skill.zip"
TEMP_ZIP="${OUTPUT_DIR}/${ZIP_NAME}"

echo "🔧 Packaging Postman Skill for Claude Desktop..."
echo ""

# Check if we're in the right directory
if [ ! -f "${SCRIPT_DIR}/SKILL.md" ]; then
    echo "❌ Error: SKILL.md not found. Please run this script from the postman-skill directory."
    exit 1
fi

# Remove old zip if it exists
if [ -f "${TEMP_ZIP}" ]; then
    echo "🗑️  Removing old ${ZIP_NAME}..."
    rm "${TEMP_ZIP}"
fi

# Create the zip file with exclusions
echo "📦 Creating zip file..."
cd "${SCRIPT_DIR}"

zip -r "${TEMP_ZIP}" . \
    -x "venv/*" \
    -x ".git/*" \
    -x ".gitignore" \
    -x "*.DS_Store" \
    -x "*.pyc" \
    -x "*__pycache__/*" \
    -x ".env" \
    -x ".env.*" \
    -x ".claude/*" \
    -x "*.egg-info/*" \
    -x "dist/*" \
    -x "build/*" \
    -x ".pytest_cache/*" \
    -x ".coverage" \
    -x "htmlcov/*" \
    -x "*.log" \
    -x "tmp/*" \
    -x "*.tmp" \
    -x ".vscode/*" \
    -x ".idea/*" \
    -x "*.swp" \
    -x "*.swo" \
    -x "package_skill.sh" \
    -x ".skillignore" \
    > /dev/null

# Get file size
FILE_SIZE=$(du -h "${TEMP_ZIP}" | cut -f1)

echo ""
echo "✅ Success! Skill packaged successfully."
echo ""
echo "📄 File: ${TEMP_ZIP}"
echo "💾 Size: ${FILE_SIZE}"
echo ""
echo "📋 Next steps:"
echo "   1. Open Claude Desktop"
echo "   2. Go to Settings > Skills"
echo "   3. Click 'Install Skill' and select ${ZIP_NAME}"
echo ""
echo "⚠️  Note: Claude Desktop has a limit of 10 folder depth."
echo "   This script automatically excludes venv/, .git/, and other deep directories."
echo ""
