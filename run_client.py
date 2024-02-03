from whisper_live.client import TranscriptionClient
client = TranscriptionClient(
  "localhost",
  9090,
  is_multilingual=False,
  lang="en",
  translate=False,
  model="small"
)

client()