#!/usr/bin/env bash
set -e

# heimdall installer — local-hatch flow
# Drops the generic twin egg hatcher next to you and runs it against
# this repo's identity (rappid + soul + agents).
#
# Heimdall's existing front-door installer (installer/install.sh) installs
# the brainstem itself.  This file is different — it brings Heimdall LOCAL
# as a twin under ~/.rapp/twins/<hash>/ so the global brainstem's Twin
# agent can boot and chat with it.
#
#   curl -fsSL https://raw.githubusercontent.com/kody-w/heimdall/main/install.sh | bash

MIRROR_BRANCH="${TWIN_EGG_HATCHER_BRANCH:-main}"
HATCHER_NAME="twin_egg_hatcher_agent.py"
MIRROR_URL="https://raw.githubusercontent.com/kody-w/twin-egg-hatcher/${MIRROR_BRANCH}/${HATCHER_NAME}"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

echo ""
echo -e "${CYAN}🌈 heimdall${NC}"
echo "   Watcher of the Bifrost · hatch local via twin-egg-hatcher"
echo ""

BRAINSTEM_HOME="${BRAINSTEM_HOME:-$HOME/.brainstem}"
if [ ! -f "$BRAINSTEM_HOME/brainstem.py" ]; then
    echo -e "${YELLOW}!${NC} No grail brainstem found at $BRAINSTEM_HOME"
    echo "  Install it first:"
    echo "    curl -fsSL https://kody-w.github.io/RAPP/installer/install.sh | bash"
    echo ""
fi

echo "   Fetching the generic hatcher from kody-w/twin-egg-hatcher..."
if ! curl -fsSL "$MIRROR_URL" -o "$HATCHER_NAME"; then
    echo -e "${RED}✗${NC} Download failed."
    echo "  Fallback: gh repo clone kody-w/twin-egg-hatcher"
    exit 1
fi
chmod +x "$HATCHER_NAME"
echo -e "${GREEN}✓${NC} Saved ${HATCHER_NAME}"
echo ""
echo "   Hatch Heimdall (pulls identity from this repo on GitHub):"
echo -e "     ${CYAN}python ./${HATCHER_NAME} hatch --source kody-w/heimdall${NC}"
echo ""
echo "   Or, if you cloned this repo, hatch from cwd:"
echo -e "     ${CYAN}python ./${HATCHER_NAME} hatch${NC}"
echo ""
echo "   Then from the global brainstem:"
echo -e "     ${CYAN}Twin(action='list')${NC}"
echo -e "     ${CYAN}Twin(action='chat', rappid_uuid='<rappid>', message='who passes the Bifrost?')${NC}"
echo ""
echo -e "${GREEN}🌈 ready.${NC}"
