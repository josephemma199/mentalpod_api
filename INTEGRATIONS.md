# Integrations Setup

## Notion
1) Create an internal integration in Notion and copy its token.
2) Share your target database with the integration (Full Access).
3) Put `NOTION_TOKEN` and `NOTION_DB_ID` in `.env`.
4) Use `POST /episode-package?export=true` to create a page with your outline + references.

## Google Docs
1) Create an OAuth client (Desktop or Web) in Google Cloud.
2) Obtain `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`.
3) Generate a `GOOGLE_REFRESH_TOKEN` for the scopes in code (docs + drive.file).
4) (Optional) Set `GOOGLE_DRIVE_PARENT_ID` to auto-file new docs.
5) Use `POST /episode-package?export=true` to create a Google Doc.

## Transcription (Whisper)
- Set `OPENAI_API_KEY` and `TRANSCRIBE_PROVIDER=openai`.
- Provide a direct `audio_url` to `/analyze` (or extend to file uploads).
