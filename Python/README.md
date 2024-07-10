# Image Requester Server

The Image Requester Server is the backend component of the Image Requester project, responsible for handling image management and providing API endpoints for the Obsidian plugin to interact with.

## Installation

1. Clone the repository and navigate to the server directory.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up the necessary environment variables in a `.env` file:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
   - `WEBHOOK_URL`: The public URL where your server is accessible.
4. Run the server using `python main.py`.

## Configuration

The server uses the following environment variables for configuration:

- `TELEGRAM_BOT_TOKEN`: The token for your Telegram bot, obtained from the BotFather.
- `WEBHOOK_URL`: The public URL where your server is accessible, used for setting up the Telegram webhook.
- `WEBHOOK_KEY`: The API key used for authentication when communicating with the Obsidian plugin.

## Functionality

The server performs the following main functions:

1. Receives images and captions from the Telegram bot via the `/telegram-webhook` endpoint.
2. Stores the received images and their metadata in a JSON database (`imageCaptionDatabase.json`).
3. Handles image requests from the Obsidian plugin via the `/controller` endpoint, returning the requested number of image URLs and metadata.
4. Receives confirmation from the Obsidian plugin after successful image download via the `/confirmation` endpoint, and deletes the corresponding images from the server.

## Database Structure

The server uses a JSON file (`imageCaptionDatabase.json`) to store image metadata. Each image entry contains the following fields:

- `url`: The URL where the image is accessible.
- `caption`: The caption associated with the image.
- `file_id`: The unique identifier of the image file.

## Contributing

Contributions to the Image Requester Server are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on the project's GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).
