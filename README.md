# bootme

AutoHotkey script installation manager with TUI interface.

## Installation

### npx (Node.js)

```bash
npx @medizana/bootme autohotkey
# or from GitHub
npx github:QofJ/bootme autohotkey
```

### uvx (Python)

```bash
uvx bootme autohotkey
# or from GitHub
uvx --from git+https://github.com/QofJ/bootme.git bootme autohotkey
```

## Usage

Run the installer and follow the TUI prompts to select which AutoHotkey scripts to install.

## Development

### Adding new AutoHotkey scripts

1. Add your `.ahk` file to `assets/autohotkeys/` directory
2. Commit your changes - the pre-commit hook will automatically sync to `src/bootme/assets/autohotkeys/`

```bash
# Manual sync (if needed)
npm run sync-assets
```

> **Note**: Both directories must stay in sync to support npx and uvx users. The pre-commit hook handles this automatically.

### Setup

```bash
# Install dependencies
npm install

# Setup git hooks
npm run prepare
```
