# Image Requester Obsidian Plugin

## Overview

The Image Requester plugin for Obsidian enhances your note-taking workflow by seamlessly integrating images captured on your mobile device into your Obsidian notes. This plugin works in conjunction with a Raspberry Pi server and a Telegram bot to automate the process of inserting images into your notes. To see the full decompiled source code, look inside the sandbox vault.

## Features

- Replace `\img` tags in your notes with actual images
- Automatic image download and insertion
- Custom server URL and API key configuration
- Ribbon icon for quick access to image replacement
- Supports captions for images

## Files

- `main.ts`: Core plugin functionality
- `network.ts`: Handles network requests to the server
- `formatting.ts`: Manages image formatting and insertion

## Installation

1. Download the latest release from the GitHub repository
2. Extract the zip file into your Obsidian plugins folder
3. Enable the plugin in Obsidian settings

## Configuration

1. Open Obsidian settings
2. Navigate to the Image Requester plugin settings
3. Enter your server URL (e.g., `https://your-server-url.com`)
4. Enter your API key

## Usage

1. In your notes, use `\img` tags where you want images to be inserted
2. Capture images on your mobile device and send them to the associated Telegram bot
3. In Obsidian, click the Image Requester ribbon icon or run the "Replace Image Tags" command
4. The plugin will replace `\img` tags with the corresponding images

## Commands

- **Replace Image Tags**: Scans the current note for `\img` tags and replaces them with the corresponding images

## Development

To set up the development environment:

1. Clone the repository
2.  Run `npm install` to install dependencies
3. Use `npm run dev` to start the development build process

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)

## Support

If you encounter any issues or have questions, please file an issue on the GitHub repository.

## Acknowledgements

This plugin is part of the larger Image Requester project, which includes a Raspberry Pi server component and a Telegram bot integration.
