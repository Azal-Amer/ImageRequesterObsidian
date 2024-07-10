# Image Requester Project

The Image Requester project is a comprehensive solution for seamlessly integrating images captured on mobile devices into Obsidian notes. It consists of three main components: a server running on a Raspberry Pi, a Telegram bot for mobile image capture, and an Obsidian plugin for image insertion and management. See each subfolder for it's respective README. The python folder contains the server code, and the plugin folder holds the plugin. The whole project is free to setup *if you have a domain, and a idle computer.*

General usage is listed below.
## Usage
Given the below setup, you text your bot an image with a caption, and it stores it in the server. You can send several images without re-syncing. Once you sync, the images are auto-inserted in place of the tags, in consecutive order, then deleted. If there is not enough tags, the remaining images are kept on the server. 


## Components

### Server (main.py)

The server is the central hub of the Image Requester project. It is responsible for receiving images and captions from the Telegram bot, storing them in a JSON database, and providing API endpoints for the Obsidian plugin to interact with.

#### Exposed Endpoints

- `/telegram-webhook` (POST): Receives images and captions from the Telegram bot and saves them to the database.
- `/controller` (POST): Handles image requests from the Obsidian plugin. Requires the following parameters:
  - `numImages`: The number of images requested by the plugin.
  - `apiKey`: The API key for authentication.
- `/confirmation` (POST): Receives confirmation from the Obsidian plugin after successful image download. Deletes the corresponding images from the server. Requires the following parameters:
  - `imageIDs`: An array of image IDs to be deleted.
  - `apiKey`: The API key for authentication.

### Telegram Bot

The Telegram bot serves as the interface for users to capture and send images along with their captions from their mobile devices. It forwards the received images and captions to the server via the `/telegram-webhook` endpoint.

#### Commands

- `/status`: Returns the number of images currently stored in the database.
- `/wipe`: Deletes all images and clears the database.

### Obsidian Plugin

The Obsidian plugin enhances the note-taking experience by allowing users to insert `\img` tags in their notes where they want images to appear. It communicates with the server to retrieve image URLs and metadata, downloads the images, and replaces the tags with actual image links and captions.

#### Features

- Replaces `\img` tags in notes with actual images and captions.
- Provides a command and a ribbon icon to trigger the image replacement process.
- Allows users to configure the server URL and API key through the plugin settings.

## Setup and Usage

1. Set up the server on a Raspberry Pi and ensure it is accessible via a static domain (e.g., using Cloudflare Tunnels).
2. Create a Telegram bot and configure it to forward images and captions to the server's `/telegram-webhook` endpoint.
3. Install the Obsidian plugin in your Obsidian vault and configure the server URL and API key in the plugin settings.
4. Insert `\img` tags in your notes where you want images to appear.
5. Capture images on your mobile device and send them to the Telegram bot along with captions.
6. In Obsidian, trigger the image replacement process using the provided command or ribbon icon.
7. The plugin will retrieve the images from the server, replace the tags with actual image links and captions, and send a confirmation to the server for image deletion.

## Contributing

Contributions to the Image Requester project are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on the project's GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).
